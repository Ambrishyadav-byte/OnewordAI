# 💻 OneWord AI - CLI Reference

After installing the package (`pip install -e .`), you can use the `oneword-cli` command from anywhere in your terminal.

## 🚀 Basic Syntax

```bash
oneword-cli -i <input_file> [options]
```

## 🛠️ Command Arguments

| Flag | Long Flag | Description | Choices | Default |
|------|-----------|-------------|---------|---------|
| `-i` | `--input` | **(Required)** Path to input video or audio file. | Any valid path | N/A |
| `-m` | `--model` | Whisper model size. Larger = slower but more accurate. | `medium`, `large` | `medium` |
| `-lang`| `--language`| Spoken language in the audio. | `hi` (Hindi), `en` (English), `ur` (Urdu), `es` (Spanish), `auto` | `auto` |
| `-mode`| `--mode` | Subtitle style/chunking. | `oneword` (1 word), `twoword` (2 words), `phrase` (sentence) | `oneword` |
| `-o` | `--output` | Custom path for the generated SRT file. | Any path | `<input_name>_<mode>_subs.srt` |

---

## 💡 Examples

### 1. High-Quality Hindi Voiceover
Use the `medium` or `large` model for better accuracy.
```bash
oneword-cli -i vlog.mp4 -lang hi -m medium
```

### 3. "Punchy" 2-Word Subtitles
Great for retention-focused editing (like Alex Hormozi style).
```bash
oneword-cli -i podcast_clip.mp4 -mode twoword
```

### 4. Traditional Subtitles (Full Sentences)
If you want standard captions instead of the one-word style.
```bash
oneword-cli -i movie_scene.mkv -mode phrase
```

### 5. Custom Output Location
Save the subtitle file to a specific folder.
```bash
oneword-cli -i footage/raw.mov -o subtitles/final.srt
```

---

## ❓ Troubleshooting

**"Command not found" error?**
Make sure you have installed the package locally:
```bash
pip install -e .
```

**"No module named transformers"?**
You might need to reinstall dependencies if using the new model:
```bash
pip install -r requirements.txt
```
