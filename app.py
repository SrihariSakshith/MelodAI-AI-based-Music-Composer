# app.py
import streamlit as st
from mood_analyzer import MoodAnalyzer
from music_parameters import MusicParameterProcessor
from music_generator import MusicGenerator
import time

# --- Model Loading ---
@st.cache_resource
def load_models():
    """
    Cache all models (NLP and MusicGen) to avoid reloading on each run.
    """
    with st.spinner("Warming up the AI studio... This might take a moment."):
        analyzer = MoodAnalyzer()
        processor = MusicParameterProcessor()
        generator = MusicGenerator()
    return analyzer, processor, generator

# --- UI Display Functions ---
def display_results(params):
    """Displays the generated musical parameters in a formatted way."""
    st.markdown("<h3>🎼 Your Musical Blueprint</h3>", unsafe_allow_html=True)

    param_groups = {
        "Core": [
            ("🎭", "Mood", params["mood_category"].capitalize()),
            ("⚡", "Energy", f"{params['energy_level']}/10"),
            ("🥁", "Tempo", f"{params['tempo']} BPM"),
        ],
        "Harmony & Melody": [
            ("🎹", "Key", f"{params['suggested_key']} ({params['key']})"),
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
        ]
    }

    def render_params(params_list):
        for icon, label, value in params_list:
            st.markdown(f'<div class="param-item"><span class="param-icon">{icon}</span> <span class="param-label">{label}:</span> <span class="param-value">{value}</span></div>', unsafe_allow_html=True)

    for group_name, params_list in param_groups.items():
        st.markdown(f"<h5>{group_name}</h5>", unsafe_allow_html=True)
        render_params(params_list)

def display_audio_player(audio_path):
    """Displays the generated audio with a player and download button."""
    st.markdown("<h4>🎧 Here's Your Custom Track</h4>", unsafe_allow_html=True)
    try:
        with open(audio_path, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        
        st.audio(audio_bytes, format='audio/mp3')
        
        st.download_button(
            label="📥 Download Track (MP3)",
            data=audio_bytes,
            file_name="whispers_of_the_wires.mp3",
            mime="audio/mp3"
        )
    except FileNotFoundError:
        st.error("Could not find the generated audio file. The generation process might have failed.")
    except Exception as e:
        st.error(f"An error occurred while trying to play the audio: {e}")

# --- Main Application Logic ---
def main():
    st.set_page_config(page_title="Whispers of the Wires", page_icon="🎵", layout="centered")

    # --- STYLES ---
    st.markdown("""
    <style>
        .stApp { background-image: linear-gradient(to right top, #d1d9e6, #d7dde8, #dde1ea, #e3e5ed, #e9e9f0); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .main-title { font-size: 3rem; text-align: center; color: #1E3A8A; font-weight: 700; margin-bottom: 0.5rem; }
        .subheader { text-align: center; color: #4B5563; font-size: 1.2rem; margin-bottom: 2rem; }
        
        /* --- Main Container Fix: No more empty boxes --- */
        .main-container {
            background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);
            padding: 2rem; border-radius: 20px; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        div[data-testid="stButton"] > button {
            width: 100%; border-radius: 10px; padding: 0.8rem 0; font-size: 1.25rem; font-weight: bold;
            background-image: linear-gradient(to right, #4338ca, #6366f1); color: white; border: none;
            transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(67, 56, 202, 0.3);
        }
        div[data-testid="stButton"] > button:hover { transform: translateY(-3px); box-shadow: 0 7px 20px rgba(67, 56, 202, 0.4); }

        /* --- Sample Prompt Buttons --- */
        .sample-buttons-container { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 1rem; }
        .sample-buttons-container .stButton > button {
            background-image: none; background-color: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe;
            font-size: 0.85rem; padding: 0.4rem 0.8rem; font-weight: 600; box-shadow: none;
        }
        .sample-buttons-container .stButton > button:hover { background-color: #e0e7ff; border-color: #a5b4fc; transform: translateY(-1px); }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .results-container {
            background: #ffffff; border-radius: 15px; padding: 2em; margin-top: 2em;
            box-shadow: 0 10px 30px rgba(0,0,0,0.07); animation: fadeIn 0.6s ease-in-out forwards;
            border-left: 6px solid #6366f1;
        }
        .results-container h3, .results-container h4 { color: #1e3a8a; text-align: center; margin-bottom: 1.5rem; font-weight: 700; }
        .results-container h5 { color: #1e3a8a; border-bottom: 2px solid #a5b4fc; padding-bottom: 8px; margin-top: 1.5em; margin-bottom: 1em; font-size: 1.2rem; }
        .param-item { display: flex; align-items: center; margin-bottom: 0.8rem; font-size: 1rem; padding: 8px; border-radius: 8px; transition: background-color 0.2s ease; }
        .param-item:hover { background-color: #f4f5f7; }
        .param-icon { margin-right: 0.8rem; font-size: 1.3rem; color: #4f46e5; }
        .param-label { color: #374151; font-weight: 600; }
        .param-value { color: #111827; word-wrap: break-word; flex-grow: 1; font-weight: 500; margin-left: 0.5rem; text-align: right; }
        .footer { text-align: center; padding: 2rem 0 1rem 0; color: #6b7280; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

    # --- APP LAYOUT ---
    st.markdown('<h1 class="main-title">🎵 Whispers of the Wires</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Crafting Custom Melodies from Your Mood with AI</p>', unsafe_allow_html=True)

    # Use a single container that is naturally centered by Streamlit's layout
    with st.container():
        try:
            analyzer, processor, generator = load_models()
        except RuntimeError as e:
            st.error(f"**Initialization Error:** {e}")
            st.warning("Please check the configuration and restart the app.")
            st.stop()
        except Exception as e:
            st.error(f"A critical error occurred while loading models: {e}")
            st.stop()

        # Initialize session state for the text area
        if "mood_input" not in st.session_state:
            st.session_state.mood_input = ""

        def set_prompt(prompt):
            st.session_state.mood_input = prompt

        user_input = st.text_area(
            "Describe your mood, a scene, or the music you need:",
            placeholder="e.g., 'An epic, cinematic soundtrack...' or 'lo-fi beats for studying'",
            height=120, key="mood_input"
        )
        
        # --- New Sample Prompts Section ---
        st.markdown("<p style='font-size:0.9rem; color:#4B5563; text-align:center;'>Or try one of these ideas:</p>", unsafe_allow_html=True)
        samples = {
            "😊 Happy Folk": "Happy and upbeat acoustic folk music for a sunny morning",
            "💪 Energetic EDM": "High-energy electronic dance music for a workout, 140 bpm",
            "🤫 Suspenseful": "A mysterious and suspenseful soundtrack for a detective exploring a dark alley",
            "🧘 Calm Piano": "Calm, peaceful, ambient piano music for focus and studying",
            "😢 Sad Violin": "A sad, slow, melancholic piano and violin piece for a rainy day",
            "⚔️ Epic Orchestral": "An epic orchestral score for a fantasy battle scene"
        }
        
        cols = st.columns(3)
        for i, (label, prompt) in enumerate(samples.items()):
            with cols[i % 3]:
                if st.button(label, key=f"sample_{i}", on_click=set_prompt, args=(prompt,)):
                    pass # The on_click handles the logic

        st.markdown("<br>", unsafe_allow_html=True) # Spacer

        # Main compose button
        if st.button("✨ Compose My Track ✨", key="compose_button") and st.session_state.mood_input.strip():
            try:
                with st.status("Your personal composer is at work...", expanded=True) as status:
                    status.write("🧠 Analyzing emotional tone...")
                    base_params = analyzer.analyze_mood(st.session_state.mood_input)
                    time.sleep(0.5)

                    status.write("🎼 Building the musical blueprint...")
                    enhanced_params = processor.enhance_parameters(base_params)
                    time.sleep(0.5)

                    status.write("🎶 Composing your track... This is the magic part!")
                    audio_path = generator.generate_music(enhanced_params)
                    
                    status.update(label="✅ Composition Complete!", state="complete", expanded=False)

                st.balloons()
                
                # Display results below the main container, not inside it, for better flow
                res_col1, res_col2 = st.columns(2, gap="large")
                with res_col1:
                    with st.container():
                        display_results(enhanced_params)
                
                with res_col2:
                    with st.container():
                        display_audio_player(audio_path)

            except Exception as e:
                st.error(f"😔 Oops! An error occurred during composition: {e}")
                st.warning("The AI might be busy, or the request was too complex. Please try a different input.")

    st.markdown('<div class="footer">Powered by Hugging Face, PyTorch & Streamlit</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()