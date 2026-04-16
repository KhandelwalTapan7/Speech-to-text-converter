import torch
import logging
import os
import numpy as np
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhisperModel:
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WhisperModel, cls).__new__(cls)
        return cls._instance
    
    def setup_ffmpeg_path(self):
        """Add FFmpeg to PATH if found locally"""
        # Check for local FFmpeg installation
        local_ffmpeg_paths = [
            r"E:\speech-to-text-app\tools\ffmpeg\bin",
            r"C:\ffmpeg\bin",
            r"C:\Program Files\FFmpeg\bin",
        ]
        
        for path in local_ffmpeg_paths:
            if os.path.exists(path):
                os.environ['PATH'] = path + os.pathsep + os.environ.get('PATH', '')
                logger.info(f"Added FFmpeg path: {path}")
                return True
        
        # Check if ffmpeg is in PATH
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("FFmpeg found in system PATH")
                return True
        except:
            pass
        
        logger.warning("FFmpeg not found! Transcription may fail.")
        return False
    
    def load_model(self, model_size="base"):
        if self._model is None:
            logger.info(f"Loading Whisper {model_size} model...")
            try:
                # Setup FFmpeg path first
                self.setup_ffmpeg_path()
                
                import whisper
                device = "cuda" if torch.cuda.is_available() else "cpu"
                logger.info(f"Using device: {device}")
                self._model = whisper.load_model(model_size, device=device)
                logger.info(f"Model loaded successfully on {device}")
            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                raise
        return self._model
    
    def transcribe(self, audio_path, language=None):
        temp_wav = None
        
        try:
            import librosa
            import soundfile as sf
            
            logger.info(f"Loading audio with librosa: {audio_path}")
            
            # Check if file exists
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            # Load audio using librosa
            try:
                audio, sr = librosa.load(audio_path, sr=16000, mono=True)
                logger.info(f"Audio loaded: {len(audio)} samples, {sr} Hz")
            except Exception as e:
                logger.warning(f"Librosa load failed: {e}")
                # Try alternative loading method
                try:
                    import audioread
                    with audioread.audio_open(audio_path) as f:
                        sr = f.samplerate
                        audio_data = []
                        for buf in f:
                            audio_data.append(np.frombuffer(buf, dtype=np.int16))
                        audio = np.concatenate(audio_data)
                        audio = audio.astype(np.float32) / 32768.0
                        # Resample if needed
                        if sr != 16000:
                            import scipy.signal
                            audio = scipy.signal.resample(audio, int(len(audio) * 16000 / sr))
                            sr = 16000
                    logger.info(f"Audio loaded with audioread: {len(audio)} samples")
                except Exception as e2:
                    logger.error(f"All loading methods failed: {e2}")
                    raise
            
            # Normalize audio
            if np.abs(audio).max() > 0:
                audio = audio / np.abs(audio).max()
            
            # Save as temporary WAV file for whisper
            temp_wav = audio_path + "_temp.wav"
            sf.write(temp_wav, audio, sr)
            logger.info(f"Saved temporary WAV: {temp_wav}")
            
            # Transcribe with whisper
            model = self.load_model()
            options = {
                "task": "transcribe",
                "fp16": False,
                "verbose": False
            }
            
            if language and language != "auto":
                options["language"] = language
                logger.info(f"Language set to: {language}")
            
            logger.info(f"Starting transcription...")
            result = model.transcribe(temp_wav, **options)
            text = result["text"].strip()
            
            if not text:
                text = "No speech detected in the audio file."
            else:
                logger.info(f"Transcription successful: {len(text)} characters")
            
            return text
            
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}", exc_info=True)
            raise
        
        finally:
            # Clean up temporary file
            if temp_wav and os.path.exists(temp_wav):
                try:
                    os.remove(temp_wav)
                    logger.info(f"Cleaned up temp file: {temp_wav}")
                except Exception as e:
                    logger.warning(f"Failed to clean up temp file: {e}")

# Global instance
whisper_model = WhisperModel()