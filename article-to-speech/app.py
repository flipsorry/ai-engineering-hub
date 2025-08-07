import streamlit as st
import uuid
import gc
import base64
from pathlib import Path
import os
import io
import numpy as np
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

# Configure page
st.set_page_config(
    page_title="Article to Speech Converter",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}
    st.session_state.generated_audio = None
    st.session_state.paragraph_audios = []  # Store multiple audio files for paragraphs

# Pre-load TTS model on startup
@st.cache_resource
def initialize_tts_model():
    """Initialize and cache the TTS model on startup"""
    try:
        with st.spinner("Loading TTS model... This may take a moment on first run."):
            # Auto-detect best available device for MacBook M1
            import torch
            if torch.backends.mps.is_available():
                device = "mps"  # Use Metal Performance Shaders for M1 Macs
                st.info("🚀 Using MPS (Metal Performance Shaders) for acceleration")
            elif torch.cuda.is_available():
                device = "cuda"  # Use CUDA if available
                st.info("🚀 Using CUDA for acceleration")
            else:
                device = "cpu"  # Fallback to CPU
                st.info("💻 Using CPU (slower but compatible)")
            
            model = ChatterboxTTS.from_pretrained(device=device)
            st.success("✅ TTS model loaded successfully!")
            model.prepare_conditionals(wav_fpath="dave_limo.mp3")
            st.success("✅ TTS model prepared successfully!")
            return model
    except Exception as e:
        st.error(f"Error loading TTS model: {str(e)}")
        return None

# Load model on startup
if "tts_model_loaded" not in st.session_state:
    st.session_state.tts_model = initialize_tts_model()
    st.session_state.tts_model_loaded = True

# Application styling with dark theme (reusing similar styling from audio-analysis-toolkit)
st.markdown("""
<style>
/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #23272f !important;
    padding-top: 2rem !important;
    position: static !important;
}

/* Sidebar section headers */
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3, 
section[data-testid="stSidebar"] label {
    color: #fff !important;
    font-weight: 700 !important;
    margin-bottom: 1rem !important;
    margin-top: 1.5rem !important;
    letter-spacing: 0.01em;
}

/* File uploader dropzone and file list */
section[data-testid="stSidebar"] .stFileUploader > div,
section[data-testid="stSidebar"] .stFileUploader [data-testid="stFileUploaderDropzone"] {
    background-color: #111215 !important;
    color: #fff !important;
    border-radius: 12px !important;
    border: none !important;
    margin-bottom: 1rem !important;
    padding: 1.25rem 1rem !important;
    box-shadow: none !important;
}

/* Uploaded file display */
section[data-testid="stSidebar"] .stFileUploader [data-testid="stFileUploaderFileContainer"] {
    background-color: #181a1f !important;
    color: #fff !important;
    border-radius: 8px !important;
    border: 1px solid #23272f !important;
    margin-top: 0.5rem !important;
    margin-bottom: 1rem !important;
    padding: 0.5rem 0.75rem !important;
}

/* Remove white patch at the top of the main area */
div.stApp, .block-container, .main, .main > div:first-child, .st-emotion-cache-uf99v8, .st-emotion-cache-1wrcr25, .st-emotion-cache-18ni7ap {
    background-color: #111215 !important;
    background: #111215 !important;
}

/* Remove unwanted top margin/padding */
.block-container, .main, .main > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Aggressive reset for top white patch */
html, body, #root, .stApp {
    background-color: #111215 !important;
    background: #111215 !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    min-height: 100vh !important;
    height: 100% !important;
}

header[data-testid="stHeader"] {
    background: #111215 !important;
    background-color: #111215 !important;
    box-shadow: none !important;
    border: none !important;
    min-height: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    opacity: 0 !important;
    display: none !important;
}

/* Center main content vertically with flexbox */
div.stApp {
    display: flex !important;
    flex-direction: column !important;
    min-height: 100vh !important;
}
.block-container {
    max-width: 1100px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    margin-top: 4rem !important;
    min-height: 80vh !important;
}

/* Feature cards */
.metric-card {
    background-color: #23272f !important;
    border-radius: 12px !important;
    color: #fff !important;
    border: none !important;
    padding: 1.5rem !important;
    margin-bottom: 2.5rem !important;
    box-shadow: 0 2px 16px 0 rgba(0,0,0,0.12) !important;
}

.section-card {
    background: none !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

.welcome-card {
    background: none !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

/* Main header styling */
.main-header {
    font-size: 2.8rem !important;
    letter-spacing: 0.02em !important;
    margin-bottom: 2.5rem !important;
    text-align: center !important;
}

/* Feature cards: equal dimensions and flex layout */
.cards-row {
    display: flex;
    gap: 2rem;
    justify-content: center;
    margin-top: 2.5rem;
}
.metric-card {
    min-width: 300px !important;
    max-width: 340px !important;
    min-height: 140px !important;
    flex: 1 1 0 !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: flex-start !important;
    box-sizing: border-box !important;
}

/* General text color */
body, .stApp, .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader, .stDataFrame {
    color: #fff !important;
}

/* Main header visibility */
.main-header, h1.main-header, .stMarkdown h1 {
    color: #fff !important;
    font-weight: 800 !important;
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
    letter-spacing: 0.02em;
}

/* Welcome heading in main area */
.welcome-card h3, .welcome-card p, .welcome-card ul, .welcome-card li {
    color: #fff !important;
}

/* Card names/titles */
.metric-card h4, .metric-card p {
    color: #fff !important;
}

/* Force all headings to be white */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp .stSubheader, .stApp .stMarkdown h2, .stApp .stMarkdown h3, .stApp .stMarkdown h4 {
    color: #fff !important;
}

/* Sliders and controls */
.stSlider label {
    color: #fff !important;
}

.stNumberInput label {
    color: #fff !important;
}

.stSelectbox label {
    color: #fff !important;
}

.stTextArea label {
    color: #fff !important;
}

/* Status messages */
.stSuccess, .stError, .stWarning, .stInfo {
    color: #fff !important;
}

/* Spacing between sidebar elements */
section[data-testid="stSidebar"] > div {
    margin-bottom: 1.5rem !important;
}
</style>
""", unsafe_allow_html=True)

def get_logo_base64():
    """Convert logo file to base64 string for embedding"""
    logo_path = Path("assets/logo.png")
    
    if logo_path.exists():
        try:
            with open(logo_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception:
            return ""
    
    return ""

def split_text_into_paragraphs(text):
    """Split text into paragraphs based on double line breaks or single line breaks"""
    # Split by double line breaks first
    paragraphs = text.split('\n\n')
    
    # If no double line breaks, split by single line breaks
    if len(paragraphs) == 1:
        paragraphs = text.split('\n')
    
    # Clean up paragraphs (remove empty ones and strip whitespace)
    cleaned_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if para:  # Only add non-empty paragraphs
            cleaned_paragraphs.append(para)
    
    return cleaned_paragraphs

def reset_session():
    """Reset session"""
    st.session_state.generated_audio = None
    st.session_state.paragraph_audios = []
    gc.collect()



def generate_speech(text, reference_audio=None, exaggeration=0.5, cfg_weight=0.5):
    """Generate speech from text using Chatterbox TTS"""
    try:
        # Use pre-loaded model from session state
        model = st.session_state.get("tts_model")
        if model is None:
            st.error("TTS model not loaded. Please refresh the page.")
            return None, None
        
        if reference_audio is not None:
            # Use reference audio for voice cloning
            # Save reference audio to temp file
            temp_path = "temp_reference.wav"
            with open(temp_path, "wb") as f:
                f.write(reference_audio.read())
            
            # Generate speech with reference
            wav = model.generate(text, audio_prompt_path=temp_path, exaggeration=exaggeration, cfg_weight=cfg_weight)
            
            # Clean up temp file
            os.remove(temp_path)
        else:
            # Generate with default voice
            wav =  model.generate(text,
                                  # Since we already called prepare_conditionals() we don't need to tell it the path
                                  # , audio_prompt_path="dave_limo.mp3",
                                  exaggeration=exaggeration,
                                  cfg_weight=cfg_weight)
        
        return wav, model.sr
    
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None, None

def save_audio_to_wav(audio_tensor, sample_rate):
    """Convert audio tensor to WAV format using torchaudio"""
    try:
        # Create temporary file
        temp_path = f"temp_audio_{uuid.uuid4()}.wav"
        
        # Save using torchaudio
        ta.save(temp_path, audio_tensor, sample_rate)
        
        # Read file into memory
        with open(temp_path, 'rb') as f:
            wav_data = f.read()
        
        # Clean up temp file
        os.remove(temp_path)
        
        return wav_data
    
    except Exception as e:
        st.error(f"Error converting audio to WAV: {str(e)}")
        return None

def main():
    # Sidebar
    with st.sidebar:
        # Logo placeholder
        logo_base64 = get_logo_base64()
        if logo_base64:
            st.markdown(f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_base64}" class="logo-image-large" alt="Logo">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="logo-container">
                <div class="logo-placeholder-large">🔊</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Add separator
        st.markdown('<div style="border-bottom: 1px solid var(--border-color); margin: 1rem 0;"></div>', unsafe_allow_html=True)
        
        st.markdown('<h2 class="sidebar-header">Text to Speech Configuration</h2>', unsafe_allow_html=True)
        
        # Text input
        default_text = """The most common unscalable thing founders have to do at the start is to recruit users manually. Nearly all startups have to. You can't wait for users to come to you. You have to go out and get them.

Stripe is one of the most successful startups we've funded, and the problem they solved was an urgent one. If anyone could have sat back and waited for users, it was Stripe. But in fact they're famous within YC for aggressive early user acquisition.

Startups building things for other startups have a big pool of potential users in the other companies we've funded, and none took better advantage of it than Stripe. At YC we use the term "Collison installation" for the technique they invented. More diffident founders ask "Will you try our beta?" and if the answer is yes, they say "Great, we'll send you a link." But the Collison brothers weren't going to wait. When anyone agreed to try Stripe they'd say "Right then, give me your laptop" and set them up on the spot."""

        text_input = st.text_area(
            "Enter text to convert to speech",
            value=default_text,
            height=150,
            help="Enter the text you want to convert to speech. Each paragraph will be converted to a separate audio file."
        )
        
        # Reference audio upload (optional)
        st.markdown("### Voice Cloning (Optional)")
        reference_audio = st.file_uploader(
            "Upload reference audio for voice cloning",
            type=['wav', 'mp3', 'mp4', 'm4a', 'flac'],
            help="Upload an audio file to clone the voice. Leave empty to use default voice."
        )
        
        if reference_audio is not None:
            st.success("Reference audio uploaded!")
            st.audio(reference_audio)
        
        # Generation parameters
        st.markdown("### Generation Settings")
        
        exaggeration = st.slider(
            "Exaggeration",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="Control the speaking speed"
        )
        
        cfg_weight = st.slider(
            "CFG Weight",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="Control the creativity/randomness in speech generation"
        )
        
        # Generate button
        generate_button = st.button(
            "🔊 Generate Speech",
            use_container_width=True,
            type="primary"
        )
        
        # Reset button
        if st.button("🔄 Reset", use_container_width=True):
            reset_session()
    
    # Main content area
    st.markdown('<h1 class="main-header">🔊 Article to Speech Converter</h1>', unsafe_allow_html=True)
    
    if not text_input:
        # Welcome screen
        st.markdown('<div class="bullet-section">', unsafe_allow_html=True)
        st.markdown("""
        <div class="welcome-card">
            <h3>🔊 Welcome to Article to Speech Converter</h3>
            <p>Convert your text to natural-sounding speech using AI-powered voice synthesis:</p>
            <ul>
                <li>📝 <strong>Paragraph Processing</strong> - Each paragraph becomes a separate audio file</li>
                <li>🎯 <strong>Text Input</strong> - Enter any text or article to convert</li>
                <li>🎤 <strong>Voice Cloning</strong> - Upload reference audio to clone any voice</li>
                <li>⚡ <strong>Exaggeration Control</strong> - Adjust speaking speed to your preference</li>
                <li>🎛️ <strong>CFG Weight Control</strong> - Fine-tune speech naturalness</li>
                <li>🔊 <strong>High Quality</strong> - Generate crisp, clear audio output</li>
                <li>💾 <strong>Download</strong> - Save generated audio as WAV files</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add feature cards at the bottom
        st.markdown("""
        <div class="cards-row" style="margin-top: 3rem;">
            <div class="metric-card">
                <h4>📝 Paragraph Processing</h4>
                <p>Each paragraph becomes a separate audio file with individual controls</p>
            </div>
            <div class="metric-card">
                <h4>🎤 Voice Cloning</h4>
                <p>Upload any audio clip to clone the voice and speaking style</p>
            </div>
            <div class="metric-card">
                <h4>⚡ Fast Generation</h4>
                <p>Convert text to speech in seconds with local processing</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Split text into paragraphs
        paragraphs = split_text_into_paragraphs(text_input)
        
        # Show text preview
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📝 Text Preview")
        st.markdown(f"**Text length:** {len(text_input)} characters")
        st.markdown(f"**Number of paragraphs:** {len(paragraphs)}")
        
        with st.expander("View paragraphs", expanded=False):
            for i, para in enumerate(paragraphs, 1):
                st.markdown(f"**Paragraph {i}:**")
                st.write(para)
                st.markdown("---")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate speech when button is clicked
        if generate_button and text_input:
            with st.spinner(f'🔄 Generating speech for {len(paragraphs)} paragraphs... This may take a moment.'):
                try:
                    paragraph_audios = []
                    
                    # Generate speech for each paragraph
                    for i, paragraph in enumerate(paragraphs, 1):
                        with st.spinner(f'Generating audio for paragraph {i}/{len(paragraphs)}...'):
                            # Generate speech for this paragraph
                            audio_tensor, sample_rate = generate_speech(
                                paragraph,
                                reference_audio=reference_audio,
                                exaggeration=exaggeration,
                                cfg_weight=cfg_weight
                            )
                            
                            if audio_tensor is not None and sample_rate is not None:
                                # Convert to WAV format
                                wav_data = save_audio_to_wav(audio_tensor, sample_rate)
                                
                                if wav_data is not None:
                                    paragraph_audios.append({
                                        'paragraph': paragraph,
                                        'audio_data': wav_data,
                                        'paragraph_number': i
                                    })
                                else:
                                    st.error(f"Failed to convert paragraph {i} to WAV format")
                            else:
                                st.error(f"Failed to generate speech for paragraph {i}")
                    
                    if paragraph_audios:
                        st.session_state.paragraph_audios = paragraph_audios
                        st.success(f'✅ Speech generated successfully for {len(paragraph_audios)} paragraphs!')
                    else:
                        st.error("Failed to generate any audio files")
                        
                except Exception as e:
                    import traceback
                    print(f"Exception: {e}")
                    print(f"Traceback: {traceback.format_exc()}")
                    st.error(f"Error during speech generation: {str(e)}")
        
        # Display generated audio for each paragraph if available
        if st.session_state.paragraph_audios:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("🔊 Generated Audio by Paragraph")
            
            for audio_item in st.session_state.paragraph_audios:
                with st.container():
                    st.markdown(f"**Paragraph {audio_item['paragraph_number']}:**")
                    
                    # Show paragraph text (truncated if too long)
                    paragraph_text = audio_item['paragraph']
                    if len(paragraph_text) > 100:
                        st.markdown(f"*{paragraph_text[:100]}...*")
                        with st.expander("Show full paragraph"):
                            st.write(paragraph_text)
                    else:
                        st.markdown(f"*{paragraph_text}*")
                    
                    # Audio player
                    st.audio(audio_item['audio_data'], format="audio/wav")
                    
                    # Download button for this paragraph
                    st.download_button(
                        label=f"💾 Download Paragraph {audio_item['paragraph_number']}",
                        data=audio_item['audio_data'],
                        file_name=f"paragraph_{audio_item['paragraph_number']}_{st.session_state.id}.wav",
                        mime="audio/wav",
                        use_container_width=True
                    )
                    
                    st.markdown("---")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()