# 🎬 OneWord AI - Production Subtitle Generator

<div align="center">

**Enterprise-grade visual subtitle generator for Local & VPS Environments**

[![PyPI](https://img.shields.io/pypi/v/oneword-ai)](https://pypi.org/project/oneword-ai/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](Dockerfile)
[![License](https://img.shields.io/badge/License-MIT-green)](license.txt)

Generate viral-style subtitles locally or on your own server. No cloud notebooks, no timeouts.

[Installation](#-installation) • [Web UI](#-web-interface) • [CLI](#-command-line) • [VPS Deployment](#-vps--server-deployment)

</div>

---

## 🚀 Installation

### Local Setup (Windows/Mac/Linux)

1. **Install Python 3.9+** and [FFmpeg](https://ffmpeg.org/).
2. **Install the package**:
   ```bash
   pip install oneword-ai
   ```

---

## 🖥️ Web Interface

Start the local web server to use the visual interface:

```bash
oneword-web
# OR
python -m onewordai.api.main
```

Open **http://localhost:8000** in your browser.

**Features:**
- ⚡ **Local Processing**: No file size limits, 100% privacy.
- 🎯 **3 Modes**: One Word, Two Word, Phrase.
- 🌍 **Multi-Language**: Supports English, Hindi, Urdu, Spanish.
- 🇮🇳 **Special Hindi Model**: Uses `Oriserve/Whisper-Hindi2Hinglish-Prime`.

---

## ⌨️ Command Line (CLI)

Perfect for batch processing or automation scripts:

```bash
# Process a single video
oneword-cli -i input_video.mp4

# Customize settings
oneword-cli -i input.mp4 -m medium -lang en --mode twoword

# Full help
oneword-cli --help
```

---

## ☁️ VPS / Server Deployment

### Method 1: Docker (Recommended)

1. **Build the image**:
   ```bash
   docker build -t oneword-ai .
   ```

2. **Run container**:
   ```bash
   docker run -d -p 8000:8000 oneword-ai
   ```

### Method 2: Systemd (Linux Servers)

Run as a background service on Ubuntu/Debian:

1. Create service file: `sudo nano /etc/systemd/system/oneword.service`
   ```ini
   [Unit]
   Description=OneWord AI Web Server
   After=network.target

   [Service]
   User=root
   WorkingDirectory=/root/oneword-ai
   ExecStart=/usr/local/bin/oneword-web
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

2. Start service:
   ```bash
   sudo systemctl enable oneword
   sudo systemctl start oneword
   ```

---

## 📦 Models

Models are downloaded to `~/.cache/huggingface` (or generic cache) on the first run.

| Model | Size | Best For |
|-------|------|----------|
| **medium** | ~1.5GB | General Purpose (Default) |
| **large** | ~3GB | High Accuracy |
| **Hindi2Hinglish** | ~1.5GB | Hindi to Hinglish Transcription |

---

## 📜 License

MIT License. Free for commercial use.