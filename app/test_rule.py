import unittest

from app.rule import check_rfi, check_command_injection, check_xss, check_directory_traversal, check_sql_injection, check_input_size


# Giả sử rằng các hàm kiểm tra của bạn đã được nhập từ đâu đó, chẳng hạn như:
# from your_module import check_rfi, check_csrf, check_command_injection, check_xss, check_directory_traversal, check_sql_injection, check_input_size

class TestSecurityChecks(unittest.TestCase):

    def test_check_rfi(self):
        self.assertEqual(check_rfi("http://example.com/file.php"), (True, "Có chứa Remote File Inclusion."))
        self.assertEqual(check_rfi("file=data.json"), (True, "Có chứa Remote File Inclusion."))
        self.assertEqual(check_rfi("no rfi here"), (False, ""))

    # def test_check_csrf(self):
    #     self.assertEqual(check_csrf("Some random request without CSRF token"), (True, "Yêu cầu có khả năng bị tấn công CSRF."))
    #     self.assertEqual(check_csrf("Request with X-CSRF-Token"), (False, ""))

    def test_check_command_injection(self):
        self.assertEqual(check_command_injection("ls -la"), (True, "Có khả năng bị tấn công Command Injection."))
        self.assertEqual(check_command_injection("echo Hello World"), (False, ""))

    def test_check_xss(self):
        self.assertEqual(check_xss("<script>alert('XSS')</script>"), (True, "có XSS."))
        self.assertEqual(check_xss("Normal text without script"), (False, ""))

    def test_check_directory_traversal(self):
        self.assertEqual(check_directory_traversal("../etc/passwd"), (True, "Có truy cập thư mục bất hợp pháp"))
        self.assertEqual(check_directory_traversal("safe/path/to/file"), (False, ""))

    def test_check_sql_injection(self):
        self.assertEqual(check_sql_injection("SELECT * FROM users WHERE name='admin' --"), (True, "Có chứa SQL Injection."))
        self.assertEqual(check_sql_injection("No SQL Injection here"), (False, ""))

    def test_check_input_size(self):
        self.assertEqual(check_input_size("A" * 1025), (True, "kích thước vượt quá giới hạn."))
        self.assertEqual(check_input_size("A" * 1024), (False, ""))

if __name__ == '__main__':
    unittest.main()