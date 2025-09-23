# ui_utils.py
import streamlit as st
import streamlit.components.v1 as components

def load_theme():
    """
    Loads the CSS file and injects the theme-switching JavaScript.
    This function should be called at the top of every page.
    """
    # Load the CSS file
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Initialize session state for theme if it doesn't exist
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    # Determine if the current theme is dark
    is_dark = st.session_state.theme == "dark"

    # Create the theme toggle in the sidebar
    # The callback function updates the session state
    def update_theme():
        st.session_state.theme = "dark" if st.session_state.theme_toggle else "light"

    st.sidebar.toggle(
        "🌙 Dark Mode",
        value=is_dark,
        key="theme_toggle",
        on_change=update_theme
    )

    # Show user info in sidebar if authenticated
    if st.session_state.get('authenticated', False):
        user_info = st.session_state.user_info
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"""
        <div class="user-profile">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👤</div>
                <div style="font-weight: 600; color: var(--text-primary);">{user_info['full_name']}</div>
                <div style="font-size: 0.9rem; color: var(--text-secondary);">@{user_info['username']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # JavaScript to apply the theme to the body element
    js_code = f"""
    <script>
        const body = window.parent.document.querySelector('body');
        body.setAttribute('data-theme', '{st.session_state.theme}');
    </script>
    """
    components.html(js_code, height=0)