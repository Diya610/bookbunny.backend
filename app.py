from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import random
import hashlib

app = Flask(__name__)

# ✅ Fix CORS (IMPORTANT for Vercel frontend)
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ Temporary in-memory storage
users = []
books = [
    {"id": 1, "title": "The Alchemist", "author": "Paulo Coelho"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "Pride and Prejudice", "author": "Jane Austen"},
]

@app.route("/")
def home():
    return jsonify({"message": "BookBunny API running!"})

# ✅ SIGNUP API
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    # Email already exists check
    for u in users:
        if u["email"] == email:
            return jsonify({"error": "Email already registered"}), 400

    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    user = {"username": username, "email": email, "password": hashed_pw}
    users.append(user)

    return jsonify({"message": "Signup successful!", "user": username}), 201


# ✅ LOGIN API
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    for u in users:
        if u["email"] == email and u["password"] == hashed_pw:
            return jsonify({"message": "Login successful!", "user": u["username"]})

    return jsonify({"error": "Invalid credentials"}), 401


# ✅ Books List API
@app.route("/books")
def get_books():
    return jsonify(books)


# ✅ Random Recommendation API
@app.route("/recommend")
def recommend():
    return jsonify(random.choice(books))


# ✅ Render Hosting PORT fix
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
