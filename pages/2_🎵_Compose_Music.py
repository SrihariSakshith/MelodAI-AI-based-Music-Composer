import streamlit as st
from ui_utils import load_theme
from mood_analyzer import MoodAnalyzer
from music_parameters import MusicParameterProcessor
from music_generator import MusicGenerator
from auth import UserAuth, init_session_state, require_auth
import time
import os

load_theme()
init_session_state()
require_auth()  # Require authentication to access this page

# Initialize auth system
auth = UserAuth()

# --- INITIALIZE SESSION STATE ---
if 'track_generated' not in st.session_state:
    st.session_state.track_generated = False
    st.session_state.enhanced_params = None
    st.session_state.audio_path = None
if "mood_input" not in st.session_state:
    st.session_state.mood_input = ""

# --- MODEL LOADING ---
@st.cache_resource
def load_models():
    with st.spinner("Warming up the AI studio... This might take a moment."):
        analyzer = MoodAnalyzer()
        processor = MusicParameterProcessor()
        generator = MusicGenerator()
    return analyzer, processor, generator

# --- UI DISPLAY FUNCTIONS ---
def display_musical_blueprint(params):
    st.markdown("<h4>🎼 Musical Blueprint</h4>", unsafe_allow_html=True)
    
    # Main parameters
    main_params = [
        ("🎭 Mood", params["mood_category"].capitalize()),
        ("⚡ Energy", f"{params['energy_level']}/10"),
        ("🥁 Tempo", f"{params['tempo']} BPM"),
        ("🎵 Time Sig", params.get("time_signature", "4/4"))
    ]
    
    # Harmony parameters
    harmony_params = [
        ("🎹 Key", f"{params['suggested_key']}"),
        ("🎼 Scale", params["scale_type"]),
        ("🎶 Chords", " - ".join(params["chord_progression"])),
        ("🎨 Texture", params.get("texture", "N/A"))
    ]
    
    # Advanced parameters
    advanced_params = [
        ("🔊 Dynamics", params.get("dynamics", "mf")),
        ("🎯 Complexity", params.get("harmonic_complexity", "moderate")),
        ("🎪 Genre", ", ".join(params.get("genre_suggestions", ["Contemporary"])[:2])),
        ("🎚️ Production", params.get("production_style", "balanced")[:20] + "...")
    ]

    # Display main parameters
    st.markdown('<div class="param-grid">', unsafe_allow_html=True)
    for icon, value in main_params:
        emoji, text = icon.split(" ", 1)
        st.markdown(f"""
        <div class="param-card">
            <div class="param-icon">{emoji}</div>
            <div class="param-label">{text}</div>
            <div class="param-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display harmony parameters
    st.markdown('<div class="param-grid" style="margin-top: 1rem;">', unsafe_allow_html=True)
    for icon, value in harmony_params:
        emoji, text = icon.split(" ", 1)
        st.markdown(f"""
        <div class="param-card">
            <div class="param-icon">{emoji}</div>
            <div class="param-label">{text}</div>
            <div class="param-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display advanced parameters
    st.markdown('<div class="param-grid" style="margin-top: 1rem;">', unsafe_allow_html=True)
    for icon, value in advanced_params:
        emoji, text = icon.split(" ", 1)
        st.markdown(f"""
        <div class="param-card">
            <div class="param-icon">{emoji}</div>
            <div class="param-label">{text}</div>
            <div class="param-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show instrumentation if available
    if "instrumentation" in params:
        with st.expander("🎸 Suggested Instrumentation"):
            instr = params["instrumentation"]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Primary Instruments:**")
                for inst in instr.get("primary", []):
                    st.markdown(f"• {inst}")
            
            with col2:
                st.markdown("**Secondary/Harmony:**")
                for inst in instr.get("secondary", []):
                    st.markdown(f"• {inst}")
            
            with col3:
                st.markdown("**Rhythm Section:**")
                for inst in instr.get("rhythm", []):
                    st.markdown(f"• {inst}")


def display_audio_player(audio_path):
    st.markdown("<h4>🎧 Your Masterpiece</h4>", unsafe_allow_html=True)
    try:
        with open(audio_path, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        st.download_button(label="📥 Download Track (MP3)", data=audio_bytes, file_name="melodai_track.mp3", mime="audio/mp3", use_container_width=True)
    except Exception as e:
        st.error(f"An error occurred while loading the audio: {e}")

# --- PAGE LAYOUT ---
user_info = st.session_state.user_info
st.markdown(f"<h1>Welcome to your Studio, {user_info['full_name']}! 🎼</h1>", unsafe_allow_html=True)
st.markdown("<h2>Let's create something amazing together.</h2>", unsafe_allow_html=True)

try:
    analyzer, processor, generator = load_models()
except Exception as e:
    st.error(f"A critical error occurred while loading AI models: {e}")
    st.stop()

# --- COMPOSER INPUT (No unnecessary containers) ---
def set_prompt(prompt):
    st.session_state.mood_input = prompt

st.text_area(
    "Describe your mood, a scene, or the music you need:",
    placeholder="e.g., An epic, cinematic soundtrack for a space battle",
    height=120, key="mood_input", label_visibility="collapsed"
)

st.write("<p style='text-align: center; color: var(--text-secondary);'>Or try one of these ideas:</p>", unsafe_allow_html=True)

samples = {"Happy Folk": "...", "Energetic EDM": "...", "Suspenseful": "...", "Calm Piano": "..."}

cols = st.columns(4)
cols[0].button("😊 Happy Folk", on_click=set_prompt, args=("Happy acoustic folk music",), use_container_width=True, type="secondary")
cols[1].button("💪 Energetic EDM", on_click=set_prompt, args=("High-energy electronic dance music",), use_container_width=True, type="secondary")
cols[2].button("🤫 Suspenseful", on_click=set_prompt, args=("A mysterious, suspenseful soundtrack",), use_container_width=True, type="secondary")
cols[3].button("🧘 Calm Piano", on_click=set_prompt, args=("Calm, peaceful, ambient piano music",), use_container_width=True, type="secondary")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ Compose My Track ✨", use_container_width=True, type="primary"):
    if st.session_state.mood_input.strip():
        st.session_state.track_generated = False
        try:
            with st.status("Your personal composer is at work...", expanded=True) as status:
                status.write("🧠 Analyzing emotional tone...")
                base_params = analyzer.analyze_mood(st.session_state.mood_input)
                time.sleep(0.5); status.write("🎼 Building the musical blueprint...")
                enhanced_params = processor.generate_advanced_parameters(base_params)
                time.sleep(0.5); status.write("🎶 Composing your track... This is the magic part!")
                audio_path = generator.generate_music(enhanced_params)

                # Save to user history
                audio_filename = os.path.basename(audio_path) if audio_path else None
                auth.save_music_history(
                    user_info['id'], 
                    st.session_state.mood_input, 
                    enhanced_params, 
                    audio_filename
                )
                
                st.session_state.track_generated = True
                st.session_state.enhanced_params = enhanced_params
                st.session_state.audio_path = audio_path
                status.update(label="✅ Composition Complete!", state="complete", expanded=False)
            st.balloons()
            st.success("🎉 Your composition has been saved to your history!")
        except Exception as e:
            st.error(f"😔 Oops! An error occurred: {e}")
            st.session_state.track_generated = False
    else:
        st.warning("Please describe the music you want to create.")
        st.session_state.track_generated = False

# --- RESULTS AREA (No unnecessary containers) ---
if st.session_state.track_generated:
    st.markdown("<h3>Your AI-Generated Composition</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1], gap="large")
    with col1:
        display_musical_blueprint(st.session_state.enhanced_params)
    with col2:
        display_audio_player(st.session_state.audio_path)
