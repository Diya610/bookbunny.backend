from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

CORS(app, origins=[
    "https://bookbunny-frontend.vercel.app",
    "https://bookbunny-frontend-diya610.vercel.app"
], supports_credentials=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookbunny.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ✅ Create DB tables when app starts
with app.app_context():
    db.create_all()

# ✅ USER MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

@app.route("/")
def home():
    return jsonify({"message": "BookBunny API running with database ✅"})

# ✅ SIGNUP
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists 😭"}), 400

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_pw)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Signup successful 🎉"}), 201

# ✅ LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        return jsonify({"message": "Login successful 🎉", "user": user.username})

    return jsonify({"error": "Invalid credentials 😭"}), 401

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
