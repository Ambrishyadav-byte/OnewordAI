"""
CLI interface for OneWord AI Subtitle Generator.
"""
import argparse
from pathlib import Path
from .core.engine import SubtitleGenerator


def main():
    parser = argparse.ArgumentParser(
        description="OneWord AI - Generate cinematic one-word subtitles using Whisper"
    )
    parser.add_argument(
        "-i", "--input", 
        required=True, 
        help="Path to input video/audio file"
    )
    parser.add_argument(
        "-m", "--model", 
        default="medium",
        choices=["medium", "large", "Oriserve/Whisper-Hindi2Hinglish-Prime"],        help="Whisper model to use (default: medium)"
    )
    parser.add_argument(
        "-lang", "--language",
        default=None,
        choices=["hi", "en", "ur", "es"],
        help="Language code (hi=Hindi, en=English, ur=Urdu, es=Spanish). Auto-detect if not specified."
    )
    parser.add_argument(
        "-mode", "--mode",
        default="oneword",
        choices=["oneword", "twoword", "phrase"],
        help="Subtitle mode: oneword (default), twoword (punch effect), phrase (full segment)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output SRT file path (optional, auto-generated if not specified)"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: Input file '{args.input}' not found.")
        return 1
    
    # Create generator
    generator = SubtitleGenerator(model_name=args.model)
    
    # Process
    try:
        output_file = generator.process(
            input_path=str(input_path),
            output_path=args.output,
            language=args.language,
            mode=args.mode
        )
        print(f"\n🎉 Done! SRT file: {output_file}")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
