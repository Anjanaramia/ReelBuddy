import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import time

# --- DATABASE OF MOVES WITH YOUTUBE TIMESTAMPS ---
# For the MVP, we use placeholder YouTube links (famous music videos/tutorials) 
# and start times to simulate exactly how video learning works.
# Using universally embeddable non-copyrighted test videos (Big Buck Bunny) so YouTube doesn't block it on Streamlit Cloud!
MOVES_DB = {
    "Hindi/Bollywood": {
        "Beginner": [
            {"name": "Thumka", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 45},
            {"name": "Lightbulb Twist", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 70},
            {"name": "Shoulder Drop", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 90}
        ]
    },
    "Punjabi": {
        "Beginner": [
            {"name": "Bhangra Shoulders", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 105},
            {"name": "Double Clap", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 120},
            {"name": "Foot Tap", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 135}
        ]
    },
    "Tamil (Kuthu)": {
        "Beginner": [
            {"name": "Local Kuthu Step", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 150},
            {"name": "Whistle Podu", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 165},
            {"name": "Shirt Collar Dust", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 180}
        ]
    },
    "Telugu (Teen Maar)": {
        "Beginner": [
            {"name": "Teen Maar Beat", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 195},
            {"name": "Hand Spin", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 210},
            {"name": "Jump Step", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 225}
        ]
    },
    "Kannada": {
        "Beginner": [
            {"name": "Sandalwood Sway", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 50},
            {"name": "Folk Step", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 80}
        ]
    },
    "American Pop/Hip Hop": {
        "Beginner": [
            {"name": "The Slide", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 60},
            {"name": "The Woah", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 75},
            {"name": "Two-Step", "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "start_time": 90}
        ]
    }
}

# --- PAGE CONFIG ---
st.set_page_config(page_title="Reel Buddy V3", page_icon="🎵", layout="wide")

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
</style>
""", unsafe_allow_html=True)


# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("🎵 Reel Buddy V3")
st.sidebar.markdown("Instant Spotify Search & YouTube Choreography!")

st.sidebar.header("1. Find your Song")
# Replaced Audio Uploader with Spotify Search
spotify_query = st.sidebar.text_input("🔍 Search Spotify (e.g., 'Naatu Naatu')", placeholder="Type song name...")

st.sidebar.header("2. Setup your crew")
group_size = st.sidebar.slider("Group Size", min_value=1, max_value=10, value=3)

st.sidebar.header("3. Pick a Style")
dance_style = st.sidebar.selectbox("Regional Style", list(MOVES_DB.keys()))

generate_btn = st.sidebar.button("✨ Generate Choreography", use_container_width=True)

# --- MOCK SPOTIFY API FUNCTION ---
def mock_spotify_search(query):
    time.sleep(1) # Simulate API request
    # Return a mocked BPM based on length of the query to make it seem dynamic
    return 90 + (len(query) * 5 % 60)


# --- MAIN STAGE ---
st.title("🎥 Your Custom Reel Routine")

if generate_btn:
    if not spotify_query:
        st.warning("Please type a song name into the Spotify Search bar first!")
        st.stop()
        
    with st.spinner('Searching Spotify & Generating Choreography...'):
        bpm = mock_spotify_search(spotify_query)
        time.sleep(1)
        
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

    # --- VIDEO CHOREOGRAPHY SEQUENCE ---
    with col2:
        st.subheader(f"🎬 Video Sequence ({dance_style})")
        
        available_moves = MOVES_DB[dance_style]["Beginner"]
        sequence_length = 4
        
        # Pick steps
        chosen_steps = [random.choice(available_moves) for _ in range(sequence_length)]
        
        # Display YouTube videos for each step
        for idx, step in enumerate(chosen_steps):
            st.markdown(f"""
            <div class="step-card">
                <h4>Step {idx+1}: {step['name']}</h4>
            </div>
            """, unsafe_allow_html=True)
            # Use Streamlit's native video player with the YouTube URL and start_time
            st.video(step['youtube_url'], start_time=step['start_time'])
            
        st.info("💡 Tip: The YouTube clips are queued exactly to the timestamp of the dance move!")
        
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
