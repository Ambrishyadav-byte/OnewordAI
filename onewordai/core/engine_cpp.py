"""
Whisper.cpp engine wrapper for ARM devices.
Provides PyTorch-compatible interface using whisper.cpp backend.
"""
import json
import subprocess
from pathlib import Path
from typing import Optional, Literal, List, Dict, Any
import tempfile
import os

from onewordai.arm import (
    WHISPER_CPP_DIR,
    get_model_path,
    is_model_downloaded,
    is_whisper_cpp_installed,
)

SubtitleMode = Literal["oneword", "twoword", "phrase"]


class WhisperCppEngine:
    """Whisper.cpp engine for ARM devices (Android/Termux)."""

    def __init__(self, model_name: str = "base"):
        """
        Initialize the Whisper.cpp engine.

        Args:
            model_name: Model to use (tiny, base, small, medium, large)
        """
        self.model_name = model_name
        self.model_path = get_model_path(model_name)
        self.whisper_binary = WHISPER_CPP_DIR / "main"

    def load_model(self, status_callback=None):
        """Verify model is ready to use."""
        if not is_whisper_cpp_installed():
            raise RuntimeError(
                "Whisper.cpp is not installed. Please run: bash onewordai/arm/setup.sh"
            )

        if not is_model_downloaded(self.model_name):
            raise RuntimeError(
                f"Model '{self.model_name}' not found. Please download it first."
            )

        if status_callback:
            status_callback(f"Loaded model: {self.model_name}")

    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        task: str = "transcribe",
    ) -> Dict[str, Any]:
        """
        Transcribe audio using whisper.cpp.

        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'en', 'hi')
            task: Task type (transcribe or translate)

        Returns:
            Dictionary with 'text' and 'chunks' (word-level timestamps)
        """
        # Prepare command
        cmd = [
            str(self.whisper_binary),
            "-m", str(self.model_path),
            "-f", str(audio_path),
            "--output-json",
            "-ml", "1",  # Max line length
        ]

        # Add language if specified
        if language and language != "auto":
            cmd.extend(["-l", language])

        # Run whisper.cpp
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=str(WHISPER_CPP_DIR),
            )

            # Parse JSON output
            # whisper.cpp saves to <audio-name>.json
            audio_name = Path(audio_path).stem
            json_output = WHISPER_CPP_DIR / f"{audio_name}.json"

            if json_output.exists():
                with open(json_output, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Clean up JSON file
                json_output.unlink()

                return self._parse_whisper_output(data)
            else:
                # Fallback: parse from stdout
                return self._parse_text_output(result.stdout)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Whisper.cpp error: {e.stderr}")

    def _parse_whisper_output(self, data: Dict) -> Dict[str, Any]:
        """
        Parse whisper.cpp JSON output to match PyTorch format.

        Args:
            data: Raw whisper.cpp JSON output

        Returns:
            Dictionary with 'text' and 'chunks' compatible with PyTorch output
        """
        transcription = data.get("transcription", [])
        
        chunks = []
        full_text = ""

        for segment in transcription:
            timestamps = segment.get("timestamps", {})
            text = segment.get("text", "").strip()
            
            if text:
                full_text += text + " "
                
                # Create chunk with timestamp
                chunk = {
                    "text": text,
                    "timestamp": [
                        timestamps.get("from", 0) / 1000.0,  # Convert ms to seconds
                        timestamps.get("to", 0) / 1000.0,
                    ],
                }
                chunks.append(chunk)

        return {
            "text": full_text.strip(),
            "chunks": chunks,
        }

    def _parse_text_output(self, output: str) -> Dict[str, Any]:
        """
        Fallback parser for text output (when JSON not available).

        Args:
            output: Raw text output from whisper.cpp

        Returns:
            Dictionary with 'text' and estimated 'chunks'
        """
        # Simple fallback - just return text with basic chunks
        lines = [line.strip() for line in output.split("\n") if line.strip()]
        
        chunks = []
        current_time = 0.0
        
        for line in lines:
            # Skip metadata lines
            if line.startswith("[") or not line:
                continue
                
            # Estimate duration based on word count
            words = line.split()
            duration = len(words) * 0.5  # ~0.5 seconds per word
            
            chunk = {
                "text": line,
                "timestamp": [current_time, current_time + duration],
            }
            chunks.append(chunk)
            current_time += duration

        return {
            "text": " ".join([c["text"] for c in chunks]),
            "chunks": chunks,
        }

    def generate_subtitles(
        self,
        audio_path: str,
        language: Optional[str] = None,
        mode: SubtitleMode = "oneword",
    ) -> str:
        """
        Generate SRT subtitles from audio.

        Args:
            audio_path: Path to audio/video file
            language: Language code
            mode: Subtitle mode (oneword, twoword, phrase)

        Returns:
            SRT formatted subtitle string
        """
        from onewordai.core.srt_generator import generate_srt

        # Transcribe
        result = self.transcribe(audio_path, language)

        # Generate SRT using shared logic
        return generate_srt(result, mode)
