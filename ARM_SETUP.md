# ARM Device Support

OneWordAI now supports ARM devices (Android/Termux) using whisper.cpp!

## Installation on Termux/ARM

### 1. Install Python and pip
```bash
pkg update
pkg install python
```

### 2. Install OneWordAI ARM
```bash
pip install oneword-ai-arm
```

### 3. Setup Whisper.cpp (One-time)
```bash
onewordai-setup-arm
```

## Web UI Usage (New!)

To run the Web Interface on your phone:
```bash
onewordai-web-arm
```
Then open `http://localhost:8000` in your browser.

## CLI Usage on ARM Devices

### Basic Usage
```bash
onewordai-process-arm -i video.mp4
```

### With Options
```bash
onewordai-process-arm -i video.mp4 -m base -lang hi -mode oneword -o output.srt
```

### Parameters
- `-i, --input`: Input video/audio file (required)
- `-m, --model`: Model size (tiny, base, small, medium, large) - default: base
- `-lang, --language`: Language code (hi, en, es, etc.) - default: auto
- `-mode, --mode`: Subtitle mode (oneword, twoword, phrase) - default: oneword
-`-o, --output`: Output SRT file path (optional)

## Download Additional Models

```bash
cd onewordai/arm/whisper.cpp
bash ./models/download-ggml-model.sh tiny
bash ./models/download-ggml-model.sh small
bash ./models/download-ggml-model.sh medium
```

## Model Sizes

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| tiny  | ~75MB | Fastest | Basic |
| base  | ~142MB | Fast | Good ⭐ |
| small | ~466MB | Medium | Better |
| medium | ~1.5GB | Slow | Best |
| large | ~2.9GB | Slowest | Premium |

**Recommended:** Use `base` for best balance on mobile devices.

## Comparison: PyTorch vs Whisper.cpp

| Feature | PyTorch (Desktop) | Whisper.cpp (ARM) |
|---------|------------------|-------------------|
| Platform | Windows/Mac/Linux | Android/Termux/ARM |
| Dependency | Requires PyTorch | No PyTorch needed |
| Speed | Fast (GPU) | Medium (CPU) |
| Memory | High | Low |
| Models | All Hugging Face | GGML format only |
| Command | `oneword-cli` | `onewordai-process-arm` |

## Troubleshooting

### Setup fails
```bash
# Make sure you have bash
pkg install bash

# Re-run setup
onewordai-setup-arm
```

### Model not found
```bash
# Download the model manually
cd onewordai/arm/whisper.cpp
bash ./models/download-ggml-model.sh base
```

### Permission denied
```bash
# Make setup script executable
chmod +x onewordai/arm/setup.sh
```

## Performance Tips

1. **Use smaller models** on older devices (tiny/base)
2. **Close other apps** to free memory
3. **Process shorter clips** if memory is limited
4. **Use base model** - best balance for mobile

## Examples

```bash
# Quick transcription (auto-detect language)
onewordai-process-arm -i video.mp4

# Hindi transcription
onewordai-process-arm -i video.mp4 -lang hi -m base

# English with two-word mode
onewordai-process-arm -i audio.mp3 -lang en -mode twoword -m small

# Custom output path
onewordai-process-arm -i vid.mp4 -o ~/subs/output.srt
```

Enjoy OneWordAI on your Android device! 🚀📱
