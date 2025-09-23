# 3_📚_My_History.py
import streamlit as st
from ui_utils import load_theme
from auth import UserAuth, init_session_state, require_auth
import os
from datetime import datetime

st.set_page_config(
    page_title="My Music History - MelodAI",
    page_icon="📚",
    layout="wide"
)

load_theme()
init_session_state()
require_auth()

# Initialize auth system
auth = UserAuth()
user_info = st.session_state.user_info

st.markdown(f"<h1>📚 {user_info['full_name']}'s Musical Journey</h1>", unsafe_allow_html=True)
st.markdown("<h2>Revisit your AI-generated compositions</h2>", unsafe_allow_html=True)

# Get user's history
history = auth.get_user_history(user_info['id'])

if not history:
    # No history yet
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎵</div>
        <h3>Your Musical Journey Starts Here!</h3>
        <p style="color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 2rem;">
            You haven't created any compositions yet. Ready to make some music?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎵 Start Composing", use_container_width=True, type="primary"):
            st.switch_page("pages/2_🎵_Compose_Music.py")
else:
    # Show statistics
    st.markdown("### 📊 Your Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎵 Total Compositions", len(history))
    
    with col2:
        moods = [item['mood_category'] for item in history if item['mood_category']]
        favorite_mood = max(set(moods), key=moods.count) if moods else "N/A"
        st.metric("🎭 Favorite Mood", favorite_mood)
    
    with col3:
        tempos = [item['tempo'] for item in history if item['tempo']]
        avg_tempo = int(sum(tempos) / len(tempos)) if tempos else 0
        st.metric("🥁 Average Tempo", f"{avg_tempo} BPM")
    
    with col4:
        energies = [item['energy_level'] for item in history if item['energy_level']]
        avg_energy = round(sum(energies) / len(energies), 1) if energies else 0
        st.metric("⚡ Average Energy", f"{avg_energy}/10")

    st.markdown("---")
    
    # Search and filter options
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("🔍 Search your compositions", placeholder="Search by prompt or mood...")
    with col2:
        mood_filter = st.selectbox("Filter by mood", 
                                 ["All"] + list(set([item['mood_category'] for item in history if item['mood_category']])))

    # Filter history based on search and mood
    filtered_history = history
    if search_term:
        filtered_history = [item for item in filtered_history 
                          if search_term.lower() in item['prompt'].lower() or 
                             (item['mood_category'] and search_term.lower() in item['mood_category'].lower())]
    
    if mood_filter != "All":
        filtered_history = [item for item in filtered_history if item['mood_category'] == mood_filter]

    st.markdown(f"### 🎼 Your Compositions ({len(filtered_history)} found)")
    
    if not filtered_history:
        st.info("No compositions match your search criteria.")
    else:
        # Display history items
        for i, item in enumerate(filtered_history):
            with st.container():
                st.markdown(f"""
                <div style="background: var(--bg-card); padding: 1.5rem; border-radius: 12px; 
                           border: 1px solid var(--border-color); margin-bottom: 1rem;">
                """, unsafe_allow_html=True)
                
                # Header with date and prompt
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**🎵 Composition #{len(history) - history.index(item)}**")
                    st.markdown(f"*\"{item['prompt']}\"*")
                
                with col2:
                    created_date = datetime.fromisoformat(item['created_at']).strftime("%b %d, %Y at %I:%M %p")
                    st.markdown(f"<small style='color: var(--text-secondary);'>{created_date}</small>", 
                              unsafe_allow_html=True)
                
                # Musical parameters
                if item['mood_category'] or item['energy_level'] or item['tempo']:
                    st.markdown("**Musical Blueprint:**")
                    param_cols = st.columns(6)
                    
                    if item['mood_category']:
                        with param_cols[0]:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 0.5rem; background: var(--bg-main); 
                                       border-radius: 8px; border: 1px solid var(--border-color);">
                                <div style="font-size: 1.2rem;">🎭</div>
                                <div style="font-size: 0.8rem; color: var(--text-secondary);">Mood</div>
                                <div style="font-weight: 600;">{item['mood_category'].title()}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    if item['energy_level']:
                        with param_cols[1]:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 0.5rem; background: var(--bg-main); 
                                       border-radius: 8px; border: 1px solid var(--border-color);">
                                <div style="font-size: 1.2rem;">⚡</div>
                                <div style="font-size: 0.8rem; color: var(--text-secondary);">Energy</div>
                                <div style="font-weight: 600;">{item['energy_level']}/10</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    if item['tempo']:
                        with param_cols[2]:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 0.5rem; background: var(--bg-main); 
                                       border-radius: 8px; border: 1px solid var(--border-color);">
                                <div style="font-size: 1.2rem;">🥁</div>
                                <div style="font-size: 0.8rem; color: var(--text-secondary);">Tempo</div>
                                <div style="font-weight: 600;">{item['tempo']} BPM</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    if item['suggested_key']:
                        with param_cols[3]:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 0.5rem; background: var(--bg-main); 
                                       border-radius: 8px; border: 1px solid var(--border-color);">
                                <div style="font-size: 1.2rem;">🎹</div>
                                <div style="font-size: 0.8rem; color: var(--text-secondary);">Key</div>
                                <div style="font-weight: 600;">{item['suggested_key']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    if item['scale_type']:
                        with param_cols[4]:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 0.5rem; background: var(--bg-main); 
                                       border-radius: 8px; border: 1px solid var(--border-color);">
                                <div style="font-size: 1.2rem;">🎼</div>
                                <div style="font-size: 0.8rem; color: var(--text-secondary);">Scale</div>
                                <div style="font-weight: 600;">{item['scale_type']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Audio player if file exists
                if item['audio_filename']:
                    audio_path = os.path.join("output", item['audio_filename'])
                    if os.path.exists(audio_path):
                        st.markdown("**🎧 Audio:**")
                        try:
                            with open(audio_path, 'rb') as audio_file:
                                audio_bytes = audio_file.read()
                            
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                st.audio(audio_bytes, format='audio/mp3')
                            with col2:
                                st.download_button(
                                    label="📥 Download",
                                    data=audio_bytes,
                                    file_name=f"melodai_{item['mood_category']}_{i+1}.mp3",
                                    mime="audio/mp3",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Could not load audio file: {e}")
                    else:
                        st.warning("Audio file not found. It may have been moved or deleted.")
                
                # Action buttons
                st.markdown("---")
                action_cols = st.columns([1, 1, 1, 2])
                
                with action_cols[0]:
                    if st.button("🔄 Recreate", key=f"recreate_{i}", use_container_width=True):
                        st.session_state.mood_input = item['prompt']
                        st.switch_page("pages/2_🎵_Compose_Music.py")
                
                with action_cols[1]:
                    if st.button("📋 Copy Prompt", key=f"copy_{i}", use_container_width=True):
                        st.session_state.copied_prompt = item['prompt']
                        st.success("Prompt copied!")
                
                with action_cols[2]:
                    if item['chord_progression']:
                        with st.popover("🎼 View Chords"):
                            st.markdown(f"**Chord Progression:**\n\n{item['chord_progression']}")
                
                st.markdown('</div>', unsafe_allow_html=True)

# Quick actions at the bottom
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🎵 Create New Composition", use_container_width=True, type="primary"):
        st.switch_page("pages/2_🎵_Compose_Music.py")

with col2:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Home.py")

with col3:
    if len(history) > 0:
        if st.button("🗑️ Clear All History", use_container_width=True):
            if st.session_state.get('confirm_clear', False):
                # Actually clear the history (you might want to implement this in auth.py)
                st.warning("Clear history functionality would be implemented here")
                st.session_state.confirm_clear = False
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm clearing all history")
