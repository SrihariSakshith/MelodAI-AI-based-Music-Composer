# 🎼 MelodAI - AI-Powered Music Composer

**Transform your emotions into personalized music with the power of artificial intelligence.**

MelodAI is an intelligent music composition system that uses advanced natural language processing and state-of-the-art AI models to create unique, personalized musical compositions based on your mood, emotions, and creative descriptions.

## ✨ Features

### 🎵 **AI Music Generation**
- **Natural Language Input**: Describe your mood, scene, or musical vision in plain English
- **Advanced AI Models**: Powered by RoBERTa sentiment analysis and Facebook's MusicGen
- **Personalized Compositions**: Every track is unique and tailored to your specific input
- **High-Quality Audio**: 32kHz stereo MP3 output with professional sound quality

### 👤 **User Experience**
- **User Authentication**: Secure registration and login system
- **Personal History**: Save and revisit all your compositions
- **Profile Management**: Edit your profile and manage your account
- **Search & Filter**: Find your past compositions easily
- **Dark/Light Theme**: Beautiful UI with theme switching

### 🎼 **Musical Intelligence**
- **Mood Analysis**: AI understands emotional context from your descriptions
- **Music Theory Integration**: Automatic key, scale, and chord progression selection
- **Advanced Parameters**: Tempo, dynamics, texture, and instrumentation suggestions
- **Genre Recommendations**: AI suggests appropriate musical styles
- **Production Insights**: Get professional production style recommendations

### 🎨 **Rich Musical Parameters**
- **Comprehensive Blueprint**: Detailed musical analysis for each composition
- **Instrumentation Suggestions**: AI recommends appropriate instruments
- **Time Signatures**: Support for various rhythmic patterns
- **Harmonic Complexity**: Adaptive complexity based on energy levels
- **Production Styles**: Professional mixing and mastering suggestions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- At least 4GB RAM (8GB recommended for better performance)
- Internet connection for initial model downloads

### Installation

1. **Clone or Download the Project**
   ```bash
   # If using git
   git clone <repository-url>
   cd ai-based-music-composition
   
   # Or download and extract the ZIP file
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv myenv
   myenv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   streamlit run Home.py
   ```

5. **Open in Browser**
   - The application will automatically open in your default browser
   - If not, navigate to `http://localhost:8501`

## 🎯 How to Use

### 1. **Create Your Account**
- Click on the "Register" tab on the homepage
- Fill in your details (full name, username, email, password)
- Click "Create Account" to register

### 2. **Login**
- Use the "Login" tab with your username and password
- You'll be redirected to your personalized dashboard

### 3. **Compose Music**
- Navigate to "Compose Music" from the sidebar
- Describe your musical vision in the text area
- Use sample prompts for inspiration
- Click "Compose My Track" to generate your music

### 4. **Explore Your History**
- Visit "My History" to see all your past compositions
- Search and filter your tracks
- Re-download or recreate any composition
- View detailed musical parameters for each track

### 5. **Learn More**
- Check the "About" page for technical details
- Understand the AI models and technology behind MelodAI

## 🎼 Example Prompts

Get started with these creative prompts:

**Emotional Descriptions:**
- "A melancholic piano piece for a rainy evening"
- "Energetic and uplifting music for a morning workout"
- "Mysterious and suspenseful soundtrack for a thriller scene"

**Scene-Based:**
- "Epic orchestral music for a space battle"
- "Calm acoustic guitar for meditation"
- "Romantic jazz for a candlelit dinner"

**Style-Specific:**
- "80s synthwave with driving bass and retro synths"
- "Celtic folk music with traditional instruments"
- "Modern electronic dance music with heavy drops"

## 🔧 Technical Architecture

### **AI Models Used:**
- **Sentiment Analysis**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Text Embeddings**: `all-MiniLM-L6-v2`
- **Music Generation**: `facebook/musicgen-small`

### **Technology Stack:**
- **Frontend**: Streamlit with custom CSS
- **Backend**: Python with advanced music theory algorithms
- **Database**: SQLite for user data and history
- **AI Framework**: Transformers, PyTorch
- **Audio Processing**: Pydub, SciPy

### **System Requirements:**
- **Minimum**: 4GB RAM, 2GB storage
- **Recommended**: 8GB RAM, 5GB storage
- **GPU**: Optional (CUDA-compatible for faster generation)

## 📁 Project Structure

```
ai-based-music-composition/
├── Home.py                 # Main homepage with authentication
├── auth.py                 # User authentication system
├── config.py              # Configuration settings
├── mood_analyzer.py       # AI mood analysis
├── music_parameters.py    # Advanced music theory processing
├── music_generator.py     # AI music generation
├── ui_utils.py           # UI utilities and theming
├── style.css             # Custom styling
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── pages/
│   ├── 2_🎵_Compose_Music.py    # Music composition interface
│   ├── 3_📚_My_History.py       # User history management
│   └── 4_ℹ️_About.py           # About page with technical details
└── output/              # Generated audio files
```

## 🎵 Musical Parameters Explained

### **Mood Categories:**
- **Happy**: Major scales, uplifting chord progressions
- **Sad**: Minor scales, melancholic harmonies
- **Calm**: Peaceful progressions, gentle rhythms
- **Energetic**: Driving rhythms, powerful dynamics
- **Mysterious**: Unusual scales, sparse arrangements
- **Romantic**: Lush harmonies, expressive melodies

### **Energy Levels (1-10):**
- **1-3**: Minimal, intimate, soft dynamics
- **4-6**: Moderate, balanced, comfortable listening
- **7-10**: High energy, full arrangements, powerful sound

### **Musical Elements:**
- **Tempo**: 60-180 BPM based on mood and energy
- **Key Signatures**: All major and minor keys
- **Time Signatures**: 4/4, 3/4, 6/8, and complex meters
- **Dynamics**: pp (very soft) to f (loud)
- **Texture**: Monophonic, homophonic, polyphonic

## 🛠️ Customization

### **Adding New Moods:**
Edit `music_parameters.py` to add new mood categories:
```python
"epic": {
    "scales": ["major", "minor", "dorian"],
    "chord_progressions": [["i", "VII", "VI", "VII"]],
    "rhythmic_patterns": ["powerful", "driving"],
    "typical_keys": ["Dm", "Am", "Em"]
}
```

### **Modifying UI:**
- Edit `style.css` for visual customization
- Modify `ui_utils.py` for functionality changes
- Update page files in `pages/` for content changes

### **Database Customization:**
- Modify `auth.py` to add new user fields
- Update database schema in the `init_database()` method

## 🐛 Troubleshooting

### **Common Issues:**

**1. Model Loading Errors:**
- Ensure stable internet connection for initial downloads
- Check available disk space (models require ~2GB)
- Restart the application if models fail to load

**2. Audio Generation Fails:**
- Verify all dependencies are installed correctly
- Check system resources (RAM/CPU usage)
- Try shorter, simpler prompts

**3. Database Errors:**
- Delete `users.db` file to reset the database
- Check file permissions in the project directory

**4. UI Issues:**
- Clear browser cache and cookies
- Try a different browser
- Check console for JavaScript errors

### **Performance Optimization:**
- Use GPU acceleration if available (modify `config.py`)
- Reduce audio duration for faster generation
- Close other resource-intensive applications

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**: Use the issue tracker for bug reports
2. **Suggest Features**: Propose new features or improvements
3. **Code Contributions**: Submit pull requests with enhancements
4. **Documentation**: Help improve documentation and examples

### **Development Setup:**
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black *.py pages/*.py

# Check code style
flake8 *.py pages/*.py
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Hugging Face**: For providing excellent AI models and transformers library
- **Facebook Research**: For the MusicGen model
- **Streamlit**: For the amazing web application framework
- **Open Source Community**: For the various libraries and tools used

## 📞 Support

If you encounter any issues or have questions:

1. Check this README for common solutions
2. Search existing issues in the repository
3. Create a new issue with detailed information
4. Include system information and error messages

## 🔮 Future Enhancements

- **Real-time Collaboration**: Multiple users composing together
- **MIDI Export**: Export compositions as MIDI files
- **Advanced Instruments**: More detailed instrument modeling
- **Longer Compositions**: Support for full-length songs
- **Mobile App**: Native mobile application
- **Cloud Deployment**: Web-based version with cloud processing

---

**Made with ❤️ and AI** | **Start creating your musical masterpieces today!** 🎵
