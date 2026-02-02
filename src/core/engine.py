"""
Core subtitle generation engine using Whisper.
Supports multiple subtitle modes and language detection.
"""
import whisper
import datetime
import torch
from pathlib import Path
from whisper.audio import load_audio
from typing import Optional, Literal

SubtitleMode = Literal["oneword", "twoword", "phrase"]


class SubtitleGenerator:
    """Generate SRT subtitles from video/audio using Whisper."""
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize the subtitle generator.
        
        Args:
            model_name: Whisper model to use (tiny, base, small, medium, large)
        """
        self.model_name = model_name
        self.model = None
        # Prevent CPU overload
        torch.set_num_threads(4)
    
    def load_model(self):
        """Load the Whisper model."""
        if self.model is None:
            print(f"📦 Loading Whisper model: {self.model_name}...")
            self.model = whisper.load_model(self.model_name)
    
    def transcribe(
        self, 
        file_path: str, 
        language: Optional[str] = None,
        progress_callback=None
    ) -> dict:
        """
        Transcribe audio/video file.
        
        Args:
            file_path: Path to audio/video file
            language: Language code (hi, en, ur, es) or None for auto-detect
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Whisper transcription result with word timestamps
        """
        self.load_model()
        
        print(f"🎵 Reading audio...")
        audio = load_audio(str(file_path))
        audio_duration = len(audio) / 16000
        print(f"⏱ Audio Duration: {audio_duration:.2f} seconds")
        
        print(f"\n🧠 Transcribing started...\n")
        
        # Transcribe with word timestamps
        transcribe_options = {
            "word_timestamps": True,
            "verbose": False
        }
        
        if language:
            transcribe_options["language"] = language
        
        # If we have a progress callback, run transcription in thread and simulate progress
        if progress_callback:
            import threading
            import time
            
            result_container = {}
            exception_container = {}
            
            def transcribe_thread():
                try:
                    result_container['result'] = self.model.transcribe(str(file_path), **transcribe_options)
                except Exception as e:
                    exception_container['error'] = e
            
            # Start transcription in background thread
            thread = threading.Thread(target=transcribe_thread)
            thread.start()
            
            # Simulate progress while transcription runs
            # Estimate: base model ~1x realtime, small ~3x, medium ~5x, large ~8x
            model_speed_multipliers = {
                'tiny': 0.5,
                'base': 1.0,
                'small': 2.5,
                'medium': 4.0,
                'large': 6.0
            }
            estimated_time = audio_duration * model_speed_multipliers.get(self.model_name, 1.5)
            
            start_time = time.time()
            while thread.is_alive():
                elapsed = time.time() - start_time
                # Progress from 0-95% based on estimated time
                progress = min(95, (elapsed / estimated_time) * 100)
                progress_callback(progress)
                time.sleep(0.5)
            
            # Wait for thread to complete
            thread.join()
            
            # Check for errors
            if 'error' in exception_container:
                raise exception_container['error']
            
            # Set to 100% when done
            progress_callback(100)
            result = result_container['result']
        else:
            # No callback, just run normally
            result = self.model.transcribe(str(file_path), **transcribe_options)
            
            # Console progress display
            last_percent = 0
            for segment in result["segments"]:
                processed_time = segment["end"]
                percent = (processed_time / audio_duration) * 100
                if percent - last_percent >= 5:
                    print(f"Progress: {percent:.1f}%")
                    last_percent = percent
            print("Progress: 100.0% ✅\n")
        
        return result
    
    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """Convert seconds to SRT timestamp format."""
        td = datetime.timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        millis = int(td.microseconds / 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def generate_srt(
        self, 
        result: dict, 
        output_path: str,
        mode: SubtitleMode = "oneword"
    ):
        """
        Generate SRT file from transcription result.
        
        Args:
            result: Whisper transcription result
            output_path: Path to save SRT file
            mode: Subtitle mode - oneword, twoword, or phrase
        """
        print("✍ Writing subtitles...")
        
        with open(output_path, "w", encoding="utf-8") as f:
            counter = 1
            
            if mode == "oneword":
                # One word per subtitle
                for segment in result["segments"]:
                    for word_data in segment["words"]:
                        word = word_data["word"].strip().replace(",", "")
                        if not word:
                            continue
                        
                        start = word_data["start"]
                        end = word_data["end"]
                        
                        f.write(f"{counter}\n")
                        f.write(f"{self.format_timestamp(start)} --> {self.format_timestamp(end)}\n")
                        f.write(f"{word}\n\n")
                        counter += 1
            
            elif mode == "twoword":
                # Two words per subtitle (punch effect)
                for segment in result["segments"]:
                    words = segment["words"]
                    i = 0
                    while i < len(words):
                        # Get up to 2 words
                        word_group = words[i:i+2]
                        text = " ".join([w["word"].strip().replace(",", "") for w in word_group if w["word"].strip()])
                        
                        if not text:
                            i += 2
                            continue
                        
                        start = word_group[0]["start"]
                        end = word_group[-1]["end"]
                        
                        f.write(f"{counter}\n")
                        f.write(f"{self.format_timestamp(start)} --> {self.format_timestamp(end)}\n")
                        f.write(f"{text}\n\n")
                        counter += 1
                        i += 2
            
            elif mode == "phrase":
                # Full segment text (phrase mode)
                for segment in result["segments"]:
                    text = segment["text"].strip()
                    if not text:
                        continue
                    
                    start = segment["start"]
                    end = segment["end"]
                    
                    f.write(f"{counter}\n")
                    f.write(f"{self.format_timestamp(start)} --> {self.format_timestamp(end)}\n")
                    f.write(f"{text}\n\n")
                    counter += 1
        
        print(f"✅ Success! Subtitles saved to: {output_path}")
    
    def process(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        language: Optional[str] = None,
        mode: SubtitleMode = "oneword",
        progress_callback=None
    ) -> str:
        """
        Full processing pipeline: transcribe and generate SRT.
        
        Args:
            input_path: Path to input video/audio
            output_path: Path for output SRT (auto-generated if None)
            language: Language code or None for auto-detect
            mode: Subtitle mode
            progress_callback: Optional progress callback
            
        Returns:
            Path to generated SRT file
        """
        video_path = Path(input_path)
        if not video_path.exists():
            raise FileNotFoundError(f"File {input_path} not found")
        
        # Auto-generate output path
        if output_path is None:
            output_path = video_path.parent / f"{video_path.stem}_{mode}_subs.srt"
        
        # Transcribe
        result = self.transcribe(input_path, language, progress_callback)
        
        # Generate SRT
        self.generate_srt(result, output_path, mode)
        
        return str(output_path)
