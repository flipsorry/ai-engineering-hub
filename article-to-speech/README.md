# Article to Speech Converter

Convert any text or article into natural-sounding speech using AI-powered voice synthesis with Chatterbox TTS. This application allows you to generate high-quality audio from text with optional voice cloning capabilities.

## Features

- 🎯 **Text to Speech** - Convert any text to natural-sounding speech
- 🎤 **Voice Cloning** - Upload reference audio to clone any voice
- ⚡ **Speed Control** - Adjust speaking speed from 0.5x to 2.0x
- 🎛️ **Temperature Control** - Fine-tune speech naturalness and creativity
- 🔊 **High Quality** - Generate crisp, clear audio output
- 💾 **Download** - Save generated audio as WAV files
- 🎨 **Modern UI** - Beautiful Streamlit interface with dark theme

## Installation and Setup

**Prerequisites**:
   Ensure you have Python 3.8 or later installed.

**1. Create Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

**2. Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

**3. Run the Application**:
   ```bash
   # for ubuntu - open up this port first
   # sudo ufw allow 8501
   streamlit run app.py
   ```



## How to Use

1. **Enter Text**: Type or paste your article text in the sidebar text area
2. **Optional Voice Cloning**: Upload a reference audio file (WAV, MP3, M4A, FLAC) to clone that voice
3. **Adjust Settings**: 
   - **Speed**: Control how fast the speech is generated (0.5x - 2.0x)
   - **Temperature**: Control creativity/randomness in speech generation (0.1 - 1.0)
4. **Generate**: Click the "🔊 Generate Speech" button
5. **Play & Download**: Listen to the generated audio and download as WAV file

## Supported Audio Formats

- **Input** (for voice cloning): WAV, MP3, MP4, M4A, FLAC
- **Output**: WAV format (high quality, compatible with all devices)

## Configuration Options

- **Speed**: 0.5 (slow) to 2.0 (fast), default 1.0
- **Temperature**: 0.1 (conservative) to 1.0 (creative), default 0.7
- **Voice Cloning**: Optional reference audio upload for personalized voices

## Requirements

- Python 3.8+
- Streamlit
- Chatterbox TTS
- NumPy
- Wave (built-in Python module)

## Technical Details

The application uses:
- **Chatterbox TTS** for high-quality text-to-speech synthesis
- **Streamlit** for the web interface
- **NumPy** for audio processing
- **Wave module** for WAV file generation
- Local processing (no external API calls required)

## Troubleshooting

1. **Installation Issues**: Make sure you have Python 3.8+ and all dependencies installed
2. **Audio Generation Errors**: Check that your text input is not empty and try adjusting temperature settings
3. **Reference Audio Issues**: Ensure reference audio files are in supported formats (WAV, MP3, M4A, FLAC)
4. **Performance**: For longer texts, generation may take more time - this is normal

---

## 📬 Stay Updated with Our Newsletter!
**Get a FREE Data Science eBook** 📖 with 150+ essential lessons in Data Science when you subscribe to our newsletter! Stay in the loop with the latest tutorials, insights, and exclusive resources. [Subscribe now!](https://join.dailydoseofds.com)

[![Daily Dose of Data Science Newsletter](https://github.com/patchy631/ai-engineering/blob/main/resources/join_ddods.png)](https://join.dailydoseofds.com)

---

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.