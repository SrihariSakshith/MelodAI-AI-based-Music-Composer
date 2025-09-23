# about.py
import streamlit as st
from ui_utils import load_theme
from auth import init_session_state

st.set_page_config(
    page_title="MelodAI - AI Music Composer",
    page_icon="🎼",
    layout="wide"
)

load_theme()

# --- HERO SECTION ---
with st.container():
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    st.markdown("<h1>MelodAI: Your Personal AI Composer</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Crafting unique, personalized melodies from your mood and ideas.</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p style="text-align:center; max-width: 700px; margin: auto; color: var(--text-secondary);">
    Welcome to <strong>MelodAI</strong>, an intelligent music composition system powered by advanced AI. 
    Our goal is to generate high-quality music that resonates with your feelings. 
    Whether you need a calming tune for studying, an energetic track for a workout, or a cinematic score for a story, 
    MelodAI translates your thoughts into music.
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- HOW IT WORKS ---
st.markdown("<h3>How It Works</h3>", unsafe_allow_html=True)
cols = st.columns(3, gap="large")
with cols[0]:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">✍️</div>
        <h4>1. Describe Your Vibe</h4>
        <p>Start by typing a description of your mood, a scene, or the kind of music you're looking for. Be as simple or as detailed as you like!</p>
    </div>
    """, unsafe_allow_html=True)
with cols[1]:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">🧠</div>
        <h4>2. AI Analyzes & Composes</h4>
        <p>Our system uses NLP to understand your text, then translates it into a detailed musical blueprint—tempo, key, instruments, and more.</p>
    </div>
    """, unsafe_allow_html=True)
with cols[2]:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">🎶</div>
        <h4>3. Listen to Your Melody</h4>
        <p>A powerful music generation model brings the blueprint to life, creating a unique audio track just for you. Listen, enjoy, and download!</p>
    </div>
    """, unsafe_allow_html=True)

# --- CALL TO ACTION ---
st.markdown("<br><hr style='border-color: var(--border-color);'><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center;">
        <h2>Ready to Create?</h2>
        <p style="color: var(--text-secondary);">Navigate to the <strong>Compose Music</strong> page from the sidebar to start your musical journey.</p>
    </div>
    """, unsafe_allow_html=True)