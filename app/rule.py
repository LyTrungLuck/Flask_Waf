import re

def check_xss(input_data):
    xss_patterns = [
        r"<script.*?>",  # Thẻ script
        r"javascript:",  # Sử dụng giao thức javascript
        r"on\w+=.*",  # Các thuộc tính sự kiện
    ]

    for pattern in xss_patterns:
        if re.search(pattern, input_data, re.IGNORECASE):
            return True, "có XSS."

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
            'check_input_size': True
        }

    print(data)

    # Kiểm tra SQL Injection
    if rule_flags.get('check_sql_injection', True):
        is_injection, message = check_sql_injection(data.get('input', ''))
        if is_injection:
            print("SQL Injection detected:", message)
            return True, message

    # Kiểm tra XSS
    if rule_flags.get('check_xss', True):
        is_xss, message = check_xss(data.get('input', ''))
        if is_xss:
            print("XSS detected:", message)
            return True, message

    # Kiểm tra Directory Traversal
    if rule_flags.get('check_directory_traversal', True):
        is_traversal, message = check_directory_traversal(data.get('input', ''))
        if is_traversal:
            print("Directory Traversal detected:", message)
            return True, message

    # Kiểm tra kích thước dữ liệu
    if rule_flags.get('check_input_size', True):
        is_large, message = check_input_size(data.get('input', ''))
        if is_large:
            print("Input size issue detected:", message)
            return True, message

    print("pass")
    return False, ""


data = {'input': "SELECT * FROM users WHERE id = 1 OR 1=1"}
rule_flags = {
    'check_sql_injection': True,
    'check_xss': True,
    'check_directory_traversal': True,
    'check_input_size': True
}

print(apply_rules(data, rule_flags))

# Nếu bạn muốn tắt kiểm tra XSS
rule_flags['check_sql_injection'] = False
print(apply_rules(data, rule_flags))

import unittest


# class TestWAFChecks(unittest.TestCase):
#
#     def test_check_sql_injection(self):
#         self.assertTrue(check_sql_injection("SELECT * FROM users WHERE id = 1 OR 1=1")[0])
#         self.assertFalse(check_sql_injection("SELECT name FROM users")[0])
#
#     def test_check_xss(self):
#         self.assertTrue(check_xss("<script>alert('XSS')</script>")[0])
#         self.assertFalse(check_xss("Hello, World!")[0])
#
#     def test_check_directory_traversal(self):
#         self.assertTrue(check_directory_traversal("../../etc/passwd")[0])
#         self.assertFalse(check_directory_traversal("uploads/file.txt")[0])
#
#     def test_check_input_size(self):
#         self.assertTrue(check_input_size("a" * 1025)[0])  # Kích thước vượt quá 1024
#         self.assertFalse(check_input_size("a" * 1024)[0])  # Kích thước không vượt quá 1024
#
#
# if __name__ == '__main__':
#     unittest.main()