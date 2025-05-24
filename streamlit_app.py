import streamlit as st
import requests
from openai import OpenAI

# === CONFIG ===
st.set_page_config(page_title="AI Content + Video Script Studio", layout="centered")

# === API SETUP ===
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

VOICES = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Antoni": "ErXwobaYiN019PkySvjV",
    "Alice": "Xb7hH8MSUJpSbSDYk0k2"
}
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]

# === SESSION STATE ===
if "script_text" not in st.session_state:
    st.session_state.script_text = ""
if "voice_audio" not in st.session_state:
    st.session_state.voice_audio = None

# === UTILS ===
def limit_words(text, max_words=250):
    return ' '.join(text.split()[:max_words])

def generate_prompt(topic, audience, tone, message, max_words):
    return (
        f"You are a viral video script writer.\n"
        f"Write a short-form script only, using under {max_words} words without adding any personal comment. "
        f"Don't add any scene sequence, and don't write Here's is a script and remove any [] comment.\n"
        f"Topic: {topic}\nTarget Audience: {audience}\nTone: {tone}\nMessage: {message}"
    )

def export_txt(script):
    return script.encode("utf-8")

def export_srt(script):
    lines = script.split(". ")
    srt = ""
    for i, line in enumerate(lines):
        srt += f"{i+1}\n00:00:{i:02d},000 --> 00:00:{i+2:02d},000\n{line.strip()}\n\n"
    return srt.encode("utf-8")

# === INTERFACE ===

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("💡 Describe your idea", key="topic")
    tone = st.selectbox("🎤 Tone", ["Direct", "Funny", "Emotional", "Educational", "Motivational"], key="tone")
    voice_choice = st.selectbox("🗣️ Select Voice", list(VOICES.keys()))
with col2:
    audience = st.text_input("🎯 Target audience", key="audience")
    message = st.text_input("📝 Additional notes", key="message")
    length_choice = st.selectbox("📏 Script Length", ["Standard (150 words)", "Extended (300 words)"])

max_words = 300 if "Extended" in length_choice else 150

btn1, btn2 = st.columns(2)
with btn1:
    if st.button("✨ Generate Script"):
        prompt = generate_prompt(topic, audience, tone, message, max_words)
        with st.spinner("Generating script..."):
            try:
                res = client.chat.completions.create(
                    model="meta-llama/llama-3-8b-instruct",
                    messages=[
                        {"role": "system", "content": "You are a professional viral content creator."},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.session_state.script_text = res.choices[0].message.content.strip()
                st.success("✅ Script ready!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
with btn2:
    disabled = not st.session_state.script_text.strip()
    if st.button("🎧 Generate Voice", disabled=disabled):
        with st.spinner("Generating voice..."):
            try:
                tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[voice_choice]}"
                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": ELEVENLABS_API_KEY
                }
                data = {
                    "text": st.session_state.script_text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
                }
                response = requests.post(tts_url, headers=headers, json=data)
                if response.status_code == 200:
                    with open("output_voice.mp3", "wb") as f:
                        f.write(response.content)
                    st.session_state.voice_audio = "output_voice.mp3"
                    st.success("✅ Voice ready!")
                else:
                    st.error("❌ Voice generation failed.")
            except Exception as e:
                st.error(f"❌ Voice generation error: {e}")

if st.session_state.script_text:
    st.markdown("### 📝 Script Output")
    st.code(st.session_state.script_text)
    st.download_button("⬇️ Download .txt", data=export_txt(st.session_state.script_text), file_name="script.txt")
    st.download_button("⬇️ Download .srt", data=export_srt(st.session_state.script_text), file_name="script.srt")

if st.session_state.voice_audio:
    st.markdown("### 🔊 Voice Output")
    st.audio(st.session_state.voice_audio, format="audio/mp3")
    with open(st.session_state.voice_audio, "rb") as f:
        st.download_button("⬇️ Download Voice", data=f, file_name="voice.mp3", mime="audio/mpeg")
