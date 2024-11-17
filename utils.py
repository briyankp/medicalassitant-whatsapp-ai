from typing import Dict, Any
from datetime import datetime, timedelta

def validate_appointment_time(time_str: str) -> bool:
    """Validate if given time is within clinic hours"""
    try:
        time = datetime.strptime(time_str, "%I:%M %p").time()
        start = datetime.strptime("9:00 AM", "%I:%M %p").time()
        end = datetime.strptime("5:00 PM", "%I:%M %p").time()
        return start <= time <= end
    except:
        return False

def format_time(time_str: str) -> str:
    """Format time string consistently"""
    try:
        time = datetime.strptime(time_str, "%I:%M %p")
        return time.strftime("%I:%M %p")
    except:
        return time_str

def clean_phone_number(phone: str) -> str:
    """Clean and format phone number"""
    return ''.join(filter(str.isdigit, phone))

def is_complete_info(info: Dict[str, Any]) -> bool:
    """Check if all required information is collected"""
    required = ['name', 'age', 'phone', 'concern', 'time']
    return all(info.get(field) for field in required)