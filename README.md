# 🎬 OneWord AI - Subtitle Generator

<div align="center">

**Generate cinematic one-word subtitles from video/audio using Whisper AI**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](license.txt)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-orange)](https://github.com/openai/whisper)

Perfect for creators making high-energy reels, shorts, and TikToks!

</div>

---

## ✨ Features

- 🎯 **Three Subtitle Modes**: One Word, Two Word Punch, Phrase Mode
- 🌍 **Multi-Language**: Auto-detect or specify (English, Hindi, Urdu, Spanish)
- 🤖 **Multiple Models**: Medium, Large, and **Hindi2Hinglish** 🆕
- 📦 **Python Package**: Installable via pip with `oneword-cli` and `oneword-web` commands
- 💻 **Local CLI**: Robust command-line tool for batch processing
- 🌐 **Web UI**: Beautiful Neobrutalism-styled web interface
- ☁️ **Cloud Ready**: Works on Google Colab and Hugging Face Spaces
- 🐳 **Docker Support**: Containerized deployment

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Ambrishyadav-byte/OnewordAI.git
cd OnewordAI

# Install as a package
pip install -e .
```

**Prerequisites**: Ensure [FFmpeg](https://ffmpeg.org/) is installed on your system.

### Usage

#### 🖥️ CLI (Command Line)

See [CLI.md](CLI.md) for full documentation.

```bash
# Basic usage
oneword-cli -i video.mp4

# Full options
oneword-cli -i video.mp4 -m medium -lang hi -mode oneword
```

#### 🌐 Web UI

```bash
# Start server & open browser
oneword-web
```

Features:
- Drag & drop file upload
- Real-time progress tracking
- Instant SRT download
- Responsive Neobrutalism design

#### ☁️ Google Colab

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

1. Open `OneWord_Colab.ipynb` in Colab
2. Run all cells
3. Upload your video
4. Download your SRT!

#### 🤗 Hugging Face Space

```bash
python app_gradio.py
```

Or deploy to Hugging Face Spaces for a hosted version!

## 📊 Subtitle Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **One Word** | Each word = separate subtitle | High-energy, attention-grabbing content |
| **Two Word Punch** | Groups of 2 words | Punchy, impactful messaging |
| **Phrase Mode** | Full sentence segments | Traditional subtitle style |

## 🎨 Web UI Preview

The web interface features a stunning **Neobrutalism** design:
- Bold black borders
- Vibrant color palette
- Sharp shadows
- Grid background pattern
- Smooth animations

## 🐳 Docker Deployment

```bash
# Build image
docker build -t oneword-ai .

# Run container
docker run -p 8000:8000 oneword-ai
```

## 📁 Project Structure

```
minimalist-one-word-subtitle-generator/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   └── engine.py          # Core subtitle generation logic
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py            # FastAPI backend
│   └── web/
│       ├── index.html         # Web UI
│       ├── style.css          # Neobrutalism styles
│       └── app.js             # Frontend logic
├── cli.py                     # CLI interface
├── app_gradio.py              # Gradio app for HF Spaces
├── OneWord_Colab.ipynb        # Google Colab notebook
├── Dockerfile                 # Docker configuration
├── requirements.txt           # Python dependencies
└── README.md
```

## 🛠️ Development

### API Endpoints

- `POST /upload` - Upload video/audio file
- `POST /process` - Start transcription job
- `GET /status/{job_id}` - Check job progress
- `GET /download/{job_id}` - Download generated SRT

### Requirements

- Python 3.8+
- FFmpeg
- PyTorch
- OpenAI Whisper
- FastAPI (for web server)
- Gradio (for HF Spaces)

## 💡 Tips for Creators

### Video Editing Workflow

1. Generate SRT using OneWord AI
2. Import into your editor:
   - **CapCut**: Text → Local Captions → Upload
   - **VN Editor**: Text → SRT → Import
   - **Premiere Pro**: File → Import → Captions
3. Apply animations (Pop, Spring, Bounce)
4. Customize colors and fonts

### Best Practices

- Use **Tiny** model for quick drafts
- Use **Base** model for production (best balance)
- Use **Small** model for technical/complex content
- **One Word** mode works best for 30-60 sec reels
- Enable language selection for multilingual content

## 🤝 Contributing

Contributions welcome! Open an issue or submit a PR.

Ideas for improvements:
- Auto-capitalization for emphasis
- Color-coded keywords
- Export with burned-in subtitles
- Batch processing multiple files

## 📜 License

MIT License - see [license.txt](license.txt)

## 🤝 Credits

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Gradio](https://gradio.app/) - ML web interfaces

Built with ❤️ by [Ambrish](https://github.com/ambrish-yadav)

Follow for updates: [@ambrish.yadav.1](https://instagram.com/ambrish.yadav.1)

---

<div align="center">

⭐ Star this repo if you find it useful!

</div>