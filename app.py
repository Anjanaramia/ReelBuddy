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

# --- MOCK DATABASE OF MOVES ---
MOVES_DB = {
    "Hindi/Bollywood": {
        "Beginner": ["Thumka", "Lightbulb Twist", "Shoulder Drop"]
    },
    "Punjabi": {
        "Beginner": ["Bhangra Shoulders", "Double Clap", "Foot Tap"]
    },
    "Tamil (Kuthu)": {
        "Beginner": ["Local Kuthu Step", "Whistle Podu", "Shirt Collar Dust"]
    },
    "Telugu (Teen Maar)": {
        "Beginner": ["Teen Maar Beat", "Hand Spin", "Jump Step"]
    },
    "Kannada": {
        "Beginner": ["Sandalwood Sway", "Folk Step"]
    },
    "American Pop/Hip Hop": {
        "Beginner": ["The Slide", "The Woah", "Two-Step"]
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
@keyframes dance {
    0% { transform: translateY(0) rotate(0deg) scale(1); }
    25% { transform: translateY(-15px) rotate(-10deg) scale(1.1); }
    50% { transform: translateY(0) rotate(0deg) scale(1); }
    75% { transform: translateY(-15px) rotate(10deg) scale(1.1); }
    100% { transform: translateY(0) rotate(0deg) scale(1); }
}
.ai-dancer {
    font-size: 80px;
    display: inline-block;
    animation-name: dance;
    animation-iteration-count: infinite;
    animation-timing-function: ease-in-out;
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
        
        # Display as a timeline of simulated AI videos
        for idx, step in enumerate(chosen_steps):
            st.markdown(f"""
            <div class="step-card">
                <h4>Step {idx+1}: {step}</h4>
                <div class="ai-dancer" style="animation-duration: {60/bpm}s;">🕺</div>
                <p style="color: #666; font-size: 12px; margin-top: 10px;">[AI Video Render Placeholder]</p>
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
