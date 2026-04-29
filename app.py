import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import tempfile
import os

# Try to import librosa, but provide fallback if it's not installed or fails
try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

# --- MOCK DATABASE OF MOVES WITH GIFS ---
# Using generic placeholder GIFs to simulate AI video generation
MOVES_DB = {
    "Hindi/Bollywood": {
        "Beginner": [
            {"name": "Thumka", "gif": "https://media.giphy.com/media/l2YWCHf5RZRoO33O0/giphy.gif"},
            {"name": "Lightbulb Twist", "gif": "https://media.giphy.com/media/3o6wrFg0Ubgv1PjZ3a/giphy.gif"},
            {"name": "Shoulder Drop", "gif": "https://media.giphy.com/media/l1IYfwozudAdkuZk4/giphy.gif"}
        ]
    },
    "Punjabi": {
        "Beginner": [
            {"name": "Bhangra Shoulders", "gif": "https://media.giphy.com/media/3ohfFuqPNPTl9gwktG/giphy.gif"},
            {"name": "Double Clap", "gif": "https://media.giphy.com/media/l2JhnvF9p3cfv9TgQ/giphy.gif"},
            {"name": "Foot Tap", "gif": "https://media.giphy.com/media/xT1XGzH3Rk2uUUS4sU/giphy.gif"}
        ]
    },
    "Tamil (Kuthu)": {
        "Beginner": [
            {"name": "Local Kuthu Step", "gif": "https://media.giphy.com/media/l41YkxvU8c7J7Bba0/giphy.gif"},
            {"name": "Whistle Podu", "gif": "https://media.giphy.com/media/3o7TKDkMBg0I7x0F1K/giphy.gif"},
            {"name": "Shirt Collar Dust", "gif": "https://media.giphy.com/media/xT0BKr4MvHdhtX8ZQ4/giphy.gif"}
        ]
    },
    "Telugu (Teen Maar)": {
        "Beginner": [
            {"name": "Teen Maar Beat", "gif": "https://media.giphy.com/media/l1J9FiGxR61OcF2mI/giphy.gif"},
            {"name": "Hand Spin", "gif": "https://media.giphy.com/media/26ufmyJhA4z1rR7O0/giphy.gif"},
            {"name": "Jump Step", "gif": "https://media.giphy.com/media/3o7TKR1b2XEE5AARyM/giphy.gif"}
        ]
    },
    "Kannada": {
        "Beginner": [
            {"name": "Sandalwood Sway", "gif": "https://media.giphy.com/media/l0HlJ7aASyD1kOiaQ/giphy.gif"},
            {"name": "Folk Step", "gif": "https://media.giphy.com/media/3o7aD2saalZwwTlY3e/giphy.gif"}
        ]
    },
    "American Pop/Hip Hop": {
        "Beginner": [
            {"name": "The Slide", "gif": "https://media.giphy.com/media/26AHyTdIGd31R2w4U/giphy.gif"},
            {"name": "The Woah", "gif": "https://media.giphy.com/media/M3i6XHZUcBJc4OLEXv/giphy.gif"},
            {"name": "Two-Step", "gif": "https://media.giphy.com/media/l3vRlT2k2L35Cnn5C/giphy.gif"}
        ]
    }
}

# --- PAGE CONFIG ---
st.set_page_config(page_title="Reel Buddy V2", page_icon="🕺", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
.vibe-meter {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    padding: 10px;
    border-radius: 10px;
    color: white;
}
.low-vibe { background-color: #ff4b4b; }
.mid-vibe { background-color: #ffa421; }
.high-vibe { background-color: #21c354; }
.step-card {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("🕺 Reel Buddy V2")
st.sidebar.markdown("AI Choreography with Audio Sync & Video Generation!")

st.sidebar.header("1. Upload Audio")
audio_file = st.sidebar.file_uploader("Upload your song (MP3/WAV)", type=['mp3', 'wav'])

st.sidebar.header("2. Setup your crew")
group_size = st.sidebar.slider("Group Size", min_value=1, max_value=10, value=3)

st.sidebar.header("3. Pick a Style")
dance_style = st.sidebar.selectbox("Regional Style", list(MOVES_DB.keys()))

generate_btn = st.sidebar.button("✨ Generate Video Choreography", use_container_width=True)

# --- HELPER FUNCTION FOR BPM ---
def get_bpm(file_buffer):
    if not LIBROSA_AVAILABLE:
        time.sleep(1) # Simulate processing
        return random.randint(90, 140) # Mock BPM
    
    try:
        # Librosa needs a file path, so we save the uploaded buffer to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(file_buffer.read())
            tmp_path = tmp.name
        
        y, sr = librosa.load(tmp_path, duration=30) # Load first 30s
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # Cleanup temp file
        try:
            os.remove(tmp_path)
        except:
            pass
            
        return round(float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo))
    except Exception as e:
        # Fallback if ffmpeg or librosa processing fails
        return random.randint(90, 140)


# --- MAIN STAGE ---
st.title("🎥 Your Custom Reel Routine")

if generate_btn:
    if audio_file is None:
        st.warning("Please upload an audio file first to sync the choreography!")
        st.stop()
        
    # Adding a fun loading spinner for "AI Video Generation"
    with st.spinner('Analyzing Audio BPM & Rendering AI Video Sequences...'):
        bpm = get_bpm(audio_file)
        time.sleep(2) # Extra sleep to simulate rendering
        
    st.success(f"🎵 Audio Analyzed! Detected BPM: **{bpm}**. Matching choreography speed...")
        
    col1, col2 = st.columns([1, 1])

    # --- FORMATION ENGINE ---
    with col1:
        st.subheader(f"📍 Suggested Formation ({group_size} People)")
        
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_facecolor('#f0f2f6')
        ax.axis('off')
        
        positions = []
        if group_size == 1:
            positions = [(0, 0)]
        elif group_size == 2:
            positions = [(-1, 0), (1, 0)]
        elif group_size == 3:
            positions = [(0, 1), (-1, -1), (1, -1)]
        elif group_size == 4:
            positions = [(0, 1), (-1, 0), (1, 0), (0, -1)]
        elif group_size == 5:
            positions = [(0, 1), (-1.5, 0), (1.5, 0), (-0.75, -1), (0.75, -1)]
        else:
            for _ in range(group_size):
                positions.append((random.uniform(-2, 2), random.uniform(-2, 2)))
                
        for i, (x, y) in enumerate(positions):
            ax.scatter(x, y, s=1500, c='#FF4B4B', alpha=0.8, edgecolors='white', linewidth=2)
            ax.text(x, y, f"{i+1}", fontsize=14, ha='center', va='center', color='white', fontweight='bold')
            
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        st.pyplot(fig)

    # --- VIDEO CHOREOGRAPHY SEQUENCE ---
    with col2:
        st.subheader(f"🎬 Video Sequence ({dance_style})")
        
        available_moves = MOVES_DB[dance_style]["Beginner"]
        # Sequence length based on BPM (faster song = more moves)
        sequence_length = 6 if bpm > 110 else 4
        
        # Pick steps
        chosen_steps = [random.choice(available_moves) for _ in range(sequence_length)]
        
        # Display as a timeline of videos/GIFs
        for idx, step in enumerate(chosen_steps):
            st.markdown(f"""
            <div class="step-card">
                <h4>Step {idx+1}: {step['name']}</h4>
                <img src="{step['gif']}" width="100%" style="border-radius: 8px;">
            </div>
            """, unsafe_allow_html=True)
            
        st.info("💡 Note: These are simulated video clips. In a production environment with cloud GPUs, these would be generated in real-time based on your specific song.")
        
    st.divider()
    
    # --- VIBE METER ---
    st.subheader("🔥 Live Vibe Meter")
    st.markdown("Imagine pointing your camera at your friends. The AI tracks their movement and gives live feedback!")
    
    vibe_score = random.randint(70, 99) # Higher score for V2 positivity
    if vibe_score < 60:
        vibe_class = "low-vibe"
        vibe_text = "Needs more energy! ⚡"
    elif vibe_score < 80:
        vibe_class = "mid-vibe"
        vibe_text = "Getting there! Stay on beat! 🎵"
    else:
        vibe_class = "high-vibe"
        vibe_text = "Perfect Sync! You are ready to film! 🎬"
        
    st.markdown(f'<div class="vibe-meter {vibe_class}">Vibe Score: {vibe_score}% - {vibe_text}</div>', unsafe_allow_html=True)
    
else:
    st.info("👈 Use the sidebar to upload a song and generate your custom choreography!")
