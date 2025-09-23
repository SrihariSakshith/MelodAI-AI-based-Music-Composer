# auth.py
import sqlite3
import hashlib
import streamlit as st
from datetime import datetime
import os

class UserAuth:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with users and history tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Create music history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS music_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                prompt TEXT NOT NULL,
                mood_category TEXT,
                energy_level INTEGER,
                tempo INTEGER,
                suggested_key TEXT,
                scale_type TEXT,
                chord_progression TEXT,
                audio_filename TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, email, password, full_name):
        """Register a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, full_name))
            conn.commit()
            return True, "Registration successful!"
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                return False, "Username already exists!"
            elif "email" in str(e):
                return False, "Email already registered!"
            else:
                return False, "Registration failed!"
        finally:
            conn.close()
    
    def login_user(self, username, password):
        """Login user and return user info"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute('''
            SELECT id, username, email, full_name FROM users 
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        
        if user:
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (user[0],))
            conn.commit()
            
            user_info = {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3]
            }
            conn.close()
            return True, user_info
        else:
            conn.close()
            return False, "Invalid username or password!"
    
    def update_user_profile(self, user_id, full_name, email):
        """Update user profile information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET full_name = ?, email = ? 
                WHERE id = ?
            ''', (full_name, email, user_id))
            conn.commit()
            conn.close()
            return True, "Profile updated successfully!"
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Email already exists!"
    
    def save_music_history(self, user_id, prompt, params, audio_filename):
        """Save music generation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        chord_progression = " - ".join(params.get("chord_progression", []))
        
        cursor.execute('''
            INSERT INTO music_history 
            (user_id, prompt, mood_category, energy_level, tempo, 
             suggested_key, scale_type, chord_progression, audio_filename)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, prompt, params.get("mood_category"),
            params.get("energy_level"), params.get("tempo"),
            params.get("suggested_key"), params.get("scale_type"),
            chord_progression, audio_filename
        ))
        
        conn.commit()
        conn.close()
    
    def get_user_history(self, user_id, limit=20):
        """Get user's music generation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT prompt, mood_category, energy_level, tempo, 
                   suggested_key, scale_type, chord_progression, 
                   audio_filename, created_at
            FROM music_history 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        history = cursor.fetchall()
        conn.close()
        
        return [{
            'prompt': row[0],
            'mood_category': row[1],
            'energy_level': row[2],
            'tempo': row[3],
            'suggested_key': row[4],
            'scale_type': row[5],
            'chord_progression': row[6],
            'audio_filename': row[7],
            'created_at': row[8]
        } for row in history]

# Session management functions
def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'  # 'login' or 'register'

def logout_user():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.session_state.auth_mode = 'login'
    st.rerun()

def require_auth():
    """Decorator-like function to require authentication"""
    if not st.session_state.get('authenticated', False):
        st.switch_page("Home.py")
        st.stop()
