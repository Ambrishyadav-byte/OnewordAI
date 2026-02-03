"""
Lightweight Web UI for ARM devices using Flask and Whisper.cpp.
"""
import os
import secrets
from pathlib import Path
from flask import Flask, render_template_string, request, send_file, redirect, url_for

from onewordai.arm import is_whisper_cpp_installed, is_model_downloaded
from onewordai.core.engine_cpp import WhisperCppEngine

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.secret_key = secrets.token_hex(16)

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OneWord AI (ARM)</title>
    <style>
        body { font-family: -apple-system, system-ui, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #fafafa; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
        h1 { text-align: center; color: #333; margin-bottom: 30px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: 500; }
        select, input[type="file"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #6366f1; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: 600; cursor: pointer; }
        button:hover { background: #4f46e5; }
        .status { padding: 15px; border-radius: 6px; margin-top: 20px; display: none; }
        .status.processing { background: #e0f2fe; color: #0369a1; display: block; }
        .status.success { background: #dcfce7; color: #15803d; display: block; }
        .status.error { background: #fee2e2; color: #b91c1c; display: block; }
        .download-btn { display: inline-block; margin-top: 10px; padding: 8px 16px; background: #10b981; color: white; text-decoration: none; border-radius: 6px; }
    </style>
</head>
<body>
    <h1>OneWord AI <span style="font-size: 0.6em; color: #666;">ARM Edition</span></h1>
    
    <div class="card">
        <form action="/process" method="post" enctype="multipart/form-data" onsubmit="showProcessing()">
            <div class="form-group">
                <label for="file">Upload Video/Audio</label>
                <input type="file" name="file" id="file" required accept="video/*,audio/*">
            </div>
            
            <div class="form-group">
                <label for="model">Model</label>
                <select name="model" id="model">
                    <option value="tiny">Tiny (Fastest)</option>
                    <option value="base" selected>Base (Recommended)</option>
                    <option value="small">Small (Better Quality)</option>
                    <option value="medium">Medium (Slow)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="language">Language</label>
                <select name="language" id="language">
                    <option value="auto">Auto Detect</option>
                    <option value="hi">Hindi</option>
                    <option value="en">English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="mode">Subtitle Mode</label>
                <select name="mode" id="mode">
                    <option value="oneword">One Word</option>
                    <option value="twoword">Two Word Punch</option>
                    <option value="phrase">Phrase Mode</option>
                </select>
            </div>
            
            <button type="submit">Generate Subtitles</button>
        </form>
    </div>

    {% if status %}
    <div class="card status {{ status }}">
        {% if status == 'processing' %}
            Processing video... method: {{ method }}
        {% elif status == 'success' %}
            <h3>🎉 Processing Complete!</h3>
            <p>Your subtitles are ready.</p>
            <a href="/download/{{ filename }}" class="download-btn">Download SRT</a>
        {% elif status == 'error' %}
            <h3>❌ Error</h3>
            <p>{{ message }}</p>
        {% endif %}
    </div>
    {% endif %}

    <div id="processing" class="status processing">
        Processing... This may take a while on mobile devices.
    </div>

    <script>
        function showProcessing() {
            document.getElementById('processing').style.display = 'block';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    if not is_whisper_cpp_installed():
        return "<h1>Error: Whisper.cpp not installed</h1><p>Please run <code>onewordai-setup-arm</code> first.</p>"
    return render_template_string(HTML_TEMPLATE, status=None)

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return redirect(url_for('home'))
        
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('home'))

    model = request.form.get('model', 'base')
    language = request.form.get('language')
    mode = request.form.get('mode', 'oneword')

    # Check model
    if not is_model_downloaded(model):
        return render_template_string(HTML_TEMPLATE, status='error', message=f"Model '{model}' not found. Please run: bash onewordai/arm/whisper.cpp/models/download-ggml-model.sh {model}")

    if file:
        # Save uploaded file
        input_path = Path(app.config['UPLOAD_FOLDER']) / file.filename
        file.save(input_path)
        
        try:
            # Initialize engine
            engine = WhisperCppEngine(model_name=model)
            engine.load_model()
            
            # Generate subtitles
            srt_content = engine.generate_subtitles(
                audio_path=str(input_path),
                language=language if language != 'auto' else None,
                mode=mode
            )
            
            # Save output
            output_filename = input_path.stem + '.srt'
            output_path = Path(app.config['OUTPUT_FOLDER']) / output_filename
            output_path.write_text(srt_content, encoding='utf-8')
            
            return render_template_string(HTML_TEMPLATE, status='success', filename=output_filename)
            
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, status='error', message=str(e))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(Path(app.config['OUTPUT_FOLDER']) / filename, as_attachment=True)

def start_server(host='0.0.0.0', port=8000):
    """Start the ARM web server."""
    print(f"🚀 OneWord AI ARM Web UI running at http://{host}:{port}")
    app.run(host=host, port=port)

if __name__ == '__main__':
    start_server()
