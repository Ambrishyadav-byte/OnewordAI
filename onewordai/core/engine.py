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
    
    def __init__(self, model_name: str = "medium"):
        """
        Initialize the subtitle generator.
        
        Args:
            model_name: Whisper model to use (tiny, base, small, medium, large)
        """
        self.model_name = model_name
        self.model = None
        # Prevent CPU overload
        torch.set_num_threads(4)
    
    def load_model(self, status_callback=None):
        """Load the Whisper model (OpenAI or Hugging Face)."""
        if self.model is None:
            if "Oriserve" in self.model_name or "/" in self.model_name:
                print(f"📦 Loading Hugging Face model: {self.model_name}...")
                from transformers import pipeline
                import torch
                import os
                from tqdm.auto import tqdm as tqdm_auto
                
                # Set up custom tqdm callback to capture download progress
                original_tqdm = tqdm_auto
                
                class ProgressCapture(original_tqdm):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, **kwargs)
                        
                    def display(self, msg=None, pos=None, *args, **kwargs):
                        super().display(msg, pos, *args, **kwargs)
                        # Capture progress for status callback
                        if status_callback and self.total:
                            downloaded = self.n
                            total = self.total
                            rate = self.format_dict.get('rate', 0) or 0
                            elapsed = self.format_dict.get('elapsed', 0) or 0
                            
                            # Format like: "68.5M/6.17G [01:29<2:06:23, 805kB/s]"
                            downloaded_str = self.format_sizeof(downloaded, 'B', 1024)
                            total_str = self.format_sizeof(total, 'B', 1024)
                            rate_str = self.format_sizeof(rate, 'B/s', 1024) if rate else "0B/s"
                            
                            elapsed_str = self.format_interval(elapsed)
                            
                            # Calculate remaining time
                            if rate > 0:
                                remaining = (total - downloaded) / rate
                                remaining_str = self.format_interval(remaining)
                            else:
                                remaining_str = "??:??"
                            
                            progress_msg = f"📦 Downloading: {downloaded_str}/{total_str} [{elapsed_str}<{remaining_str}, {rate_str}]"
                            status_callback(progress_msg)
                
                # Monkey-patch tqdm for this model load
                import tqdm.auto
                original_tqdm_ref = tqdm.auto.tqdm
                tqdm.auto.tqdm = ProgressCapture
                
                try:
                    if status_callback:
                        status_callback("📦 Checking model files... (Download starting if needed)")
                    
                    device = "cuda" if torch.cuda.is_available() else "cpu"
                    self.model = pipeline(
                        "automatic-speech-recognition",
                        model=self.model_name,
                        device=device
                    )
                    self.model_type = "huggingface"
                finally:
                    # Restore original tqdm
                    tqdm.auto.tqdm = original_tqdm_ref
                    
            else:
                if status_callback:
                    size_estimate = "~1.5GB" if "medium" in self.model_name else "~3GB"
                    status_callback(f"📦 Downloading Model ({size_estimate}, 5-15 min) - One-time only!")
                    
                print(f"📦 Loading OpenAI Whisper model: {self.model_name}...")
                self.model = whisper.load_model(self.model_name)
                self.model_type = "openai"
                
            if status_callback:
                status_callback("✅ Model Ready! Transcribing...")

    def transcribe(
        self, 
        file_path: str, 
        language: Optional[str] = None,
        progress_callback=None,
        status_callback=None
    ) -> dict:
        """
        Transcribe audio/video file.
        Args:
            file_path: Path to audio/video file
            language: Language code (hi, en, ur, es) or None for auto-detect
            progress_callback: Optional callback function for progress updates
            status_callback: Optional callback for status text updates
        """
        self.load_model(status_callback)
        
        print(f"🎵 Reading audio...")
        audio = load_audio(str(file_path))
        audio_duration = len(audio) / 16000
        print(f"⏱ Audio Duration: {audio_duration:.2f} seconds")
        
        print(f"\n🧠 Transcribing started ({self.model_type})...\n")
        
        # Threaded transcription to support progress callback
        if progress_callback:
            import threading
            import time
            
            result_container = {}
            exception_container = {}
            
            # Transcription function wrapper
            def transcribe_task():
                try:
                    if self.model_type == "huggingface":
                        # Hugging Face Pipeline
                        generate_kwargs = {"language": language} if language else {}
                        # For Hindi2Hinglish, language might need to be 'hi' or auto
                        
                        out = self.model(
                            str(file_path), 
                            return_timestamps="word",
                            generate_kwargs=generate_kwargs
                        )
                        
                        # Normalize output to match OpenAI structure
                        # Transformers returns: {'text': '...', 'chunks': [{'text': ' word', 'timestamp': (start, end)}, ...]}
                        chunks = out.get("chunks", [])
                        words = []
                        for chunk in chunks:
                             # Timestamp is a tuple (start, end)
                             ts = chunk.get("timestamp")
                             if ts:
                                 start, end = ts
                                 words.append({
                                     "word": chunk["text"].strip(),
                                     "start": start,
                                     "end": end
                                 })
                        
                        # Create a single segment with all words
                        segment = {
                            "text": out["text"],
                            "start": words[0]["start"] if words else 0,
                            "end": words[-1]["end"] if words else 0,
                            "words": words
                        }
                        
                        result_container['result'] = {
                            "text": out["text"],
                            "segments": [segment]
                        }
                        
                    else:
                        # OpenAI Whisper
                        transcribe_options = {"word_timestamps": True, "verbose": False}
                        if language:
                            transcribe_options["language"] = language
                            
                        result_container['result'] = self.model.transcribe(str(file_path), **transcribe_options)
                        
                except Exception as e:
                    exception_container['error'] = e
            
            # Start background thread
            thread = threading.Thread(target=transcribe_task)
            thread.start()
            
            # Simulate progress
            # Estimate speed: HF models can be slower or faster depending on implementation
            # Generic estimate logic
            speed_mult = 4.0 if self.model_type == "huggingface" else 1.5
            if self.model_name in ['tiny', 'base']: speed_mult = 1.0
            
            estimated_time = audio_duration * speed_mult
            
            start_time = time.time()
            while thread.is_alive():
                elapsed = time.time() - start_time
                progress = min(95, (elapsed / estimated_time) * 100)
                progress_callback(progress)
                time.sleep(0.5)
            
            thread.join()
            
            if 'error' in exception_container:
                raise exception_container['error']
            
            progress_callback(100)
            return result_container['result']
            
        else:
            # Sync execution (CLI usage mostly)
            if self.model_type == "huggingface":
                out = self.model(str(file_path), return_timestamps="word")
                chunks = out.get("chunks", [])
                words = []
                for chunk in chunks:
                        ts = chunk.get("timestamp")
                        if ts:
                            words.append({
                                "word": chunk["text"].strip(),
                                "start": ts[0],
                                "end": ts[1]
                            })
                return {
                    "text": out["text"],
                    "segments": [{
                        "text": out["text"],
                        "start": words[0]["start"] if words else 0,
                        "end": words[-1]["end"] if words else 0,
                        "words": words
                    }]
                }
            else:
                transcribe_options = {"word_timestamps": True, "verbose": False}
                if language:
                    transcribe_options["language"] = language
                return self.model.transcribe(str(file_path), **transcribe_options)

    # ... (format_timestamp and generate_srt remain unchanged) ...

    def process(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        language: Optional[str] = None,
        mode: SubtitleMode = "oneword",
        progress_callback=None,
        status_callback=None
    ) -> str:
        """
        Full processing pipeline: transcribe and generate SRT.
        
        Args:
            input_path: Path to input video/audio
            output_path: Path for output SRT (auto-generated if None)
            language: Language code or None for auto-detect
            mode: Subtitle mode
            progress_callback: Optional progress callback
            status_callback: Optional callback for status text updates
            
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
        result = self.transcribe(input_path, language, progress_callback, status_callback)
        
        # Generate SRT
        self.generate_srt(result, str(output_path), mode)
        
        return str(output_path)
    
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
    

