from fastapi import FastAPI, Request, Response
import google.generativeai as genai
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure APIs
WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

print("=== STARTUP CONFIG ===")
print(f"Phone ID: {WHATSAPP_PHONE_ID}")
print(f"Token exists: {'Yes' if WHATSAPP_TOKEN else 'No'}")
print(f"Token length: {len(WHATSAPP_TOKEN) if WHATSAPP_TOKEN else 'No token'}")
print("===================")

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# In-memory storage
sessions = {}

def send_whatsapp_message(to: str, message: str):
    print("\n=== SENDING MESSAGE ===")
    print(f"To: {to}")
    print(f"Message: {message}")
    
    url = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_ID}/messages"
    print(f"URL: {url}")
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    print("Headers set (token hidden)")
    
    try:
        print("\nSending request...")
        response = requests.post(url, json=payload, headers=headers)
        print(f"Response Status: {response.status_code}")
        print(f"Response Text: {response.text}")
        return response.json()
    except Exception as e:
        print(f"ERROR sending message: {str(e)}")
        return None

@app.get("/")
async def root():
    return {"status": "healthy"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    print("\n=== WEBHOOK VERIFICATION ===")
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    print(f"Mode: {mode}")
    print(f"Token received: {token}")
    print(f"Expected token: {VERIFY_TOKEN}")
    print(f"Challenge: {challenge}")
    
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("Verification successful!")
            return Response(content=challenge, media_type="text/plain")
    print("Verification failed!")
    return Response(content="Invalid token", media_type="text/plain")

@app.post("/webhook")
async def webhook(request: Request):
    print("\n=== WEBHOOK MESSAGE RECEIVED ===")
    try:
        body = await request.json()
        print(f"Full webhook body: {json.dumps(body, indent=2)}")
        
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        message = value.get("messages", [{}])[0]
        
        if not message:
            print("No message found in webhook")
            return {"status": "no message"}

        user_number = message.get("from")
        msg_text = message.get("text", {}).get("body", "")

        print(f"From: {user_number}")
        print(f"Message: {msg_text}")

        if not user_number or not msg_text:
            print("Invalid message format")
            return {"status": "invalid message"}

        print("\nProcessing message...")
        response = process_message(user_number, msg_text)
        print(f"Bot response: {response}")
        
        print("\nSending response back...")
        send_whatsapp_message(user_number, response)
        
        return {"status": "processed"}
    except Exception as e:
        print(f"ERROR in webhook: {str(e)}")
        return {"status": "error", "message": str(e)}

def process_message(user_id: str, message: str) -> str:
    print(f"\n=== PROCESSING MESSAGE ===")
    print(f"User ID: {user_id}")
    print(f"Message: {message}")
    
    if user_id not in sessions:
        print("New session created")
        sessions[user_id] = {
            "state": "start",
            "info": {},
            "history": []
        }
    
    session = sessions[user_id]
    session["history"].append({"role": "user", "message": message})
    print(f"Current state: {session['state']}")
    
    # First message or greeting
    if session["state"] == "start":
        if any(greeting in message.lower() for greeting in ["hi", "hello", "hey"]):
            session["state"] = "greeting"
            return "Hello! I'm Lisa from Dr. Smith's Family Clinic. Would you like to schedule an appointment?"
            
    # After greeting
    elif session["state"] == "greeting":
        if any(yes in message.lower() for yes in ["yes", "yeah", "sure", "okay"]):
            session["state"] = "asking_name"
            return "Great! Could you tell me your name?"
        else:
            session["state"] = "asking_name"
            session["info"]["purpose"] = message
            return "I understand. Could you tell me your name so I can help you better?"
    
    # Collecting name
    elif session["state"] == "asking_name":
        session["info"]["name"] = message
        session["state"] = "asking_concern"
        return f"Thank you {message}. What brings you to see Dr. Smith today?"
    
    # Collecting health concern
    elif session["state"] == "asking_concern":
        session["info"]["concern"] = message
        session["state"] = "asking_phone"
        return "I'll make a note of that. Could you share your phone number for our records?"
    
    # Collecting phone
    elif session["state"] == "asking_phone":
        session["info"]["phone"] = message
        session["state"] = "asking_time"
        return "Dr. Smith is available tomorrow between 9 AM and 5 PM. What time works best for you?"
    
    # Collecting appointment time
    elif session["state"] == "asking_time":
        session["info"]["time"] = message
        session["state"] = "confirming"
        
        summary = f"""Perfect! I've scheduled your appointment with Dr. Smith for {message} tomorrow.

Location: 123 Medical Plaza, Suite 101 
(Near Central Hospital)

Please arrive 10 minutes early.
Reply 'ok' to confirm."""
        return summary
    
    # Final confirmation
    elif session["state"] == "confirming":
        session["state"] = "completed"
        return "Thank you for choosing Dr. Smith's Clinic. We look forward to seeing you tomorrow! Take care 🙏"
    
    # Default response for completed state
    elif session["state"] == "completed":
        return "Your appointment is confirmed for tomorrow. Is there anything else you need help with?"
    
    # Default fallback
    return "I'm here to help you schedule an appointment. Would you like to proceed?"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))