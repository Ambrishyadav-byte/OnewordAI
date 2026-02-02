import whisper
import datetime
import argparse
from pathlib import Path
from whisper.audio import load_audio
import torch

def format_timestamp(seconds: float):
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def process_subtitles(input_path, model_type, output_dir):
    video_path = Path(input_path)
    if not video_path.exists():
        print(f"❌ Error: File {input_path} not found.")
        return

    # Output location
    save_dir = Path(output_dir) if output_dir else video_path.parent
    save_dir.mkdir(parents=True, exist_ok=True)
    output_filename = save_dir / f"{video_path.stem}_subs.srt"

    # Prevent CPU overload
    torch.set_num_threads(4)

    print(f"\n📦 Loading Whisper model: {model_type} ...")
    model = whisper.load_model(model_type)

    print(f"🎵 Reading audio...")
    audio = load_audio(str(video_path))
    audio_duration = len(audio) / 16000
    print(f"⏱ Audio Duration: {audio_duration:.2f} seconds")

    print(f"\n🧠 Transcribing started...\n")

    # Run transcription
    result = model.transcribe(
        str(video_path),
        word_timestamps=True,
        verbose=False
    )

    # Progress display
    last_percent = 0
    for segment in result["segments"]:
        processed_time = segment["end"]
        percent = (processed_time / audio_duration) * 100
        if percent - last_percent >= 5:  # update every 5%
            print(f"Progress: {percent:.1f}%")
            last_percent = percent

    print("Progress: 100.0% ✅\n")

    # Write SRT
    print("✍ Writing subtitles...")
    with open(output_filename, "w", encoding="utf-8") as f:
        counter = 1
        for segment in result["segments"]:
            for word_data in segment["words"]:
                word = word_data["word"].strip().replace(",", "")
                if not word:
                    continue

                start = word_data["start"]
                end = word_data["end"]

                f.write(f"{counter}\n")
                f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
                f.write(f"{word}\n\n")
                counter += 1

    print(f"\n✅ Success! Subtitles saved to: {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate minimalist one-word SRT subtitles.")
    parser.add_argument("-i", "--input", required=True, help="Path to input video/audio file")
    parser.add_argument("-m", "--model", default="base", help="Model: tiny, base, small, medium, large")
    parser.add_argument("-o", "--output", help="Output directory (optional)")

    args = parser.parse_args()
    process_subtitles(args.input, args.model, args.output)
