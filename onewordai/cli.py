"""
CLI interface for OneWord AI Subtitle Generator.
"""
import argparse
import subprocess
import sys
from pathlib import Path
from pathlib import Path


def setup_arm():
    """Install whisper.cpp for ARM devices."""
    from onewordai.arm import ARM_DIR, is_whisper_cpp_installed
    
    if is_whisper_cpp_installed():
        print("✅ Whisper.cpp is already installed!")
        return 0
    
    print("🚀 Installing whisper.cpp for ARM devices...")
    print("This may take a few minutes...\n")
    
    setup_script = ARM_DIR / "setup.sh"
    
    try:
        subprocess.run(["bash", str(setup_script)], check=True)
        print("\n✅ Setup complete!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Setup failed: {e}")
        return 1
    except FileNotFoundError:
        print("❌ Error: bash not found. Are you on a Unix-like system?")
        return 1


def process_arm():
    """Process audio/video on ARM devices using whisper.cpp."""
    from onewordai.arm import is_whisper_cpp_installed, is_model_downloaded
    from onewordai.core.engine_cpp import WhisperCppEngine
    
    parser = argparse.ArgumentParser(
        description="OneWord AI - ARM/Termux version using whisper.cpp"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to input video/audio file"
    )
    parser.add_argument(
        "-m", "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model to use (default: base)"
    )
    parser.add_argument(
        "-lang", "--language",
        default=None,
        help="Language code (hi=Hindi, en=English, etc.)"
    )
    parser.add_argument(
        "-mode", "--mode",
        default="oneword",
        choices=["oneword", "twoword", "phrase"],
        help="Subtitle mode: oneword (default), twoword, phrase"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output SRT file path (optional)"
    )
    
    args = parser.parse_args(sys.argv[2:])  # Skip 'process-arm'
    
    # Check if whisper.cpp is installed
    if not is_whisper_cpp_installed():
        print("❌ Whisper.cpp not installed!")
        print("\nRun this command to install:")
        print("  onewordai setup-arm")
        return 1
    
    # Check if model is downloaded
    if not is_model_downloaded(args.model):
        print(f"❌ Model '{args.model}' not found!")
        print(f"\nDownload it with:")
        print(f"  cd onewordai/arm/whisper.cpp")
        print(f"  bash ./models/download-ggml-model.sh {args.model}")
        return 1
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: Input file '{args.input}' not found.")
        return 1
    
    # Create engine
    engine = WhisperCppEngine(model_name=args.model)
    
    # Process
    try:
        print(f"🎬 Processing: {input_path.name}")
        print(f"📦 Model: {args.model}")
        print(f"🌍 Language: {args.language or 'auto'}")
        print(f"🎯 Mode: {args.mode}\n")
        
        engine.load_model(status_callback=print)
        
        srt_content = engine.generate_subtitles(
            audio_path=str(input_path),
            language=args.language,
            mode=args.mode
        )
        
        # Save SRT
        if args.output:
            output_file = Path(args.output)
        else:
            output_file = input_path.with_suffix('.srt')
        
        output_file.write_text(srt_content, encoding='utf-8')
        
        print(f"\n🎉 Done! SRT file: {output_file}")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


def web_arm():
    """Start the ARM Web UI."""
    from onewordai.arm import is_whisper_cpp_installed
    
    if not is_whisper_cpp_installed():
        print("❌ Whisper.cpp not installed!")
        print("Run: onewordai-setup-arm")
        return 1
        
    from onewordai.arm.web import start_server
    start_server()


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
        choices=["medium", "large", "Oriserve/Whisper-Hindi2Hinglish-Prime"],
        help="Whisper model to use (default: medium)"
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
    from .core.engine import SubtitleGenerator
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
