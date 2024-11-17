# medicalassitant-whatsapp-ai
Whatsapp Medical Assitant that books an Appointment for doctors and answer all queries regarding doctors work

# Medical Appointment Bot 🏥

A WhatsApp-based conversational AI assistant that helps manage appointments at Dr. Smith's Clinic. Built with Python, FastAPI, and Google's Gemini AI, this bot provides a seamless and natural booking experience for patients.

## Features ✨

- **Natural Conversation**: Engages in human-like dialogue using Gemini AI
- **Smart Appointment Management**: 
  - Collects patient information naturally
  - Handles scheduling, rescheduling, and cancellations
  - Validates clinic hours and appointment availability
  - Provides clear appointment confirmations
- **Context-Aware**: Remembers previous interactions and maintains conversation flow
- **Emergency Detection**: Identifies urgent medical situations and provides appropriate guidance
- **WhatsApp Integration**: Seamless communication through WhatsApp Business API
- **Voice Message Support**: Can process transcribed voice messages (future feature)

## Tech Stack 🛠

- **Backend**: Python 3.12, FastAPI
- **AI/ML**: Google Gemini Pro API
- **Database**: SQLite
- **Messaging**: WhatsApp Business API
- **Deployment**: Docker-ready

## Project Structure 📁

```
medical-bot/
├── main.py           # FastAPI + WebHook handling + Core logic
├── prompts.py        # Gemini AI prompts
├── database.py       # SQLite database operations
├── config.py         # Configuration and constants
├── requirements.txt  # Python dependencies
├── Dockerfile        # Container configuration
└── .env             # Environment variables (not tracked)
```

## Setup and Installation 🚀

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/medical-appointment-bot.git
   cd medical-appointment-bot
   ```

2. **Set up environment variables**
   Create a `.env` file with:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   WHATSAPP_PHONE_ID=your_whatsapp_phone_id
   WHATSAPP_TOKEN=your_whatsapp_token
   VERIFY_TOKEN=your_verify_token
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

### Docker Deployment 🐳

```bash
docker build -t medical-bot .
docker run -p 8080:8080 medical-bot
```

## Core Functionalities 🎯

### Appointment Booking Flow
1. Bot introduces itself as Lisa from Dr. Smith's Clinic
2. Collects patient information conversationally:
   - Name
   - Age
   - Medical concern/symptoms
   - Contact number
   - Preferred appointment time
3. Validates appointment details
4. Sends confirmation with unique reference code

### Special Commands
- `reset` - Start fresh conversation
- `cancel` - Cancel current appointment
- `reschedule` - Change appointment time
- `status` - Check appointment details

## Database Schema 💾

### Appointments Table
- `confirmation_code` (Primary Key)
- `patient_name`
- `age`
- `medical_concern`
- `appointment_date`
- `appointment_time`
- `phone_number`
- `relation`
- `status`
- `created_at`

### Conversations Table
- `phone_number` (Primary Key)
- `collected_info`
- `history`
- `last_updated`

## Acknowledgments 🙏

- Google Gemini AI for natural language processing
- WhatsApp Business API for messaging capabilities
- FastAPI for the efficient backend framework
