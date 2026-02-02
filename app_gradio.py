"""
Gradio interface for Hugging Face Spaces.
"""
import gradio as gr
from onewordai.core.engine import SubtitleGenerator
from pathlib import Path
import tempfile


def process_video(
    video_file,
    model_choice,
    language_choice,
    mode_choice,
    progress=gr.Progress()
):
    """Process video and return SRT file."""
    if video_file is None:
        return None, "❌ Please upload a file first"
    
    try:
        # Update progress
        progress(0, desc="Initializing...")
        
        # Create generator
        generator = SubtitleGenerator(model_name=model_choice)
        
        # Process
        progress(0.1, desc="Loading model...")
        
        # Create temp output file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False, encoding='utf-8') as f:
            output_path = f.name
        
        def progress_callback(percent):
            progress(percent / 100, desc=f"Transcribing... {percent}%")
        
        
        result_path = generator.process(
            input_path=video_file,
            output_path=output_path,
            language=language_choice if language_choice != "Auto Detect" else None,
            mode=mode_choice.lower().replace(" ", ""),
            progress_callback=progress_callback
        )
        
        progress(1.0, desc="Complete!")
        
        # Return the file path - Gradio will create download button automatically
        return result_path, "✅ Success! Click the file above to download your SRT."
        
    except Exception as e:
        return None, f"❌ Error: {str(e)}"


# ========== GRADIO INTERFACE ==========
with gr.Blocks(
    theme=gr.themes.Base(),
    title="OneWord AI - Subtitle Generator",
    css="""
    .gradio-container {
        font-family: 'Space Grotesk', sans-serif;
    }
    """
) as app:
    gr.Markdown(
        """
        # 🎬 OneWord AI - Subtitle Generator
        
        Generate cinematic one-word subtitles using Whisper AI.
        Perfect for high-energy reels and shorts!
        """
    )
    
    with gr.Row():
        with gr.Column():
            # Input
            video_input = gr.File(
                label="📁 Upload Video/Audio",
                file_types=["video", "audio"]
            )
            
            # Model selection
            model_input = gr.Radio(
                choices=["tiny", "base", "small"],
                value="base",
                label="🤖 Whisper Model",
                info="Tiny = Fastest, Small = Most Accurate"
            )
            
            # Language selection
            language_input = gr.Dropdown(
                choices=["Auto Detect", "English", "Hindi", "Urdu", "Spanish"],
                value="Auto Detect",
                label="🌍 Language"
            )
            
            # Mode selection
            mode_input = gr.Radio(
                choices=["One Word", "Two Word", "Phrase"],
                value="One Word",
                label="📝 Subtitle Mode",
                info="One Word = Each word separate, Two Word = Punch effect, Phrase = Full sentences"
            )
            
            # Process button
            process_btn = gr.Button("🚀 Generate Subtitles", variant="primary", size="lg")
        
        with gr.Column():
            # Output
            output_file = gr.File(label="📥 Download SRT")
            status_output = gr.Textbox(label="Status", interactive=False)
    
    # Event handler
    process_btn.click(
        fn=process_video,
        inputs=[video_input, model_input, language_input, mode_input],
        outputs=[output_file, status_output]
    )
    
    gr.Markdown(
        """
        ---
        ### 💡 How to Use
        1. Upload your video/audio file
        2. Select Whisper model (Base recommended)
        3. Choose language (or Auto Detect)
        4. Pick subtitle mode
        5. Click Generate!
        """
    )
    gr.Markdown("""
        <div style="text-align: center; margin-top: 20px;">
        Made with ❤️ for creators | Follow [@ambrish.yadav.1](https://instagram.com/ambrish.yadav.1)
        </div>
    """)


if __name__ == "__main__":
    app.launch()
