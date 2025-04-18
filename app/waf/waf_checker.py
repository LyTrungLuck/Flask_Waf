import re

def is_request_safe(data):
    payload = f"{data.get('query', '')} {data.get('body', '')}"

    # Rule 1: Chặn SQLi đơn giản
    if re.search(r"(union|select|drop|--|\bor\b|\band\b)", payload, re.IGNORECASE):
        return False, "SQL Injection pattern detected"

    # Rule 2: Chặn XSS đơn giản
    if re.search(r"<script.*?>", payload, re.IGNORECASE):
        return False, "XSS pattern detected"

    return True, "OK"
