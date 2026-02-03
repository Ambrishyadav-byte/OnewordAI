# 🎬 OneWord AI Sublic

<div align="center">

**Enterprise-Grade Visual Subtitle Generator**
*Create viral-style one-word subtitles locally. No cloud, no fees, total privacy.*

[![PyPI Version](https://img.shields.io/pypi/v/oneword-ai)](https://pypi.org/project/oneword-ai/)
[![ARM Support](https://img.shields.io/badge/ARM-Ready-green)](ARM_SETUP.md)
[![License](https://img.shields.io/badge/License-MIT-blue)](license.txt)

</div>

---

## 🚀 Choose Your Path

We provide two dedicated packages to ensure maximum performance on every platform.

| Platform | Package Name | Description |
|----------|--------------|-------------|
| **Android / Termux** | `oneword-ai-arm` | Ultralight (Whisper.cpp only). No PyTorch bloat. |
| **PC / Server** | `oneword-ai` | Full Power (PyTorch + Whisper + Whisper.cpp). |

---

## 📱 Android / Termux Installation

Run these commands in Termux:

```bash
# 1. Install System Dependencies
pkg install python git clang make ffmpeg

# 2. Install the Lightweight Package
pip install oneword-ai-arm

# 3. Setup (One-time)
oneword-setup-arm
```

### Usage on Phone
*   **Web UI:** Run `oneword-web-arm` and open `http://localhost:8000`
*   **CLI:** Run `oneword-process-arm -i video.mp4`

---

## 💻 PC Installation (Windows / Mac / Linux)

For standard desktop environments:

```bash
# Install Video Processor
# (Ensure ffmpeg is installed on your system)
pip install oneword-ai
```

### Usage on PC
*   **Web UI:** Run `oneword-web` and open `http://localhost:8000`
*   **CLI:** Run `oneword-cli -i video.mp4`

---

## 🎨 Features
*   **Local Processing:** 100% privacy, no file limits.
*   **3 Modes:** One Word, Two Word (Punch), Phrase.
*   **Multi-Language:** English, Hindi, Urdu, Spanish, and more.
*   **Optimized:** Dedicated engine for ARM devices using `whisper.cpp`.

## 📜 License
MIT License. Free for commercial use.