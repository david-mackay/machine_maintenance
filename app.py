from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
import datetime
from dateutil.relativedelta import relativedelta

from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler

from mysql.connector import connect

db_config = {
    "host": "united-plastics-db.ckk0bk8u3zdd.us-east-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Icarlyrocks!2",
    "database": "machine_maintenance",
}

def create_connection():
    return connect(**db_config)


app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)

app.config["MAIL_SERVER"] = "smtp.example.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "your_email@example.com"
app.config["MAIL_PASSWORD"] = "your_email_password"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
mail = Mail(app)


@app.route("/upload_machine", methods=["POST"])
def upload_machine():
    machine_name = request.form["machine_name"]
    description = request.form["description"]
    frequency = request.form["frequency"]
    service_by = request.form["service_by"]
    notes = request.form["notes"]
    user_id = request.form["user_id"]
    #todo: get company_id from user_id, check_permissions

    photo = request.files["photo"]
    if photo and photo.filename != "":
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)
        photo.save(photo_path)
    else:
        photo_path = None

    conn = create_connection()
    cursor = conn.cursor()
    query = (
        "INSERT INTO Machines (description, photo_url, default_frequency, service_by_date, notes) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    cursor.execute(query, (description, photo_path, frequency, service_by, notes))

    conn.commit()
    cursor.close()
    conn.close()

    return "Machine uploaded successfully!"


@app.route("/set_frequency", methods=["POST"])
def set_frequency():
    machine_id = request.form.get("machine_id")
    frequency = int(request.form.get("frequency"))
    conn = create_connection()
    cursor = conn.cursor()

    query = "UPDATE Machines SET default_frequency = %s WHERE machine_id = %s"
    cursor.execute(query, (frequency, machine_id))
    conn.commit()

    cursor.close()
    conn.close()

    return "Default servicing frequency updated successfully", 200


@app.route("/set_default_frequency", methods=["POST"])
def set_default_frequency():
    machine_id = int(request.form.get("machine_id"))
    frequency = int(request.form.get("frequency"))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE machines SET default_frequency = ? WHERE machine_id = ?",
        (frequency, machine_id),
    )
    conn.commit()
    conn.close()

    return "Default frequency updated successfully!"


@app.route("/set_service_by_date", methods=["POST"])
def set_service_by_date():
    machine_id = int(request.form.get("machine_id"))
    service_by = request.form.get("service_by")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE machines SET service_by = ? WHERE machine_id = ?",
        (service_by, machine_id),
    )
    conn.commit()
    conn.close()

    return "Service by date updated successfully!"


@app.route("/view_machines", methods=["GET"])
def view_machines():
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Machines"
    cursor.execute(query)
    machines = cursor.fetchall()

    result = []
    for machine in machines:
        result.append(
            {
                "machine_id": machine[0],
                "description": machine[2],
                "photo_url": machine[3],
                "default_frequency": machine[4],
                "last_service_date": machine[5],
                "service_by_date": machine[6],
                "notes": machine[7],
            }
        )

    cursor.close()
    conn.close()

    return jsonify(result)


app.config["MAIL_SERVER"] = "smtp.example.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "your_email@example.com"
app.config["MAIL_PASSWORD"] = "your_email_password"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)

def send_email(to, subject, body):
    msg = Message(subject, recipients=[to])
    msg.body = body
    mail.send(msg)


def check_upcoming_services():
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Machines WHERE service_by_date <= CURDATE() + INTERVAL 7 DAY"
    cursor.execute(query)
    machines = cursor.fetchall()

    for machine in machines:
        contact_email = "contact@example.com"
        subject = f"Upcoming Service for Machine {machine[0]}"
        body = f"Service is due for machine {machine[2]} by {machine[6]}"
        send_email(contact_email, subject, body)

    cursor.close()
    conn.close()

scheduler = BackgroundScheduler()
scheduler.add_job(check_upcoming_services, "interval", days=1)
scheduler.start()


if __name__ == "__main__":
    app.run(debug=True)
