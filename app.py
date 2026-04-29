import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import base64
import os

# --- DATABASE OF MOVES ---
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

STYLE_IMAGE_MAP = {
    "Hindi/Bollywood": "bollywood.png",
    "Punjabi": "punjabi.png",
    "Tamil (Kuthu)": "south_indian.png",
    "Telugu (Teen Maar)": "south_indian.png",
    "Kannada": "south_indian.png",
    "American Pop/Hip Hop": "hiphop.png"
}

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

# --- PAGE CONFIG ---
st.set_page_config(page_title="Reel Buddy V4", page_icon="💃", layout="wide")

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
    padding: 15px;
    margin-bottom: 20px;
    text-align: center;
}
.spotify-box {
    background-color: #1DB954;
    color: white;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
    margin-bottom: 15px;
}
@keyframes dance {
    0% { transform: translateY(0) rotate(0deg) scale(1); }
    25% { transform: translateY(-10px) rotate(-3deg) scale(1.02); }
    50% { transform: translateY(0) rotate(0deg) scale(1); }
    75% { transform: translateY(-10px) rotate(3deg) scale(1.02); }
    100% { transform: translateY(0) rotate(0deg) scale(1); }
}
.ai-dancer {
    display: inline-block;
    animation-name: dance;
    animation-iteration-count: infinite;
    animation-timing-function: ease-in-out;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    width: 100%;
    max-width: 300px;
}
</style>
""", unsafe_allow_html=True)


# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("💃 Reel Buddy V4")
st.sidebar.markdown("AI Character Choreography!")

st.sidebar.header("1. Find your Song")
spotify_query = st.sidebar.text_input("🔍 Search Spotify (e.g., 'Naatu Naatu')", placeholder="Type song name...")

st.sidebar.header("2. Setup your crew")
group_size = st.sidebar.slider("Group Size", min_value=1, max_value=10, value=3)

st.sidebar.header("3. Pick a Style")
dance_style = st.sidebar.selectbox("Regional Style", list(MOVES_DB.keys()))

generate_btn = st.sidebar.button("✨ Generate AI Choreography", use_container_width=True)

# --- MOCK SPOTIFY API FUNCTION ---
def mock_spotify_search(query):
    time.sleep(1) # Simulate API request
    return 90 + (len(query) * 5 % 60)

# --- MAIN STAGE ---
st.title("🎥 Your Custom AI Reel Routine")

if generate_btn:
    if not spotify_query:
        st.warning("Please type a song name into the Spotify Search bar first!")
        st.stop()
        
    with st.spinner('Generating AI Characters & Syncing to Beat...'):
        bpm = mock_spotify_search(spotify_query)
        time.sleep(1.5)
        
    st.markdown(f'<div class="spotify-box">🎧 Spotify API Match: "{spotify_query}" | Detected BPM: {bpm}</div>', unsafe_allow_html=True)
        
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

    # --- AI CHARACTER CHOREOGRAPHY SEQUENCE ---
    with col2:
        st.subheader(f"🎬 AI Choreography ({dance_style})")
        
        available_moves = MOVES_DB[dance_style]["Beginner"]
        sequence_length = 3
        
        chosen_steps = [random.choice(available_moves) for _ in range(sequence_length)]
        
        # Load the corresponding AI image
        img_filename = STYLE_IMAGE_MAP.get(dance_style, "hiphop.png")
        img_path = os.path.join("assets", img_filename)
        img_b64 = get_base64_of_bin_file(img_path)
        
        if img_b64:
            img_html = f'<img src="data:image/png;base64,{img_b64}" class="ai-dancer" style="animation-duration: {60/bpm}s;">'
        else:
            img_html = f'<div class="ai-dancer" style="font-size:80px; animation-duration: {60/bpm}s;">🕺</div>'
        
        for idx, step in enumerate(chosen_steps):
            st.markdown(f"""
            <div class="step-card">
                <h4 style="margin-bottom: 15px;">Step {idx+1}: {step}</h4>
                {img_html}
            </div>
            """, unsafe_allow_html=True)
            
        st.success("✨ AI Characters successfully generated and synced to BPM!")
        
    st.divider()
    
    # --- VIBE METER ---
    st.subheader("🔥 Live Vibe Meter")
    st.markdown("Imagine pointing your camera at your friends. The AI tracks their movement and gives live feedback!")
    
    vibe_score = random.randint(70, 99)
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
    st.info("👈 Use the sidebar to search for a song and generate your custom choreography!")
