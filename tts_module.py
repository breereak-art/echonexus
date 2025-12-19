"""
Text-to-Speech Module for EchoWorld Nexus
Generates audio guidance with ethical watermarks
"""

import os
import io
import tempfile
from typing import Optional
from gtts import gTTS


def generate_audio_guidance(
    text: str,
    language: str = "en",
    include_watermark: bool = True
) -> Optional[bytes]:
    """
    Generate audio guidance from text using gTTS
    
    Args:
        text: The guidance text to convert to speech
        language: Language code (default: en)
        include_watermark: Whether to add ethical disclaimer
        
    Returns:
        Audio bytes or None if failed
    """
    
    if include_watermark:
        watermark = "Note: This is a simulated financial planning tool. "
        full_text = watermark + text
    else:
        full_text = text
    
    try:
        # Limit text length to prevent API issues
        if len(full_text) > 400:
            full_text = full_text[:400]
        
        tts = gTTS(text=full_text, lang=language, slow=False, tld='com')
        
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        audio_data = audio_buffer.getvalue()
        
        # Verify we got valid audio data
        if audio_data and len(audio_data) > 100:
            return audio_data
        else:
            print(f"TTS returned invalid data: {len(audio_data)} bytes")
            return None
        
    except Exception as e:
        print(f"TTS Error: {e}")
        return None


def generate_audio_file(
    text: str,
    output_path: str,
    language: str = "en",
    include_watermark: bool = True
) -> bool:
    """
    Generate audio guidance and save to file
    
    Args:
        text: The guidance text
        output_path: Where to save the MP3 file
        language: Language code
        include_watermark: Whether to add ethical disclaimer
        
    Returns:
        True if successful, False otherwise
    """
    
    if include_watermark:
        watermark = "Note: This is a simulated financial planning tool. "
        full_text = watermark + text
    else:
        full_text = text
    
    try:
        tts = gTTS(text=full_text, lang=language, slow=False)
        tts.save(output_path)
        return True
    except Exception as e:
        print(f"TTS Save Error: {e}")
        return False


def get_language_for_country(country: str) -> str:
    """Get appropriate language code for a country"""
    language_map = {
        "Germany": "en",
        "Japan": "en",
        "France": "en",
        "Spain": "en",
        "Italy": "en",
    }
    return language_map.get(country, "en")


def generate_intro_audio(country: str, city: str) -> Optional[bytes]:
    """Generate intro greeting audio"""
    
    intro_text = (
        f"Hello! This is your Financial Guardian calling from {city}, {country}. "
        f"I've completed analyzing your financial simulation and I'm ready to share my insights. "
        f"Please listen carefully as I walk you through your personalized financial guidance."
    )
    
    return generate_audio_guidance(intro_text, include_watermark=False)


def generate_summary_audio(
    approval_rate: float,
    potential_savings: float,
    best_path: str,
    success_prob: float
) -> Optional[bytes]:
    """Generate quick summary audio"""
    
    summary_text = (
        f"Quick summary: Your approval rate is {approval_rate:.0f} percent. "
        f"Potential savings identified: {potential_savings:.0f} euros. "
        f"Recommended path: {best_path}. "
        f"Success probability: {success_prob:.0f} percent. "
        f"For detailed guidance, click the full audio report button."
    )
    
    return generate_audio_guidance(summary_text, include_watermark=True)


def estimate_audio_duration(text: str) -> float:
    """Estimate audio duration in seconds (rough estimate: 150 words per minute)"""
    word_count = len(text.split())
    return (word_count / 150) * 60
