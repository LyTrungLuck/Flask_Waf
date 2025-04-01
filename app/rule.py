import re

def check_rfi(input_data):
    rfi_patterns = [
        r"http[s]?://",  # Kiểm tra URL dẫn đến tệp
        r"file=.+\.(php|txt|json|xml|html|css|js)$"  # Kiểm tra tệp với phần mở rộng cụ thể
    ]

    for pattern in rfi_patterns:
        if re.search(pattern, input_data, re.IGNORECASE):
            return True, "Có chứa Remote File Inclusion."

    return False, ""


# def check_csrf(input_data):
#     # Một phương pháp đơn giản để phát hiện CSRF có thể là kiểm tra sự tồn tại của các cookie hoặc header CSRF
#     if "X-CSRF-Token" not in input_data:
#         return True, "Yêu cầu có khả năng bị tấn công CSRF."
#
#     return False, ""


def check_command_injection(input_data):
    command_injection_patterns = [
        r"\;|&&|\|\|",  # Những ký tự có thể được sử dụng để chèn lệnh
        r"(\bcat\b|\bls\b|\bcp\b|\bmv\b|\bmkdir\b|\bchmod\b|\bexec\b|\bcommand\b)",  # Tìm các lệnh hệ thống
    ]

    for pattern in command_injection_patterns:
        if re.search(pattern, input_data, re.IGNORECASE):
            return True, "Có khả năng bị tấn công Command Injection."

    return False, ""


def check_xss(input_data):
    xss_patterns = [
        r"<script.*?>",  # Thẻ script
        r"javascript:",  # Sử dụng giao thức javascript
        r"on\w+=.*",  # Các thuộc tính sự kiện
    ]

    for pattern in xss_patterns:
        if re.search(pattern, input_data, re.IGNORECASE):
            return True, "có chứa XSS."

    return False, ""


def check_directory_traversal(input_data):
    if '../' in input_data or '..\\' in input_data:
        return True, "Có truy cập thư mục bất hợp pháp"

    return False, ""


# def check_http_request(request):
#     valid_methods = ["GET", "POST", "PUT", "DELETE"]
#     if request.method not in valid_methods:
#         return True, "Invalid HTTP method detected."
#
#     # Kiểm tra tiêu đề cơ bản
#     if 'User-Agent' not in request.headers:
#         return True, "Missing User-Agent header."
#
#     return False, ""


def check_sql_injection(input_data):
    # Định nghĩa mẫu để phát hiện SQL Injection
    sql_injection_patterns = [
        r"'.*--",  # SQL comment
        r"'.*#",
        r"'.*;.*",  # Statements termination
        r"OR\s+1=1",  # Always true
        r"UNION.*SELECT",  # Union-based
        r"DROP\s+TABLE",  # Drop table
        r"EXEC\s+",  # Execute commands
        r"INSERT\s+INTO",  # Insert into statement
        r"UPDATE.*SET",  # Update statement
        r"DELETE\s+FROM"  # Delete statement
    ]

    # Kiểm tra SQL Injection
    for pattern in sql_injection_patterns:
        if re.search(pattern, input_data, re.IGNORECASE):
            return True, "Có chứa SQL Injection."

    return False, ""


def check_input_size(input_data, max_size=1024):
    if len(input_data) > max_size:
        return True, "kích thước vượt quá giới hạn."

    return False, ""


def apply_rules(data, rule_flags=None):
    if rule_flags is None:
        rule_flags = {
            'check_sql_injection': True,
            'check_xss': True,
            'check_directory_traversal': True,
            'check_input_size': True,
            'check_rfi': True,
            # 'check_csrf': True,
            'check_command_injection': True
        }

    # Kiểm tra SQL Injection
    if rule_flags.get('check_sql_injection', True):
        is_injection, message = check_sql_injection(data.get('input', ''))
        if is_injection:
            return True, message

    # Kiểm tra XSS
    if rule_flags.get('check_xss', True):
        is_xss, message = check_xss(data.get('input', ''))
        if is_xss:
            return True, message

    # Kiểm tra Directory Traversal
    if rule_flags.get('check_directory_traversal', True):
        is_traversal, message = check_directory_traversal(data.get('input', ''))
        if is_traversal:
            return True, message

    # Kiểm tra Remote File Inclusion
    if rule_flags.get('check_rfi', True):
        is_rfi, message = check_rfi(data.get('input', ''))
        if is_rfi:
            return True, message

    # Kiểm tra CSRF
    # if rule_flags.get('check_csrf', True):
    #     is_csrf, message = check_csrf(data.get('input', ''))
    #     if is_csrf:
    #         return True, message

    # Kiểm tra Command Injection
    if rule_flags.get('check_command_injection', True):
        is_command_injection, message = check_command_injection(data.get('input', ''))
        if is_command_injection:
            return True, message

    # Kiểm tra kích thước dữ liệu
    if rule_flags.get('check_input_size', True):
        is_large, message = check_input_size(data.get('input', ''))
        if is_large:
            return True, message

    return False, ""