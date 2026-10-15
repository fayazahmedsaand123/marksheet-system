from flask import Flask, render_template, request, redirect, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from database import get_db
from helpers import  calculate_total, calculate_percentage, calculate_result, calculate_grade
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-key")

app.config["MAIL_SERVER"]   = "smtp.gmail.com"
app.config["MAIL_PORT"]     = 587
app.config["MAIL_USE_TLS"]  = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)
def is_admin():
    return session.get("user_role") == "admin"

try:
    db = get_db()
    print("MYSQL Database Connected Successfully")
    db.close()
except Exception as e:
    print("MYSQL Database Connection Failed: ",e)

@app.route("/")
def home():

    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM marksheets ORDER BY id ASC ")
    marksheets = cursor.fetchall()
    cursor.close()
    db.close()

    total_students = len(marksheets)
    pass_count = sum(1 for m in marksheets if m["result"] == "Pass")
    fail_count = sum(1 for m in marksheets if m["result"] == "Fail")

    return render_template("dashboard.html",
                           marksheets=marksheets,
                           total_students=total_students,
                           pass_count=pass_count,
                           fail_count=fail_count
    )

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    if "user_id" not in session:
        return redirect("/login")
    if not is_admin():
        return redirect("/")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        student_name = request.form["student_name"]
        roll_number = request.form["roll_number"]
        class_name = request.form["class"]
        exam_name = request.form["exam_name"]
        english = int(request.form["english"])
        mathematics = int(request.form["mathematics"])
        computer = int(request.form["computer"])
        physics = int(request.form["physics"])
        chemistry = int(request.form["chemistry"])

        total = calculate_total(english, mathematics, computer, physics, chemistry)
        percentage = calculate_percentage(total)
        result = calculate_result(english, mathematics, computer, physics, chemistry)
        grade = calculate_grade(percentage,result)

        query = """
            UPDATE marksheets SET
                student_name=%s, roll_number=%s, `class`=%s, exam_name=%s,
                english=%s, mathematics=%s, computer=%s, physics=%s, chemistry=%s,
                total=%s, percentage=%s, grade=%s, result=%s WHERE id = %s   
        """
        values = (student_name, roll_number, class_name, exam_name,
                  english, mathematics, computer, physics, chemistry,
                  total, percentage, grade, result, id)
        cursor.execute(query,values)
        db.commit()
        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "message": "Marksheet updated successfully"
        })

    cursor.execute("SELECT * FROM marksheets WHERE id = %s",(id,))
    marksheet = cursor.fetchone()
    cursor.close()
    db.close()

    return render_template("marksheet/edit.html",marksheet=marksheet)

@app.route("/delete/<int:id>",methods=["POST"])
def delete(id):
    if not is_admin():
        return jsonify({"success": False, "message": "Access denied!"})

    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM marksheets WHERE id = %s",(id,))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({
        "success" : True,
        "message" :"Marksheet deleted successfully"
    })


@app.route("/view/<int:id>")
def view_marksheet(id):

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM marksheets WHERE id = %s",(id,))
    marksheet = cursor.fetchone()
    cursor.close()
    db.close()

    return render_template("marksheet/view.html",marksheet=marksheet)


@app.route("/create", methods=["GET", "POST"])
def create():

    if "user_id" not in session:
        return redirect("/login")
    if not is_admin():
        return redirect("/")

    if request.method == "POST":

        student_name = request.form["student_name"]
        roll_number = request.form["roll_number"]
        class_name = request.form["class"]
        exam_name = request.form["exam_name"]
        english = int(request.form["english"])
        mathematics  = int(request.form["mathematics"])
        computer = int(request.form["computer"])
        physics = int(request.form["physics"])
        chemistry = int(request.form["chemistry"])

        total = calculate_total(english,mathematics,computer,physics,chemistry)
        percentage = calculate_percentage(total)
        result = calculate_result(english,mathematics,computer,physics,chemistry)
        grade = calculate_grade(percentage,result)

        db = get_db()
        cursor = db.cursor()
        query = """
            INSERT INTO marksheets
                (student_name, roll_number, `class`, exam_name, english, mathematics,
                computer, physics, chemistry, total, percentage, grade, result)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (student_name,roll_number,class_name,exam_name,english,mathematics,computer,
                  physics,chemistry,total,percentage,grade,result)

        cursor.execute(query,values)
        db.commit()
        cursor.close()
        db.close()

        return redirect("/")
    return render_template("marksheet/create.html")

@app.route("/register")
def register():
    return redirect("/login")


@app.route('/login',methods=["GET","POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s",(email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_role"] = user["role"]
            return redirect("/")
        else:
            error = "Invalid email or password!"
    return render_template("auth/login.html",error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/users")
def users():
    if "user_id" not in session:
        return redirect("/login")
    if not is_admin():
        return redirect("/")

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, role, created_at FROM users ORDER BY id ASC")
    all_users = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("auth/users.html", users=all_users)


@app.route("/users/add", methods=["GET", "POST"])
def add_user():
    if "user_id" not in session:
        return redirect("/login")
    if not is_admin():
        return redirect("/")

    if request.method == "POST":
        name     = request.form["name"]
        email    = request.form["email"]
        password = generate_password_hash(request.form["password"])
        role     = "user"

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            (name, email, password, role)
        )
        db.commit()
        cursor.close()
        db.close()

        return redirect("/users")

    return render_template("auth/add_user.html")


@app.route("/users/delete/<int:id>", methods=["POST"])
def delete_user(id):
    if not is_admin():
        return jsonify({"success": False, "message": "Access denied!"})

    # Prevent admin from deleting themselves
    if id == session["user_id"]:
        return jsonify({"success": False, "message": "Cannot delete yourself!"})

    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"success": True, "message": "User deleted!"})

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    message = None
    error   = None

    if request.method == "POST":
        email = request.form["email"]

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            # Generate secure token
            token = serializer.dumps(email, salt="password-reset")

            # Build reset link
            reset_link = f"http://127.0.0.1:5000/reset-password/{token}"

            # Send email
            msg = Message(
                subject="Password Reset - Marksheet System",
                sender=os.getenv("MAIL_USERNAME"),
                recipients=[email]
            )
            msg.body = f"""
Hello {user['name']},

You requested to reset your password.

Click this link to reset your password:
{reset_link}

This link expires in 30 minutes.

If you did not request this, ignore this email.

Marksheet System
            """
            mail.send(msg)
            message = "Reset link sent to your email!"
        else:
            error = "No account found with this email!"

    return render_template("auth/forgot_password.html",
                           message=message,
                           error=error)


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    error = None

    try:
        # Verify token — expires after 30 minutes
        email = serializer.loads(token, salt="password-reset", max_age=1800)
    except:
        return render_template("auth/reset_password.html",
                               error="Link expired or invalid!",
                               token=None)

    if request.method == "POST":
        new_password = generate_password_hash(request.form["password"])

        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE email = %s",
                       (new_password, email))
        db.commit()
        cursor.close()
        db.close()

        return redirect("/login")

    return render_template("auth/reset_password.html",
                           token=token,
                           error=error)

if __name__ == "__main__":
    print("Marksheet System Starting...")
    app.run(debug=True)