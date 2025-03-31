from flask_cors import CORS

from app import app
CORS(app)  # Bật CORS cho ứng dụng

if __name__ == "__main__":
    app.run( host="0.0.0.0", port=5000, debug=True)

