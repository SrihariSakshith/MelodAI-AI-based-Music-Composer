# music_generator.py

import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile
import numpy as np
from pydub import AudioSegment
# We don't need `which` anymore because we are setting the path directly.
import os
from pathlib import Path

from config import Config

# --- FFMPEG Configuration ---
# This is the definitive fix. We are manually telling pydub where to find ffmpeg.
# Make sure the path below matches exactly where you extracted ffmpeg.
# IMPORTANT: Use double backslashes (\\) in the path.
ffmpeg_path = "C:\\ffmpeg\\bin\\ffmpeg.exe" 

# Check if the specified file exists before setting it
if not os.path.exists(ffmpeg_path):
    raise RuntimeError(
        f"ffmpeg.exe not found at the specified path: {ffmpeg_path}\n"
        "Please verify the path in music_generator.py is correct.\n"
        "It should point to the ffmpeg.exe file inside the bin folder you extracted."
    )

# Set the converter path for pydub
AudioSegment.converter = ffmpeg_path
print(f"✅ FFMPEG path set to: {AudioSegment.converter}")


class MusicGenerator:
    """
    Handles music generation using the MusicGen model.
    It takes musical parameters, creates a suitable prompt, generates audio,
    and processes it into a playable MP3 file.
    """
    def __init__(self):
        """
        Initializes the MusicGenerator by loading the MusicGen model and processor.
        """
        self.device = "cuda:0" if torch.cuda.is_available() and Config.DEVICE == "cuda" else "cpu"
        print(f"Initializing MusicGenerator on device: {self.device}")
        try:
            self.processor = AutoProcessor.from_pretrained(Config.MUSIC_GEN_MODEL)
            self.model = MusicgenForConditionalGeneration.from_pretrained(Config.MUSIC_GEN_MODEL)
            self.model.to(self.device)
            print("✅ MusicGen model loaded successfully.")
        except Exception as e:
            print(f"🔥 Failed to load MusicGen model: {e}")
            raise

    def _create_prompt(self, params: dict) -> str:
        """
        Creates a descriptive text prompt for the MusicGen model based on musical parameters.
        """
        energy_desc = "high-energy" if params['energy_level'] > 7 else "low-energy" if params['energy_level'] < 4 else "medium-energy"
        
        prompt = (
            f"A {params['genre_style']} track with a {params['mood_category']} mood, {energy_desc}. "
            f"The piece is in {params['suggested_key']} {params['scale_type']} "
            f"with a tempo of approximately {params['tempo']} BPM. "
            f"Prominent instruments include {', '.join(params['instruments'])}. "
            f"It features a {params['rhythmic_pattern']} rhythm and a {params['texture']} texture."
        )
        return prompt

    def _process_and_save_audio(self, audio_tensor: torch.Tensor, params: dict) -> str:
        """
        Processes the raw audio tensor: normalizes, adjusts volume, and saves as an MP3.
        """
        print("Processing and saving audio...")
        audio_np = audio_tensor.squeeze().cpu().numpy()

        audio_np /= np.max(np.abs(audio_np))
        volume_factor = 0.6 + (params.get('energy_level', 5) / 25)
        audio_np *= volume_factor
        audio_int16 = (audio_np * 32767).astype(np.int16)

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        temp_wav_path = output_dir / "temp_music.wav"
        final_mp3_path = output_dir / "generated_music.mp3"

        scipy.io.wavfile.write(temp_wav_path, rate=Config.SAMPLING_RATE, data=audio_int16)
        print(f"Temporary WAV saved to {temp_wav_path}")

        try:
            audio_segment = AudioSegment.from_wav(temp_wav_path)
            audio_segment.export(final_mp3_path, format="mp3", bitrate="192k")
            print(f"✅ Audio exported successfully to {final_mp3_path}")
            return str(final_mp3_path)
        except Exception as e:
            print(f"🔥 Error during WAV to MP3 conversion: {e}")
            raise
        finally:
            if os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)
                print(f"Removed temporary file: {temp_wav_path}")


    def generate_music(self, params: dict) -> str:
        """
        The main public method to generate music from a set of parameters.
        """
        prompt = self._create_prompt(params)
        print(f"🎵 Generating with prompt: {prompt}")

        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        ).to(self.device)

        num_tokens = int(Config.AUDIO_DURATION_SECONDS * 50) 
        
        audio_values = self.model.generate(**inputs, max_new_tokens=num_tokens)
        
        audio_path = self._process_and_save_audio(audio_values, params)
        return audio_path