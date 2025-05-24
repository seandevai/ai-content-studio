# AI Content + Video Script Studio

This app allows users to generate short-form video scripts and turn them into voiceover audio using AI. It is ideal for TikTok, Reels, and YouTube Shorts creators, marketers, and educators.

## Features
- Generate viral video scripts in seconds
- Choose tone, target audience, and message
- Convert scripts into audio with AI voices
- Download as .mp3, .txt, or .srt

## Setup

1. Clone the repository
2. Add your API keys in `.streamlit/secrets.toml`:

```
[general]
OPENROUTER_API_KEY = "your-openrouter-api-key"
ELEVENLABS_API_KEY = "your-elevenlabs-api-key"
```

3. Run the app:
```
streamlit run streamlit_app.py
```

Deploy on [Streamlit Cloud](https://streamlit.io/cloud) for free.