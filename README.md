# 🎬 OneWord AI - Cinematic Subtitle Generator

<div align="center">

**Generate viral-style one-word subtitles from video/audio using Whisper AI**

[![PyPI](https://img.shields.io/pypi/v/oneword-ai)](https://pypi.org/project/oneword-ai/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](license.txt)

Perfect for creating high-energy reels, shorts, and TikToks! 🚀

[Installation](#-installation) • [Usage](#-usage) • [Features](#-features) • [Credits](#-credits)

</div>

---

## ✨ Features

- 🎯 **Three Subtitle Modes**: One Word, Two Word Punch, Phrase Mode
- 🌍 **Multi-Language Support**: Auto-detect or specify (English, Hindi, Urdu, Spanish)
- 🤖 **Multiple AI Models**: 
  - OpenAI Whisper (Medium, Large)
  - Hindi2Hinglish (Oriserve/Whisper-Hindi2Hinglish-Prime) 🇮🇳
- 💻 **Dual Interface**: CLI for power users, Web UI for visual workflow
- 📦 **Easy Installation**: One-line pip install
- ☁️ **Cloud Ready**: Works seamlessly on Google Colab

---

## 🚀 Installation

```bash
pip install oneword-ai
```

**Prerequisites**: Install [FFmpeg](https://ffmpeg.org/) on your system.

---

## 📖 Usage

### Option 1: Web Interface (Easiest)

Start the web server:

```bash
python -m onewordai.api.main
```

Then open http://localhost:8000 in your browser.

**Features:**
- 📤 Drag & drop file upload
- 📊 Real-time download progress with speed & ETA
- ⏱️ Live transcription status updates
- ❌ Cancel processing anytime
- ⚠️ Reload protection (won't lose progress)
- 📥 Instant SRT download

---

### Option 2: Google Colab

Run OneWord AI in the cloud with full Web UI or Python API:

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ambrishyadav-byte/OnewordAI/blob/main/OneWord_Colab.ipynb)

**Two Options in Colab:**

**A) Web UI with Public URL (Recommended):**
```python
!pip install oneword-ai pyngrok

from pyngrok import ngrok
import threading

def start_server():
    import uvicorn
    uvicorn.run("onewordai.api.main:app", host="0.0.0.0", port=8000)

threading.Thread(target=start_server, daemon=True).start()
import time; time.sleep(5)

public_url = ngrok.connect(8000)
print(f"🌐 Web UI: {public_url}")
```

**B) Python API:**
```python
!pip install oneword-ai

from onewordai.core.engine import SubtitleGenerator

generator = SubtitleGenerator(model_name="medium")
output = generator.process("video.mp4", mode="oneword")
print(f"✅ Saved: {output}")
```

---

### Option 3: Command Line (CLI)

For batch processing and automation:

```bash
# Basic usage
python -m onewordai.cli -i video.mp4

# With options
python -m onewordai.cli -i video.mp4 -m medium -lang hi -mode oneword
```

**See [CLI.md](CLI.md) for full documentation.**

---

## 📊 Subtitle Modes

| Mode | Description | Best For |
|------|-------------|----------|
| **oneword** | Each word = separate subtitle | High-energy viral content, reels |
| **twoword** | Groups of 2 words | Punchy messaging, Instagram posts |
| **phrase** | Full sentence segments | YouTube videos, longer content |

---

## 🎨 Model Options

| Model | Size | Speed | Quality | Language |
|-------|------|-------|---------|----------|
| **medium** | ~1.5GB | Fast | ⭐⭐⭐⭐ | Multi-language |
| **large** | ~3GB | Slower | ⭐⭐⭐⭐⭐ | Multi-language |
| **Oriserve/Whisper-Hindi2Hinglish-Prime** | ~1.5GB | Fast | ⭐⭐⭐⭐⭐ | Hindi → Hinglish |

> **Note**: Models are downloaded automatically on first use and cached locally.

---

## 🤝 Credits

This project wouldn't be possible without these amazing open-source projects:

### Core Technologies
- **[OpenAI Whisper](https://github.com/openai/whisper)** - State-of-the-art speech recognition model
- **[Oriserve/Whisper-Hindi2Hinglish-Prime](https://huggingface.co/Oriserve/Whisper-Hindi2Hinglish-Prime)** - Fine-tuned Hindi to Hinglish transcription
- **[HuggingFace Transformers](https://github.com/huggingface/transformers)** - Model loading and inference framework

### Backend & UI
- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance Python web framework
- **[Gradio](https://gradio.app/)** - ML web interface library
- **[FFmpeg](https://ffmpeg.org/)** - Multimedia processing toolkit

### Special Thanks
- OpenAI team for making Whisper open-source
- Oriserve team for the specialized Hindi model
- All open-source contributors

---

## 📜 License

MIT License - see [license.txt](license.txt)

Free to use for personal and commercial projects!

---

## 👨‍💻 Author

**Built with ❤️ by [Ambrish Yadav](https://github.com/Ambrishyadav-byte)**

💼 Connect: [@ambrish.yadav.1](https://instagram.com/ambrish.yadav.1)

📦 PyPI: [oneword-ai](https://pypi.org/project/oneword-ai/)

---

<div align="center">

⭐ **Star this repo if you find it useful!** ⭐

[Report Bug](https://github.com/Ambrishyadav-byte/OnewordAI/issues) • [Request Feature](https://github.com/Ambrishyadav-byte/OnewordAI/issues)

</div>