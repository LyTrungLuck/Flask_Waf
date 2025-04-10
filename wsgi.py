from functools import wraps

from flask import request, jsonify, render_template, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user

from app import app, dao, login
from app.dao import get_webs_by_user, create_web
from app.rule import apply_rules


@app.route("/")
def home():
    return render_template("index.html")  # Trả về tệp index.html


@app.route("/waf", methods=["GET", "POST"])
def waf():
    user_id = current_user.id  # Giả sử bạn có một user_id, có thể lấy từ session hoặc thông tin người dùng

    if request.method == "POST":
        # Nhận dữ liệu từ biểu mẫu
        app_name = request.form["app_name"]
        app_url = request.form["app_url"]

        # Tạo một đối tượng Web mới
        create_web(app_name, app_url, user_id)
        flash("Ứng dụng web đã được thêm thành công!")

        return redirect(url_for('waf'))  # Chuyển hướng về trang waf để làm mới nội dung

    # Lấy danh sách ứng dụng web của người dùng
    webs = get_webs_by_user(user_id)

    return render_template("waf.html", webs=webs)


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



# Hàm trang bị kiểm tra nguồn gốc
def allow_specific_origin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Lấy tiêu đề Origin (hoặc Referer) từ yêu cầu
        origin = request.headers.get('Origin') or request.headers.get('Referer')
        print(f'Origin or Referer: {origin}')  # In ra để kiểm tra
        print(f'request.headers: {request.headers}')  # In ra để kiểm tra
        print(f'END')  # In ra để kiểm tra

        # Kiểm tra nếu Origin là product.com
        if not origin or 'http://127.0.0.1:5002' not in origin:
            return jsonify({"message": "Request BỊ CHẶN!!!", "reason": "Request bị từ chối, chỉ cho phép từ https://product.com"}), 403

        return f(*args, **kwargs)

    return decorated_function


@app.route('/api/request', methods=['POST'])
@allow_specific_origin
def handle_request():
    print('handle_request')
    data = request.json
    print(f'data={data}')

    # Lấy rule_flags từ dữ liệu gửi đến
    rule_flags = data.get('rule_flags', None)

    # Áp dụng các quy tắc WAF
    is_blocked, reason = apply_rules(data, rule_flags)

    if is_blocked:
        return jsonify({"message": "Request BỊ CHẶN!!!", "reason": reason}), 403

    # Tiếp tục xử lý yêu cầu nếu không bị chặn
    return jsonify({"message": "Request hợp lệ", "data": data}), 200


if __name__ == "__main__":
    # app.run( host="0.0.0.0", port=5000, debug=True)
    with app.app_context():
        app.run( host="0.0.0.0", port=5000, debug=True)