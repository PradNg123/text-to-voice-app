import streamlit as st
import edge_tts
import asyncio
import html
import os
import time

OUTPUT_FILE = "output.mp3"

# --- Google Analytics (inline injection) ---
st.markdown("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-13Z4BFNNSD"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-13Z4BFNNSD');
</script>
""", unsafe_allow_html=True)

# Voices dictionary
voices = {
    "Guy": "en-US-GuyNeural",
    "Ryan": "en-GB-RyanNeural",
    "James": "en-US-AndrewNeural",
    "Eric": "en-US-EricNeural",
    "Christopher": "en-US-ChristopherNeural",
    "Jenny": "en-US-JennyNeural",
    "Aria": "en-US-AriaNeural",
    "Libby": "en-GB-LibbyNeural",
    "Ava": "en-US-AvaMultilingualNeural",
    "Emma": "en-US-EmmaMultilingualNeural"
}

# Async TTS function
async def text_to_speech(text, voice):
    text_safe = html.escape(text.strip())
    if not text_safe:
        raise ValueError("Text is empty after stripping spaces.")
    communicate = edge_tts.Communicate(text_safe, voice=voice)
    await communicate.save(OUTPUT_FILE)

# Async runner for Streamlit
def run_async_task(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        return asyncio.create_task(coro)
    else:
        return asyncio.run(coro)

# ------------------ Custom CSS & Animation ------------------ #
st.markdown(
    """
    <style>
    /* Background gradient */
    body {
        background: linear-gradient(135deg, #89f7fe, #66a6ff);
    }

    /* Animated title */
    .animated-title {
        font-size: 50px;
        font-weight: bold;
        background: linear-gradient(270deg, #ff4b4b, #ffb84b, #4bffb8, #4b8bff);
        background-size: 800% 800%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientBG 10s ease infinite;
        text-align: center;
    }

    @keyframes gradientBG {
        0%{background-position:0% 50%}
        50%{background-position:100% 50%}
        100%{background-position:0% 50%}
    }

    /* Subtitle animation */
    .animated-subtitle {
        font-size: 24px;
        text-align: center;
        color: #fff;
        margin-bottom: 30px;
        animation: fadeIn 3s ease;
    }

    @keyframes fadeIn {
        0%{opacity:0}
        100%{opacity:1}
    }

    /* Button styling */
    .stButton>button {
        background-color:#ff4b4b; 
        color:white; 
        font-size:18px; 
        border-radius:12px;
        padding:10px 20px;
    }

    /* Footer */
    .footer {
        text-align:center;
        padding:20px;
        font-size:16px;
        color:#fff;
        margin-top:50px;
        background-color: rgba(0,0,0,0.2);
        border-radius:12px;
    }
    </style>
    """, unsafe_allow_html=True
)

# ------------------ Header ------------------ #
st.markdown('<p class="animated-title">🎙️ Voice Magic TTS</p>', unsafe_allow_html=True)
st.markdown('<p class="animated-subtitle">Convert text into beautiful voices instantly!</p>', unsafe_allow_html=True)

# User input
text = st.text_area("Enter your text here:")
voice_choice = st.selectbox("Choose Voice", list(voices.keys()))

# Convert button with progress
if st.button("Convert to Speech"):
    if not text.strip():
        st.warning("⚠️ Please enter some text.")
    else:
        voice = voices[voice_choice]

        # Progress bar
        progress_text = st.empty()
        progress_bar = st.progress(0)
        try:
            for i in range(0, 101, 10):
                progress_text.text(f"Generating speech... {i}%")
                progress_bar.progress(i)
                time.sleep(0.05)  # visual progress

            # Run TTS
            run_async_task(text_to_speech(text, voice))

            progress_bar.progress(100)
            progress_text.text("✅ Conversion Complete!")

            # Show audio player
            st.audio(OUTPUT_FILE, format="audio/mp3")

            # Download button
            with open(OUTPUT_FILE, "rb") as f:
                st.download_button(
                    label="📥 Download MP3",
                    data=f,
                    file_name="voice_output.mp3",
                    mime="audio/mp3"
                )

        except Exception as e:
            st.error(f"❌ Error generating speech: {e}")

# ------------------ Footer ------------------ #
st.markdown('<div class="footer">Made with ❤️ using Python & Edge-TTS | Your TTS Companion</div>', unsafe_allow_html=True)
