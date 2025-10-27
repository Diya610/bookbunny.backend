from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

CORS(app, resources={r"/*": {
    "origins": "*",
    "allow_headers": "*",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
}})


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookbunny.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ✅ User model MUST come BEFORE db.create_all()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# ✅ NOW we can create DB
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "BookBunny API running with database ✅"})

# ✅ Signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400
    
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400
    
    hashed_pw = generate_password_hash(data["password"])
    user = User(username=data["username"], email=data["email"], password_hash=hashed_pw)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "Signup successful"}), 201

# ✅ Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    
    if user and check_password_hash(user.password_hash, data["password"]):
        return jsonify({"message": "Login successful", "user": user.username})
    
    return jsonify({"error": "Invalid credentials"}), 401


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

