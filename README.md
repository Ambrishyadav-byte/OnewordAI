# 🎬 OneWord AI

<div align="center">

**Enterprise-Grade Visual Subtitle Generator**
*Create viral-style one-word subtitles locally. No cloud, no fees, total privacy.*

[![PyPI Version](https://img.shields.io/pypi/v/oneword-ai)](https://pypi.org/project/oneword-ai/)
[![License](https://img.shields.io/badge/License-MIT-blue)](license.txt)

</div>

---

## 🚀 Overview

OneWord AI is a professional tool designed to create cinematic, high-retention subtitles for your videos. It runs entirely locally on your machine, ensuring maximum privacy and zero recurring costs.

---

## 📦 Installation

```bash
pip install oneword-ai
```

*(Requires Python 3.9+ and ffmpeg installed on your system)*

---

## 🚀 Usage

### Command Line Interface (CLI)

```bash
oneword-cli -i input.mp4 -mode oneword
```

### Options
*   `-i, --input`: Path to video/audio file (Required)
*   `-mode`: Subtitle style (`oneword`, `twoword`, `phrase`)
*   `-m, --model`: Whisper model (`base`, `small`, `medium`, `large`)
*   `-lang`: Language code (`en`, `hi`, etc.)

---

## 🌐 Web Interface

Launch the modern web dashboard:

```bash
oneword-web
```

Open `http://localhost:8000` in your browser.

---

## 🎨 Features
*   **Local Processing:** 100% privacy, no file limits.
*   **3 Modes:** One Word, Two Word (Punch), Phrase.
*   **Multi-Language:** Support for 99+ languages via Whisper.
*   **High Performance:** Optimized PyTorch engine.

## 📜 License
MIT License. Free for commercial use.