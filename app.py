from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import random

app = Flask(__name__)
CORS(app)  # allow requests from frontend

# In-memory demo storage (replace with DB for production)
users = []
books = [
    {"id": 1, "title": "The Alchemist", "author": "Paulo Coelho", "genre": "Fiction"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic"},
    {"id": 3, "title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance"},
]

@app.route("/")
def home():
    return jsonify({"message": "BookBunny API running!"})

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")  # demo only: DO NOT store plain passwords in production
    if not username or not email or not password:
        return jsonify({"error": "username, email and password required"}), 400
    user = {"id": len(users) + 1, "username": username, "email": email}
    users.append(user)
    return jsonify({"message": "User registered", "user": user}), 201

@app.route("/recommend", methods=["GET"])
def recommend():
    return jsonify(random.choice(books))

if __name__ == "__main__":
    # Use PORT env var for Render compatibility
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
