from os import abort

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.before_request
def block_direct_access():
    print(request.remote_addr)
    if request.remote_addr != "127.0.0.1":
        abort(403)

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(["Book A", "Book B", "Book C"])

@app.route("/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    return jsonify({"message": "Added to cart", "data": data})

if __name__ == "__main__":
    app.run(host="127.0.0.2", port=8000)
