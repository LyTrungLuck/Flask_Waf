from flask import request, jsonify, render_template

from app import app
from app.rule import apply_rules


@app.route("/")
def home():
    return render_template("test.html")  # Trả về tệp index.html


@app.route('/api/request', methods=['POST'])
def handle_request():
    data = request.json

    # Áp dụng các quy tắc WAF
    is_blocked, reason = apply_rules(data)

    if is_blocked:
        return jsonify({"message": "Request blocked", "reason": reason}), 403

    # Tiếp tục xử lý yêu cầu nếu không bị chặn
    return jsonify({"message": "Request processed", "data": data}), 200
