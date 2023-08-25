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




app.config["MAIL_SERVER"] = "smtp.example.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "your_email@example.com"
app.config["MAIL_PASSWORD"] = "your_email_password"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)

from server_functions.routes import *
from server_functions.helpers import *

scheduler = BackgroundScheduler()
scheduler.add_job(check_upcoming_services, "interval", days=1)
scheduler.start()


if __name__ == "__main__":
    app.run(debug=True)
