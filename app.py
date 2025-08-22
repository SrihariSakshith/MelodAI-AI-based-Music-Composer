import streamlit as st
from mood_analyzer import MoodAnalyzer
from music_parameters import MusicParameterProcessor

@st.cache_resource
def load_models():
    """Cache models to avoid reloading on each run."""
    """Cache models to avoid reloading"""
    analyzer = MoodAnalyzer()
    processor = MusicParameterProcessor()
    return analyzer, processor

def display_results(params):
    """Displays the generated musical parameters in a formatted way."""
    st.markdown('<div class="music-box">', unsafe_allow_html=True)
    st.markdown("<h3>🎼 Your Musical Blueprint</h3>", unsafe_allow_html=True)

    # Define parameters with icons, labels, and formatting
    param_groups = {
        "Core": [
            ("🎭", "Mood", params["mood_category"].capitalize()),
            ("⚡", "Energy", f"{params['energy_level']}/10"),
            ("🥁", "Tempo", f"{params['tempo']} BPM"),
        ],
        "Harmony & Melody": [
            ("🎹", "Key", f"{params['key']} ({params['suggested_key']})"),
            ("🎼", "Scale", params["scale_type"]),
            ("🎶", "Chords", " - ".join(params["chord_progression"])),
        ],
        "Timbre & Texture": [
            ("🎸", "Instruments", ", ".join(params['instruments'])),
            ("🎨", "Texture", params["texture"]),
        ],
        "Rhythm & Dynamics": [
            ("🕺", "Rhythm", params["rhythmic_pattern"]),
            ("🔊", "Dynamics", params["dynamics"]),
        ],
        "Meta": [
            ("🏷️", "Genre Style", params.get("genre_style", "N/A")),
            ("📈", "Sentiment Confidence", f"{params.get('sentiment_confidence', 'N/A'):.2f}" if isinstance(params.get('sentiment_confidence'), float) else params.get('sentiment_confidence', 'N/A')),
        ]
    }

    # Display all parameter groups in a single column to avoid empty boxes
    def render_params(params_list):
        for icon, label, value in params_list:
            st.markdown(f'<div class="param-item"><span class="param-icon">{icon}</span> <span class="param-label">{label}:</span> <span class="param-value">{value}</span></div>', unsafe_allow_html=True)

    for group_name, params_list in param_groups.items():
        st.markdown(f"<h5>{group_name}</h5>", unsafe_allow_html=True)
        render_params(params_list)

    st.markdown('</div>', unsafe_allow_html=True)

def show_test_samples(analyzer, processor):
    """Displays an expander section for testing sample inputs."""
    st.markdown("---")
    with st.expander("🔬 Test with Sample Inputs", expanded=False):
        samples = [
            "I'm excited for my workout!",
            "I need calm music for studying",
            "Feeling sad and lonely tonight",
            "Let's party and dance all night!",
            "A mysterious, suspenseful vibe",
            "Romantic dinner for two"
        ]
        st.markdown('<div class="sample-buttons-container">', unsafe_allow_html=True)
        for i, sample in enumerate(samples):
            if st.button(sample, key=f"sample_{i}"):
                try:
                    with st.spinner(f"Analyzing '{sample}'..."):
                        base_params = analyzer.analyze_mood(sample)
                        enhanced_params = processor.enhance_parameters(base_params)
                    st.json(enhanced_params)
                except Exception as e:
                    st.error(f"Failed to process sample: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Whispers of the Wires", page_icon="🎵", layout="centered")

    st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(to right top, #d4dce8, #dde3ed, #e5eaf2, #edf1f7, #f6f8fb);
    }

    /* --- Main Title & Subheader --- */
    .main-title {
        text-align: center;
        color: #1E3A8A; /* A deep, professional blue */
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .subheader {
        text-align: center;
        color: #4B5563; /* A softer, secondary text color */
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* --- Main Content Card --- */
    .main-container {
        background-color: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        padding: 2rem 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* --- Input Area --- */
    div[data-testid="stTextArea"] > label {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #1E3A8A !important;
        margin-bottom: 0.5rem;
    }
    .stTextArea textarea {
        border: 2px solid #d1d5db;
        border-radius: 10px;
        font-size: 1.1rem;
        padding: 10px;
        background-color: #f9fafb;
        min-height: 120px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
    }
    .stTextArea textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3), inset 0 2px 4px rgba(0,0,0,0.06);
    }

    /* --- Button --- */
    div[data-testid="stButton"] > button {
        width: 100%;
        border-radius: 10px;
        padding: 0.75rem 0;
        font-size: 1.2rem;
        font-weight: bold;
        background-image: linear-gradient(to right, #4f46e5 0%, #818cf8 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
    }
    div[data-testid="stButton"] > button:active {
        transform: translateY(1px);
    }
    div[data-testid="stButton"] > button:focus {
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.4);
        outline: none;
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(30px) scale(0.98);
      }
      to {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }

    /* --- Results Box --- */
    .music-box {
        background: #ffffff;
        border-radius: 15px;
        padding: 2em;
        margin-top: 2em;
        box-shadow: 0 10px 30px rgba(0,0,0,0.07);
        border-left: 6px solid;
        border-image: linear-gradient(to top, #4f46e5, #818cf8) 1;
        animation: fadeIn 0.6s ease-in-out forwards;
    }

    .music-box h3 {
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }

    .music-box h5 {
        color: #1e3a8a;
        border-bottom: 2px solid #93c5fd;
        padding-bottom: 8px;
        margin-top: 1.5em;
        margin-bottom: 1em;
        font-size: 1.2rem;
        font-weight: 700;
    }

    .param-item {
        display: flex;
        align-items: center;
        margin-bottom: 0.8rem;
        font-size: 1rem;
        padding: 8px;
        border-radius: 8px;
        transition: background-color 0.2s ease;
    }
    .param-item:hover {
        background-color: #f8f9fc;
    }

    .param-icon {
        margin-right: 0.8rem;
        font-size: 1.3rem;
        color: #4f46e5;
    }

    .param-label {
        color: #374151;
        font-weight: 600;
        flex-shrink: 0;
        margin-right: 0.5rem;
    }

    .param-value {
        color: #111827;
        word-wrap: break-word;
        flex-grow: 1;
        font-weight: 500;
    }

    /* --- Test Samples Section --- */
    .stExpander {
        border: 1px solid #d1d5db !important;
        border-radius: 10px !important;
        background-color: #ffffff !important;
        margin-top: 2rem;
    }
    .stExpander header {
        font-size: 1.1rem !important;
        font-weight: bold !important;
        color: #1e3a8a !important;
    }

    .sample-buttons-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 1rem;
    }

    .sample-buttons-container .stButton > button {
        width: auto;
        flex-grow: 1;
        background-image: none;
        background-color: #eef2f7;
        color: #334155;
        font-size: 1rem;
        font-weight: 500;
        padding: 0.5rem 0;
        box-shadow: none;
        border: 1px solid #d1d9e6;
    }
    .sample-buttons-container .stButton > button:hover {
        background-color: #d1d5db;
        transform: translateY(-1px);
        box-shadow: none;
    }

    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #6b7280;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">🎵 Whispers of the Wires</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">AI-Powered Music Composition from Your Mood</p>', unsafe_allow_html=True)

    # Load models once
    with st.spinner("Loading AI models... (First time may take a moment)"):
        analyzer, processor = load_models()

    user_input = st.text_area(
        "Describe your mood or music need:",
        placeholder="e.g., 'A soundtrack for a romantic dinner' or 'Upbeat music for a morning run'",
        height=120,
        key="mood_input"
    )

    if st.button("✨ Analyze & Compose 🎶") and user_input.strip():
        try:
            with st.spinner("🎼 Reading the emotional score and composing your musical DNA..."):
                base_params = analyzer.analyze_mood(user_input)
                enhanced_params = processor.enhance_parameters(base_params)

            display_results(enhanced_params)

        except Exception as e:
            st.error(f"😔 Oops! An error occurred: {e}")
            st.warning("Could not process the request. Please try a different input or check the model server status.")

    # Show test samples section
    show_test_samples(analyzer, processor)

    st.markdown('<div class="footer">Powered by Hugging Face & Streamlit</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()