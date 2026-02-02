# 🎬 OneWord AI - Cinematic Subtitle Generator

<div align="center">

**Generate viral-style one-word subtitles from video/audio using Whisper AI**

[![PyPI](https://img.shields.io/pypi/v/oneword-ai)](https://pypi.org/project/oneword-ai/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
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

### Method 1: Install from PyPI (Recommended)

```bash
pip install oneword-ai
```

**Prerequisites**: Ensure [FFmpeg](https://ffmpeg.org/) is installed on your system.

---

## 📖 Usage

### Option 1: Web Interface (Easiest)

Start the web server and process files through a beautiful UI:

```bash
# Start server
python -m onewordai.api.main
```

Then open http://localhost:8000 in your browser.

**Features:**
- 📤 Drag & drop file upload
- 📊 Real-time download progress with speed tracking
- ⏱️ Live transcription status
- ❌ Cancel processing anytime
- 📥 Instant SRT download
- ⚠️ Reload protection (won't lose progress)

---

### Option 2: Google Colab with Package

Run OneWord AI in the cloud without any local installation:

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ambrishyadav-byte/OnewordAI/blob/main/OneWord_Colab.ipynb)

**Quick Start in Colab:**

```python
# Install package
!pip install oneword-ai

# Import and use
from onewordai.core.engine import SubtitleGenerator

# Generate subtitles
generator = SubtitleGenerator(model_name="medium")
output = generator.process("video.mp4", mode="oneword")
print(f"✅ Subtitles saved: {output}")
```

---

### Option 3: Command Line Interface (CLI)

For batch processing and automation:

```bash
# Basic usage
python -m onewordai.cli -i video.mp4

# Advanced options
python -m onewordai.cli -i video.mp4 -m medium -lang hi -mode oneword
```

**See [CLI.md](CLI.md) for full CLI documentation.**

---

## 📊 Subtitle Modes

| Mode | Description | Best For |
|------|-------------|----------|
| **One Word** | Each word = separate subtitle | High-energy viral content, reels |
| **Two Word Punch** | Groups of 2 words | Punchy messaging, Instagram posts |
| **Phrase Mode** | Full sentence segments | YouTube videos, longer content |

---

## 🎨 Model Options

| Model | Size | Speed | Quality | Language Support |
|-------|------|-------|---------|------------------|
| **medium** | ~1.5GB | Fast | Good | Multi-language |
| **large** | ~3GB | Slower | Best | Multi-language |
| **Hindi2Hinglish** | ~1.5GB | Fast | Excellent for Hindi | Hindi → Hinglish |

---

## 🤝 Credits

This project wouldn't be possible without these amazing open-source projects:

### Core Technologies
- **[OpenAI Whisper](https://github.com/openai/whisper)** - Revolutionary speech recognition model
- **[Oriserve/Whisper-Hindi2Hinglish-Prime](https://huggingface.co/Oriserve/Whisper-Hindi2Hinglish-Prime)** - Hindi to Hinglish transcription model
- **[HuggingFace Transformers](https://github.com/huggingface/transformers)** - Model loading and inference

### Backend & UI
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[Gradio](https://gradio.app/)** - ML web interfaces
- **[FFmpeg](https://ffmpeg.org/)** - Audio/video processing

### Special Thanks
- OpenAI for making Whisper open-source
- Oriserve team for the Hindi2Hinglish model
- All contributors to the dependencies

---

## 📜 License

MIT License - see [license.txt](license.txt)

Free to use for personal and commercial projects!

---

## 👨‍💻 Author

**Built with ❤️ by [Ambrish Yadav](https://github.com/Ambrishyadav-byte)**

💼 Connect: [@ambrish.yadav.1](https://instagram.com/ambrish.yadav.1)

---

<div align="center">

⭐ **Star this repo if you find it useful!** ⭐

[Report Bug](https://github.com/Ambrishyadav-byte/OnewordAI/issues) • [Request Feature](https://github.com/Ambrishyadav-byte/OnewordAI/issues)

</div>