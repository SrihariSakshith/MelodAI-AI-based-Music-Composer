# config.py

class Config:
    # --- NLP Models ---
    SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    # --- Music Generation Model ---
    MUSIC_GEN_MODEL = "facebook/musicgen-small"

    # --- Generation Parameters ---
    MAX_LENGTH = 128
    AUDIO_DURATION_SECONDS = 15  # Set to 15 seconds for faster generation
    SAMPLING_RATE = 32000  # MusicGen's native sampling rate

    # --- System ---
    # DEVICE = "cuda" # Change to "cpu" if you don't have a GPU
    DEVICE = "cpu" 