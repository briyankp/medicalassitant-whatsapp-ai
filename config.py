from datetime import datetime, timedelta

# Clinic Information
CLINIC_INFO = {
    "name": "Dr. Smith's Family Clinic",
    "doctor": "Dr. Smith",
    "address": "123 Medical Plaza, Suite 101",
    "landmark": "Near Central Hospital",
    "visiting_fee": 500,
    "fee_validity": "7 days",
    "timing": "9 AM to 5 PM",
    "working_days": "Monday to Friday",
    "insurance": "Accepts most major insurance plans"
}

# Message Templates
def get_appointment_confirmation(name: str, time: str) -> str:
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A, %B %d")
    return f"""Your appointment is confirmed:

📅 Date: {tomorrow}
⏰ Time: {time}
👨‍⚕️ Doctor: {CLINIC_INFO['doctor']}
📍 Location: {CLINIC_INFO['address']}
          ({CLINIC_INFO['landmark']})
💰 Visiting Fee: ${CLINIC_INFO['visiting_fee']} (valid for {CLINIC_INFO['fee_validity']})

Please arrive 10 minutes early.
Bring any previous medical records if available.

See you tomorrow! Take care 🙏"""

def get_doctor_summary(patient_info: dict) -> str:
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A, %B %d")
    return f"""PATIENT DETAILS:
- Name: {patient_info.get('name')}
- Age: {patient_info.get('age', 'Not provided')}
- Contact: {patient_info.get('phone')}

PRESENTING COMPLAINT:
{patient_info.get('concern', 'Not specified')}

APPOINTMENT:
- Date: {tomorrow}
- Time: {patient_info.get('time')}

ADDITIONAL NOTES:
{patient_info.get('notes', 'No additional notes')}"""