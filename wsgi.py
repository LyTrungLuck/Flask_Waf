from functools import wraps

from flask import request, jsonify, render_template, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user

from app import app, dao, login
from app.dao import get_webs_by_user, create_web
from app.rule import apply_rules
from app.waf.proxy import forward_request
from app.waf.waf_checker import is_request_safe


@app.route("/")
def home():
    return render_template("index.html")  # Trả về tệp index.html


@app.route("/waf_registration", methods=["GET", "POST"])
def waf_registration():
    user_id = current_user.id  # Giả sử bạn có một user_id, có thể lấy từ session hoặc thông tin người dùng

    if request.method == "POST":
        # Nhận dữ liệu từ biểu mẫu
        app_name = request.form["app_name"]
        app_url = request.form["app_url"]

        # Tạo một đối tượng Web mới
        create_web(app_name, app_url, user_id)
        flash("Ứng dụng web đã được thêm thành công!")

        return redirect(url_for('waf_registration'))  # Chuyển hướng về trang waf để làm mới nội dung

    # Lấy danh sách ứng dụng web của người dùng
    webs = get_webs_by_user(user_id)

    return render_template("waf.html", webs=webs)


@app.route("/waf/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def waf(path):
    headers = dict(request.headers)
    body = request.get_data(as_text=True)
    query = request.query_string.decode()

    # Kiểm tra WAF rule
    is_safe, reason = is_request_safe({"query": query, "body": body})
    if not is_safe:
        return jsonify({"error": "Blocked by WAF", "reason": reason}), 403

    # Forward tới hệ thống backend (theo web_url hoặc web_id trong query/session)
    content, status_code, response_headers = forward_request(
        path, request.method, headers, body, query
    )
    return content, status_code, response_headers


@app.route('/login/', methods=['get', 'post'])
# @annonymous_user
def login_my_user():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username, password)
        if user:
            login_user(user=user)
            n = request.args.get('next')
            return redirect(n if n else '/')
        else:
            if not dao.user_exists(request.form['username']):
                err_msg = 'Tài khoản KHÔNG tồn tại'
            else:
                err_msg = 'SAI mật khẩu'
    return render_template("login.html", err_msg=err_msg)


@app.route('/logout/')
def logout_my_user():
    logout_user()
    return redirect('/login')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


@app.route('/register/', methods=['get', 'post'])
# @annonymous_user
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        # save user
        try:
            if dao.user_exists(request.form['username']):
                err_msg = 'Tài khoản đã tồn tại'
            else:
                dao.create_user(name=request.form['name'],
                                username=request.form['username'],
                                password=request.form.get('password'))
                return redirect('/login')
        except:
            err_msg = 'Hệ thống có lỗi'
    return render_template("register.html", err_msg=err_msg)


if __name__ == "__main__":
    # app.run( host="0.0.0.0", port=5000, debug=True)
    with app.app_context():
        app.run( host="0.0.0.0", port=5000, debug=True)