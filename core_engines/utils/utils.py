from datetime import datetime

def get_formatted_datetime():
    """Get current datetime formatted as MM/DD/YYYY HH:MM"""
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M")

def _dict_to_string(input_dict):
    """Convert a dictionary to a formatted string"""
    if not isinstance(input_dict, dict):
        return str(input_dict)
    
    result = "{"
    for key, value in input_dict.items():
        if isinstance(value, str):
            result += f"'{key}': '{value}', "
        else:
            result += f"'{key}': {value}, "
    if result.endswith(", "):
        result = result[:-2]
    result += "}"
    return result