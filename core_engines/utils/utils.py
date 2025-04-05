from datetime import datetime

def get_formatted_datetime():
    """Get current datetime formatted as MM/DD/YYYY HH:MM"""
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M")