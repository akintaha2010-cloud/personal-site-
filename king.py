import sqlite3

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database import add_user, get_user_by_email


auth = Blueprint(
    "auth",
    __name__
)

#Function for user registration
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not full_name or not email or not password:
            return "Please fill in all fields.", 400

        # Aynı e-posta daha önce kaydedilmiş mi?
        existing_user = get_user_by_email(email)

        if existing_user is not None:
            return "An account with this email already exists.", 400

        hashed_password = generate_password_hash(password)

        try:
            add_user(
                full_name,
                email,
                hashed_password
            )
        except sqlite3.IntegrityError:
            return "An account with this email already exists.", 400

        return redirect(url_for("auth.login"))

    return render_template("register.html")

#Function for login
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            return "Email and password are required.", 400

        user = get_user_by_email(email)

        if user is None:
            return "Account not found.", 401

        # user[3] veritabanındaki hashlenmiş şifre
        hashed_password = user[3]

        if not check_password_hash(hashed_password, password):
            return "Incorrect password.", 401

        session["user_id"] = user[0]
        session["full_name"] = user[1]
        session["email"] = user[2]

        return redirect(url_for("index"))

    return render_template("login.html")

#Function for logout
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))