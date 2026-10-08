import random

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db, bcrypt, BLOCKLIST
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
import random
from datetime import datetime, timedelta
from flask_mail import Message
from app.extensions import mail
from flask import current_app


def is_valid_text(value, max_len):
    return isinstance(value, str) and 0 < len(value.strip()) <= max_len

auth_bp = Blueprint("auth", __name__)

def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(user_email, otp_code):

    msg = Message(
        subject="Your OTP Verification Code",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[user_email],
        body=f"Your Verification code is: {otp_code}. It will expire in 5 minutes."
    )
    mail.send(msg)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email, and password are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long"}), 400

    if not (is_valid_text(name, 100) and is_valid_text(email, 255) and is_valid_text(password, 72)):
        return jsonify({"error": "Invalid input"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    otp = generate_otp()

    new_user = User(
        name=name, 
        email=email, 
        password_hash=hashed_password, 
        otp_code=otp, 
        otp_code_expiration=datetime.utcnow() + timedelta(minutes=5),
        )

    db.session.add(new_user)
    db.session.commit()

    send_otp_email(email, otp)

    return jsonify({"message": "Registered. Check your email for a verification code."}), 201


@auth_bp.route("/resend-otp", methods=["POST"])
def resend_otp():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.is_verified:
        return jsonify({"message": "Account already verified"}), 200

    new_otp = generate_otp()

    user.otp_code = new_otp
    user.otp_code_expiration = datetime.utcnow() + timedelta(minutes=5)

    db.session.commit()

    send_otp_email(email, new_otp)

    return jsonify({"message": "A new verification code has been sent"}), 200



@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    email = data.get("email")
    otp = data.get("otp")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.is_verified:
        return jsonify({"message": "Account already verified"}), 200

    if otp != user.otp_code:
        return jsonify({"error": "Incorrect verification code"}), 400

    if datetime.utcnow() > user.otp_code_expiration:
        return jsonify({"error": "Verification code expired"}), 400

    user.is_verified = True
    user.otp_code = None
    user.otp_code_expiration = None

    db.session.commit()

    return jsonify({"message": "Account verified successfully"}), 200




@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    if not (is_valid_text(email, 255) and is_valid_text(password, 72)):
        return jsonify({"error": "Invalid email or password"}), 400

    if not user.is_verified:
        return jsonify({"error": "Please verify your email before logging in"}), 403

    access_token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": access_token}), 200



@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200