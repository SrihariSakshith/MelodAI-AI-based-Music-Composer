# 4_ℹ️_About.py
import streamlit as st
from ui_utils import load_theme
from auth import init_session_state

st.set_page_config(
    page_title="About MelodAI - AI Music Composer",
    page_icon="ℹ️",
    layout="wide"
)

load_theme()
init_session_state()

# --- HERO SECTION ---
with st.container():
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    st.markdown("<h1>About MelodAI 🎼</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Discover the technology behind your personal AI composer</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p style="text-align:center; max-width: 800px; margin: auto; color: var(--text-secondary); font-size: 1.1rem;">
    <strong>MelodAI</strong> represents the cutting edge of AI-powered music composition. 
    Using advanced natural language processing and state-of-the-art music generation models, 
    we transform your emotions and ideas into personalized musical experiences. 
    Our mission is to democratize music creation and make it accessible to everyone, 
    regardless of musical background or technical expertise.
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- TECHNOLOGY STACK ---
st.markdown("<h3>🔬 The Technology Behind MelodAI</h3>", unsafe_allow_html=True)

cols = st.columns(2, gap="large")
with cols[0]:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">🧠</div>
        <h4>Natural Language Processing</h4>
        <p><strong>Model:</strong> RoBERTa-based sentiment analysis<br>
        <strong>Purpose:</strong> Understands emotional context and mood from your text descriptions<br>
        <strong>Capability:</strong> Processes complex emotional nuances and translates them into musical parameters</p>
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">🎵</div>
        <h4>Music Generation AI</h4>
        <p><strong>Model:</strong> Facebook's MusicGen<br>
        <strong>Purpose:</strong> Generates high-quality audio from musical descriptions<br>
        <strong>Capability:</strong> Creates unique compositions with specified tempo, key, and style</p>
    </div>
    """, unsafe_allow_html=True)

# --- HOW IT WORKS ---
st.markdown("<h3>🎯 How It Works</h3>", unsafe_allow_html=True)
cols = st.columns(3, gap="large")
with cols[0]:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">✍️</div>
        <h4>1. Text Analysis</h4>
        <p>Your description is processed through advanced NLP models that extract emotional sentiment, energy levels, and musical preferences from natural language.</p>
    </div>
    """, unsafe_allow_html=True)
with cols[1]:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">🎼</div>
        <h4>2. Parameter Generation</h4>
        <p>AI algorithms map emotional data to musical parameters: tempo, key signature, chord progressions, and instrumentation choices.</p>
    </div>
    """, unsafe_allow_html=True)
with cols[2]:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">🎶</div>
        <h4>3. Audio Synthesis</h4>
        <p>State-of-the-art generative models create unique audio compositions based on the calculated musical blueprint.</p>
    </div>
    """, unsafe_allow_html=True)

# --- FEATURES ---
st.markdown("<h3>✨ Key Features</h3>", unsafe_allow_html=True)

feature_cols = st.columns(2, gap="large")
with feature_cols[0]:
    st.markdown("""
    <div class="feature-card">
        <h4>🎨 Personalized Compositions</h4>
        <ul style="text-align: left; color: var(--text-secondary);">
            <li>Unique tracks generated for each prompt</li>
            <li>Emotional intelligence in music creation</li>
            <li>Multiple genre and style support</li>
            <li>Customizable musical parameters</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with feature_cols[1]:
    st.markdown("""
    <div class="feature-card">
        <h4>👤 User Experience</h4>
        <ul style="text-align: left; color: var(--text-secondary);">
            <li>Personal account with composition history</li>
            <li>Easy-to-use interface for all skill levels</li>
            <li>Instant audio playback and download</li>
            <li>Dark/Light theme support</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- TECHNICAL SPECS ---
st.markdown("<h3>⚙️ Technical Specifications</h3>", unsafe_allow_html=True)

spec_cols = st.columns(3, gap="medium")
with spec_cols[0]:
    st.markdown("""
    <div class="feature-card">
        <h4>🔧 Audio Quality</h4>
        <p><strong>Sample Rate:</strong> 32 kHz<br>
        <strong>Duration:</strong> 15 seconds<br>
        <strong>Format:</strong> MP3<br>
        <strong>Quality:</strong> High-fidelity stereo</p>
    </div>
    """, unsafe_allow_html=True)

with spec_cols[1]:
    st.markdown("""
    <div class="feature-card">
        <h4>🎹 Musical Range</h4>
        <p><strong>Tempo:</strong> 60-180 BPM<br>
        <strong>Keys:</strong> All major/minor keys<br>
        <strong>Genres:</strong> Classical, Pop, Electronic, Ambient<br>
        <strong>Moods:</strong> Happy, Sad, Energetic, Calm, Epic</p>
    </div>
    """, unsafe_allow_html=True)

with spec_cols[2]:
    st.markdown("""
    <div class="feature-card">
        <h4>💾 Data & Privacy</h4>
        <p><strong>Storage:</strong> Local SQLite database<br>
        <strong>History:</strong> Personal composition library<br>
        <strong>Privacy:</strong> Your data stays with you<br>
        <strong>Security:</strong> Encrypted password storage</p>
    </div>
    """, unsafe_allow_html=True)

# --- DEVELOPMENT INFO ---
st.markdown("<h3>👨‍💻 Development & Credits</h3>", unsafe_allow_html=True)

dev_cols = st.columns(2, gap="large")
with dev_cols[0]:
    st.markdown("""
    <div class="feature-card">
        <h4>🛠️ Built With</h4>
        <ul style="text-align: left; color: var(--text-secondary);">
            <li><strong>Streamlit:</strong> Interactive web application framework</li>
            <li><strong>Transformers:</strong> Hugging Face NLP models</li>
            <li><strong>PyTorch:</strong> Deep learning framework</li>
            <li><strong>SQLite:</strong> Lightweight database for user data</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with dev_cols[1]:
    st.markdown("""
    <div class="feature-card">
        <h4>🤖 AI Models Used</h4>
        <ul style="text-align: left; color: var(--text-secondary);">
            <li><strong>Sentiment Analysis:</strong> cardiffnlp/twitter-roberta-base-sentiment-latest</li>
            <li><strong>Text Embeddings:</strong> all-MiniLM-L6-v2</li>
            <li><strong>Music Generation:</strong> facebook/musicgen-small</li>
            <li><strong>Audio Processing:</strong> Custom parameter mapping algorithms</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- CALL TO ACTION ---
st.markdown("<br><hr style='border-color: var(--border-color);'><br>", unsafe_allow_html=True)

if st.session_state.get('authenticated', False):
    st.markdown("""
        <div style="text-align: center;">
            <h2>Ready to Create More Music? 🎵</h2>
            <p style="color: var(--text-secondary); font-size: 1.1rem;">Your personal AI composer is waiting for your next creative prompt!</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎵 Go to Composer Studio", use_container_width=True, type="primary"):
            st.switch_page("pages/2_🎵_Compose_Music.py")
else:
    st.markdown("""
        <div style="text-align: center;">
            <h2>Ready to Start Your Musical Journey? 🚀</h2>
            <p style="color: var(--text-secondary); font-size: 1.1rem;">Create your account and start composing personalized music today!</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏠 Get Started", use_container_width=True, type="primary"):
            st.switch_page("Home.py")
