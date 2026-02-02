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
        """Load the Whisper model (OpenAI or Hugging Face)."""
        if self.model is None:
            if "OriserveAI" in self.model_name or "/" in self.model_name:
                print(f"📦 Loading Hugging Face model: {self.model_name}...")
                from transformers import pipeline
                import torch
                
                device = "cuda" if torch.cuda.is_available() else "cpu"
                self.model = pipeline(
                    "automatic-speech-recognition",
                    model=self.model_name,
                    device=device
                )
                self.model_type = "huggingface"
            else:
                print(f"📦 Loading OpenAI Whisper model: {self.model_name}...")
                self.model = whisper.load_model(self.model_name)
                self.model_type = "openai"
    
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
        """
        self.load_model()
        
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
