from flask import request, jsonify, render_template

from app import app
from app.rule import apply_rules


@app.route("/")
def home():
    return render_template("test.html")  # Trả về tệp index.html


@app.route('/api/request', methods=['POST'])
def handle_request():
    data = request.json

    # Lấy rule_flags từ dữ liệu gửi đến
    rule_flags = data.get('rule_flags', {})

    # Áp dụng các quy tắc WAF
    is_blocked, reason = apply_rules(data, rule_flags)

    if is_blocked:
        return jsonify({"message": "Request BỊ CHẶN!!!", "reason": reason}), 403

    # Tiếp tục xử lý yêu cầu nếu không bị chặn
    return jsonify({"message": "Request hợp lệ", "data": data}), 200
