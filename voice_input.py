"""
Voice Input Module for EchoWorld Nexus
Enables conversational financial guidance interaction through speech recognition
"""

import os
import io
import json
import base64
from typing import Dict, Any, Optional, List
from datetime import datetime


def get_openai_client():
    """Get OpenAI client for Whisper transcription"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except Exception:
        return None


def transcribe_audio(audio_bytes: bytes, language: str = "en") -> Dict[str, Any]:
    """
    Transcribe audio using OpenAI Whisper API
    
    Args:
        audio_bytes: Audio data in bytes
        language: Language code for transcription
        
    Returns:
        Dictionary with transcription result
    """
    
    client = get_openai_client()
    
    if not client:
        return {
            "success": False,
            "error": "OpenAI API not configured",
            "text": ""
        }
    
    try:
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"
        
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language
        )
        
        return {
            "success": True,
            "text": response.text,
            "language": language,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "text": ""
        }


def parse_financial_query(text: str) -> Dict[str, Any]:
    """
    Parse transcribed text to extract financial query intent
    
    Args:
        text: Transcribed text from speech
        
    Returns:
        Dictionary with parsed intent and entities
    """
    
    text_lower = text.lower()
    
    intent = "general_query"
    entities = {}
    
    country_keywords = {
        "germany": "Germany",
        "german": "Germany",
        "berlin": "Germany",
        "munich": "Germany",
        "japan": "Japan",
        "japanese": "Japan",
        "tokyo": "Japan",
        "osaka": "Japan",
        "united states": "United States",
        "usa": "United States",
        "america": "United States",
        "new york": "United States",
        "san francisco": "United States",
        "uk": "United Kingdom",
        "london": "United Kingdom",
        "canada": "Canada",
        "toronto": "Canada",
        "vancouver": "Canada",
        "australia": "Australia",
        "sydney": "Australia",
        "melbourne": "Australia",
        "netherlands": "Netherlands",
        "amsterdam": "Netherlands",
        "singapore": "Singapore",
        "france": "France",
        "paris": "France",
        "spain": "Spain",
        "barcelona": "Spain",
        "madrid": "Spain",
        "dubai": "UAE",
        "uae": "UAE",
        "portugal": "Portugal",
        "lisbon": "Portugal"
    }
    
    for keyword, country in country_keywords.items():
        if keyword in text_lower:
            entities["country"] = country
            break
    
    if any(word in text_lower for word in ["cost", "expensive", "cheap", "afford", "price", "rent"]):
        intent = "cost_inquiry"
    elif any(word in text_lower for word in ["visa", "permit", "requirement", "document"]):
        intent = "visa_inquiry"
    elif any(word in text_lower for word in ["salary", "income", "earn", "pay", "wage"]):
        intent = "salary_inquiry"
    elif any(word in text_lower for word in ["compare", "vs", "versus", "difference", "better"]):
        intent = "comparison"
    elif any(word in text_lower for word in ["budget", "save", "saving", "plan", "simulate"]):
        intent = "budget_planning"
    elif any(word in text_lower for word in ["vtc", "transaction", "control", "spending"]):
        intent = "vtc_inquiry"
    
    import re
    money_pattern = r'[\$\€\£]?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:dollars?|euros?|pounds?)?'
    money_matches = re.findall(money_pattern, text, re.IGNORECASE)
    if money_matches:
        entities["amounts"] = [float(m.replace(",", "")) for m in money_matches]
    
    return {
        "intent": intent,
        "entities": entities,
        "original_text": text,
        "confidence": 0.85 if entities else 0.6
    }


def generate_conversational_response(
    query_result: Dict[str, Any],
    country: Optional[str] = None,
    city: Optional[str] = None
) -> str:
    """
    Generate a conversational response based on parsed query
    
    Args:
        query_result: Parsed query result from parse_financial_query
        country: Current selected country
        city: Current selected city
        
    Returns:
        Conversational response text
    """
    
    intent = query_result.get("intent", "general_query")
    entities = query_result.get("entities", {})
    
    target_country = entities.get("country", country)
    
    from data_module import get_cost_of_living, get_visa_requirements, get_world_bank_data
    
    if intent == "cost_inquiry" and target_country:
        col_data = get_cost_of_living(target_country)
        if col_data:
            currency = col_data.get("currency", "EUR")
            rent = col_data.get("rent_1br_city", 0)
            groceries = col_data.get("groceries_monthly", 0)
            
            return (
                f"Based on my data for {target_country}, here's what you can expect: "
                f"A one-bedroom apartment in the city center costs around {currency} {rent:,} per month. "
                f"Monthly groceries typically run about {currency} {groceries:,}. "
                f"The overall PPP index is {col_data.get('ppp_index', 1.0):.2f}, which affects your purchasing power. "
                f"Would you like me to simulate your budget for this destination?"
            )
    
    elif intent == "visa_inquiry" and target_country:
        visa_data = get_visa_requirements(target_country)
        if visa_data:
            return (
                f"For {target_country}, the main visa options include: {', '.join(visa_data.get('visa_types', [])[:3])}. "
                f"You'll typically need proof of funds around {visa_data.get('blocked_account', 0):,} in your currency. "
                f"Processing usually takes about {visa_data.get('processing_time_weeks', 4)} weeks. "
                f"Health insurance is {'required' if visa_data.get('health_insurance_required') else 'recommended'}. "
                f"Do you want more details about a specific visa type?"
            )
    
    elif intent == "salary_inquiry" and target_country:
        col_data = get_cost_of_living(target_country)
        if col_data:
            currency = col_data.get("currency", "EUR")
            min_salary = col_data.get("min_salary_tech", 0)
            avg_salary = col_data.get("avg_salary_tech", 0)
            
            return (
                f"In {target_country}'s tech sector, salaries range quite a bit. "
                f"Entry-level positions start around {currency} {min_salary:,} monthly, "
                f"while the average tech salary is about {currency} {avg_salary:,} per month. "
                f"With the local cost of living, this should give you a comfortable lifestyle. "
                f"Want me to run a financial simulation with these numbers?"
            )
    
    elif intent == "comparison":
        return (
            "I can help you compare different destinations! "
            "Tell me which countries you're considering, and I'll break down the costs, "
            "visa requirements, and quality of life factors for each. "
            "Just say something like 'Compare Germany and Portugal' to get started."
        )
    
    elif intent == "budget_planning":
        return (
            "Let's plan your budget! To give you accurate projections, I need to know: "
            "your expected monthly income, your current savings, and which country you're targeting. "
            "I'll then run a Monte Carlo simulation to show you the best financial paths forward. "
            "What's your expected salary in your destination?"
        )
    
    elif intent == "vtc_inquiry":
        return (
            "Visa Transaction Controls help you manage your spending while abroad. "
            "I offer three profiles: Conservative for strict budgeting, Standard for balanced control, "
            "and Flexible for established expats. "
            "Each profile sets limits on international transactions, daily spending, and high-risk purchases. "
            "Which profile would you like to explore?"
        )
    
    return (
        "I'm your Financial Guardian, here to help with your international move. "
        "You can ask me about costs of living, visa requirements, salary expectations, "
        "or run a budget simulation. "
        f"{'I noticed you mentioned ' + target_country + '. Would you like details about moving there?' if target_country else 'Which country are you considering?'}"
    )


class VoiceConversationManager:
    """Manages voice-based conversation flow"""
    
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.context: Dict[str, Any] = {}
    
    def process_voice_input(self, audio_bytes: bytes) -> Dict[str, Any]:
        """Process voice input and generate response"""
        
        transcription = transcribe_audio(audio_bytes)
        
        if not transcription.get("success"):
            return {
                "success": False,
                "error": transcription.get("error", "Transcription failed"),
                "response": "I couldn't understand that. Could you please repeat?"
            }
        
        text = transcription.get("text", "")
        
        parsed = parse_financial_query(text)
        
        if parsed.get("entities", {}).get("country"):
            self.context["country"] = parsed["entities"]["country"]
        
        response = generate_conversational_response(
            parsed,
            country=self.context.get("country"),
            city=self.context.get("city")
        )
        
        self.conversation_history.append({
            "role": "user",
            "text": text,
            "timestamp": datetime.now().isoformat()
        })
        
        self.conversation_history.append({
            "role": "guardian",
            "text": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "user_text": text,
            "parsed_intent": parsed,
            "response": response,
            "context": self.context
        }
    
    def process_text_input(self, text: str) -> Dict[str, Any]:
        """Process text input (fallback when voice unavailable)"""
        
        parsed = parse_financial_query(text)
        
        if parsed.get("entities", {}).get("country"):
            self.context["country"] = parsed["entities"]["country"]
        
        response = generate_conversational_response(
            parsed,
            country=self.context.get("country"),
            city=self.context.get("city")
        )
        
        self.conversation_history.append({
            "role": "user",
            "text": text,
            "timestamp": datetime.now().isoformat()
        })
        
        self.conversation_history.append({
            "role": "guardian",
            "text": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "user_text": text,
            "parsed_intent": parsed,
            "response": response,
            "context": self.context
        }
    
    def set_context(self, country: Optional[str] = None, city: Optional[str] = None):
        """Set conversation context"""
        if country:
            self.context["country"] = country
        if city:
            self.context["city"] = city
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.context = {}


_conversation_manager = None

def get_conversation_manager() -> VoiceConversationManager:
    """Get or create singleton conversation manager"""
    global _conversation_manager
    if _conversation_manager is None:
        _conversation_manager = VoiceConversationManager()
    return _conversation_manager


def check_voice_input_available() -> Dict[str, Any]:
    """Check if voice input is available"""
    client = get_openai_client()
    return {
        "whisper_available": client is not None,
        "browser_api_hint": "Use navigator.mediaDevices.getUserMedia for browser recording",
        "supported_formats": ["wav", "mp3", "webm", "m4a"],
        "max_duration_seconds": 120
    }
