import re

def normalize_phone(phone: str) -> str:
    if not phone:
        return ""
    digits = re.sub(r"[^\d]", "", phone)
    if len(digits) == 11 and digits.startswith("0"):
        return f"+98{digits[1:]}"
    elif len(digits) == 10:
        return f"+98{digits}"
    elif len(digits) == 12 and digits.startswith("98"):
        return f"+{digits}"
    return phone
