# Home.py
import streamlit as st
from ui_utils import load_theme
from auth import UserAuth, init_session_state, logout_user
import re

st.set_page_config(
    page_title="MelodAI - AI Music Composer",
    page_icon="🎼",
    layout="wide"
)

load_theme()
init_session_state()

# Initialize auth system
auth = UserAuth()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

# Check if user is already authenticated
if st.session_state.get('authenticated', False):
    # User is logged in, show main homepage
    user_info = st.session_state.user_info
    
    # User info in sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"**Welcome, {user_info['full_name']}!** 👋")
        st.markdown(f"*@{user_info['username']}*")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Edit Profile", use_container_width=True):
                st.session_state.show_edit_profile = True
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
    
    # Show edit profile modal
    if st.session_state.get('show_edit_profile', False):
        with st.container():
            st.markdown("### ✏️ Edit Profile")
            
            with st.form("edit_profile_form"):
                new_full_name = st.text_input("Full Name", value=user_info['full_name'])
                new_email = st.text_input("Email", value=user_info['email'])
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                        if validate_email(new_email):
                            success, message = auth.update_user_profile(
                                user_info['id'], new_full_name, new_email
                            )
                            if success:
                                st.session_state.user_info['full_name'] = new_full_name
                                st.session_state.user_info['email'] = new_email
                                st.success(message)
                                st.session_state.show_edit_profile = False
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.error("Please enter a valid email address")
                
                with col2:
                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                        st.session_state.show_edit_profile = False
                        st.rerun()
    
    # Main homepage content for authenticated users
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    st.markdown(f"<h1>Welcome back, {user_info['full_name']}! 🎼</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Ready to create some amazing music today?</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p style="text-align:center; max-width: 700px; margin: auto; color: var(--text-secondary);">
    Your personal AI composer is ready to transform your ideas into beautiful melodies. 
    Describe your mood, and let's create something magical together!
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎵 Start Composing", use_container_width=True, type="primary"):
            st.switch_page("pages/2_🎵_Compose_Music.py")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📚 View My History", use_container_width=True):
            st.switch_page("pages/3_📚_My_History.py")

else:
    # User is not logged in, show login/register interface
    
    # --- HERO SECTION ---
    with st.container():
        st.markdown('<div class="hero-section">', unsafe_allow_html=True)
        st.markdown("<h1>🎼 MelodAI</h1>", unsafe_allow_html=True)
        st.markdown("<h2>Your Personal AI Music Composer</h2>", unsafe_allow_html=True)
        st.markdown("""
        <p style="text-align:center; max-width: 700px; margin: auto; color: var(--text-secondary);">
        Transform your thoughts and emotions into beautiful, personalized music with the power of AI. 
        Join thousands of creators who are already composing their musical stories.
        </p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- FEATURES SECTION ---
    st.markdown("<h3>✨ What Makes MelodAI Special</h3>", unsafe_allow_html=True)
    cols = st.columns(3, gap="large")
    
    with cols[0]:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🧠</div>
            <h4>AI-Powered Analysis</h4>
            <p>Our advanced AI understands your emotions and translates them into musical parameters with incredible accuracy.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🎨</div>
            <h4>Personalized Compositions</h4>
            <p>Every track is unique to you. No two compositions are the same, ensuring your music is truly personal.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">📱</div>
            <h4>Easy to Use</h4>
            <p>Simply describe your mood or scene in natural language, and watch as AI creates your perfect soundtrack.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- LOGIN/REGISTER SECTION ---
    st.markdown("<br><hr style='border-color: var(--border-color);'><br>", unsafe_allow_html=True)
    
    # Toggle between login and register
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_tab1, auth_tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with auth_tab1:
            st.markdown("### Welcome Back!")
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                if st.form_submit_button("🚀 Login", use_container_width=True, type="primary"):
                    if username and password:
                        success, result = auth.login_user(username, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.user_info = result
                            st.success("Login successful! Welcome back! 🎉")
                            st.rerun()
                        else:
                            st.error(result)
                    else:
                        st.error("Please fill in all fields")
        
        with auth_tab2:
            st.markdown("### Join the MelodAI Community!")
            with st.form("register_form"):
                reg_full_name = st.text_input("Full Name", placeholder="Your full name")
                reg_username = st.text_input("Username", placeholder="Choose a unique username")
                reg_email = st.text_input("Email", placeholder="your.email@example.com")
                reg_password = st.text_input("Password", type="password", placeholder="Create a strong password")
                reg_confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                
                if st.form_submit_button("🎵 Create Account", use_container_width=True, type="primary"):
                    if all([reg_full_name, reg_username, reg_email, reg_password, reg_confirm_password]):
                        if reg_password != reg_confirm_password:
                            st.error("Passwords don't match!")
                        elif not validate_email(reg_email):
                            st.error("Please enter a valid email address")
                        else:
                            is_valid, password_msg = validate_password(reg_password)
                            if not is_valid:
                                st.error(password_msg)
                            else:
                                success, message = auth.register_user(
                                    reg_username, reg_email, reg_password, reg_full_name
                                )
                                if success:
                                    st.success("Registration successful! Please login with your new account. 🎉")
                                    st.balloons()
                                else:
                                    st.error(message)
                    else:
                        st.error("Please fill in all fields")

    # --- HOW IT WORKS SECTION ---
    st.markdown("<br><hr style='border-color: var(--border-color);'><br>", unsafe_allow_html=True)
    st.markdown("<h3>🎯 How It Works</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3, gap="large")
    with cols[0]:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">✍️</div>
            <h4>1. Describe Your Vision</h4>
            <p>Tell us about your mood, a scene, or the type of music you want. Be as creative as you like!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🔮</div>
            <h4>2. AI Magic Happens</h4>
            <p>Our AI analyzes your input and creates a detailed musical blueprint with tempo, key, instruments, and more.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🎶</div>
            <h4>3. Enjoy Your Music</h4>
            <p>Listen to your personalized composition, download it, and share it with the world!</p>
        </div>
        """, unsafe_allow_html=True)

    # --- CALL TO ACTION ---
    st.markdown("<br><hr style='border-color: var(--border-color);'><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center;">
            <h2>🚀 Ready to Start Your Musical Journey?</h2>
            <p style="color: var(--text-secondary); font-size: 1.1rem;">
                Join our community of creators and start composing music that truly represents you.
            </p>
        </div>
        """, unsafe_allow_html=True)
