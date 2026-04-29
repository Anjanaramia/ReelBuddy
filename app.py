import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import time

# --- MOCK DATABASE OF MOVES ---
MOVES_DB = {
    "Hip Hop": {
        "Beginner": ["The Slide", "Step-Touch", "The Woah", "Shoulder Bounce", "Two-Step"],
        "Intermediate": ["Running Man", "Cabbage Patch", "Spongebob", "Criss Cross"]
    },
    "Bollywood": {
        "Beginner": ["Bhangra Shoulders", "Lightbulb Twist", "Side-to-Side Sway", "Hip Bumps"],
        "Intermediate": ["Thumka", "Jumping Jacks (Desi Style)", "Spin & Clap"]
    },
    "Trendy (TikTok)": {
        "Beginner": ["Hand Hearts", "Body Roll (Simple)", "Point & Look", "Dice Roll"],
        "Intermediate": ["The Smeeze", "Renegade (Shortened)", "Clock Work"]
    }
}

# --- PAGE CONFIG ---
st.set_page_config(page_title="Reel Buddy MVP", page_icon="💃", layout="wide")

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
</style>
""", unsafe_allow_html=True)


# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("💃 Reel Buddy")
st.sidebar.markdown("Generate instant choreography and formations for your group!")

st.sidebar.header("1. Setup your crew")
group_size = st.sidebar.slider("Group Size", min_value=1, max_value=10, value=3)

st.sidebar.header("2. Pick a Vibe")
dance_style = st.sidebar.selectbox("Dance Style", ["Hip Hop", "Trendy (TikTok)", "Bollywood"])
difficulty = st.sidebar.radio("Difficulty Level", ["Beginner", "Intermediate"])

st.sidebar.header("3. Music Setup")
song_vibe = st.sidebar.selectbox("Song Vibe", ["Hype (Fast)", "Chill (Mid-tempo)", "Romantic (Slow)"])

generate_btn = st.sidebar.button("✨ Generate Choreography", use_container_width=True)

# --- MAIN STAGE ---
st.title("🎥 Your Custom Reel Routine")

if generate_btn:
    # Adding a fun loading spinner
    with st.spinner('Analyzing vibe & calculating formations...'):
        time.sleep(1.5)
        
    col1, col2 = st.columns([1, 1])

    # --- FORMATION ENGINE ---
    with col1:
        st.subheader(f"📍 Suggested Formation ({group_size} People)")
        
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_facecolor('#f0f2f6')
        ax.axis('off')
        
        # Calculate positions based on group size
        positions = []
        if group_size == 1:
            positions = [(0, 0)]
        elif group_size == 2:
            positions = [(-1, 0), (1, 0)]
        elif group_size == 3:
            positions = [(0, 1), (-1, -1), (1, -1)] # Triangle
        elif group_size == 4:
            positions = [(0, 1), (-1, 0), (1, 0), (0, -1)] # Diamond
        elif group_size == 5:
            positions = [(0, 1), (-1.5, 0), (1.5, 0), (-0.75, -1), (0.75, -1)] # V-Shape
        else:
            # Random scatter for larger groups (simplified for MVP)
            for _ in range(group_size):
                positions.append((random.uniform(-2, 2), random.uniform(-2, 2)))
                
        # Draw the dancers
        for i, (x, y) in enumerate(positions):
            ax.scatter(x, y, s=1500, c='#FF4B4B', alpha=0.8, edgecolors='white', linewidth=2)
            ax.text(x, y, f"{i+1}", fontsize=14, ha='center', va='center', color='white', fontweight='bold')
            
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        st.pyplot(fig)
        
        st.info("Tip: The numbers represent the dancers. Person 1 is usually the lead!")

    # --- CHOREOGRAPHY SEQUENCE ---
    with col2:
        st.subheader("🎵 Step-by-Step Sequence")
        
        # Select random moves based on style and difficulty
        available_moves = MOVES_DB[dance_style][difficulty]
        # Ensure we have enough moves to sample, allow duplicates if needed
        sequence_length = 4 if song_vibe == "Chill (Mid-tempo)" else 6
        
        # Pick steps
        chosen_steps = [random.choice(available_moves) for _ in range(sequence_length)]
        
        # Display as a timeline
        for idx, step in enumerate(chosen_steps):
            st.markdown(f"**Step {idx+1}:** {step}")
            st.progress((idx+1) / sequence_length)
            
        st.success(f"Perfect sequence for a {song_vibe.lower()} track!")
        
    st.divider()
    
    # --- VIBE METER (MOCKUP) ---
    st.subheader("🔥 Live Vibe Meter (Coming Soon)")
    st.markdown("Imagine pointing your camera at your friends. The AI tracks their movement and gives live feedback!")
    
    vibe_score = random.randint(40, 99)
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
    st.info("👈 Use the sidebar to set up your crew and click **Generate Choreography**!")
    st.image("https://images.unsplash.com/photo-1547153760-18fc86324498?auto=format&fit=crop&q=80&w=800", caption="Ready to dance?")
