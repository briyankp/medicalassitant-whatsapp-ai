import google.generativeai as genai
from typing import Dict, Any
import json
from config import CLINIC_INFO, get_appointment_confirmation, get_doctor_summary

def analyze_message(message: str, conversation_history: list, collected_info: dict) -> dict:
    """Use Gemini to analyze message and decide response"""
    
    prompt = f"""You are Lisa, {CLINIC_INFO['doctor']}'s clinic assistant. Respond naturally to this conversation.

Clinic hours: {CLINIC_INFO['timing']}, {CLINIC_INFO['working_days']}
Current conversation history:
{json.dumps(conversation_history[-5:], indent=2)}

Information collected so far:
{json.dumps(collected_info, indent=2)}

Current message: "{message}"

IMPORTANT GUIDELINES:
1. Be professional but friendly
2. Keep responses concise and clear
3. Remember previous information
4. Stay focused on appointment booking
5. For fees/charges, use our standard fee: ${CLINIC_INFO['visiting_fee']} valid for {CLINIC_INFO['fee_validity']}
6. Don't create false medical records
7. For medical questions, guide to the appointment
8. Be honest about what you don't know

Required appointment info:
- Full name
- Age
- Phone number
- Medical concern
- Preferred time ({CLINIC_INFO['timing']})

Return JSON:
{{
    "response": "your natural response",
    "collected_info": {{ any new info }},
    "appointment_status": "none|pending|confirmed",
    "needs_summary": true/false
}}"""

    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        print(f"Error in message analysis: {e}")
        return {
            "response": "I'm having trouble understanding. Could you please rephrase that?",
            "collected_info": {},
            "appointment_status": "none",
            "needs_summary": False
        }

def process_voice_message(audio_data: bytes) -> str:
    """Placeholder for future voice processing"""
    # TODO: Implement voice-to-text conversion
    return "Voice processing will be implemented soon!"