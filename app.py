from flask import Flask, request
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
import os
import datetime
from dateutil.relativedelta import relativedelta


from mysql.connector import connect

# Database connection parameters
db_config = {
    'host': 'www.amazon.host.com',
    'user': 'admin',
    'password': 'password',
    'database': 'machine_maintenance'
}

# Function to create a connection to the MySQL database
def create_connection():
    return connect(**db_config)



app = Flask(__name__)

# Configure Flask-Bcrypt
bcrypt = Bcrypt(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


# Function to upload machine details
def upload_machine_to_db(description, photo, frequency, service_by, notes):
    # Creating a connection to the database
    conn = create_connection()
    cursor = conn.cursor()

    # Save photo and get its URL
    photo_filename = secure_filename(photo.filename)
    photo_path = os.path.join('uploads', photo_filename)
    photo.save(photo_path)
    photo_url = f'/uploads/{photo_filename}'

    # Inserting machine details into the database
    query = """
    INSERT INTO Machines (description, photo_url, default_frequency, service_by_date, notes)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (description, photo_url, frequency, service_by, notes))
    conn.commit()

    # Closing the connection
    cursor.close()
    conn.close()

@app.route('/upload_machine', methods=['POST'])
def upload_machine():
    data = request.form
    description = data.get('description')
    photo = request.files['photo']
    frequency = int(data.get('frequency'))
    service_by = data.get('service_by')  # Date in 'YYYY-MM-DD' format
    notes = data.get('notes')

    # Uploading machine details to the database
    upload_machine_to_db(description, photo, frequency, service_by, notes)

    return 'Machine uploaded successfully', 200

@app.route('/set_frequency', methods=['POST'])
def set_frequency():
    machine_id = request.form.get('machine_id')
    frequency = int(request.form.get('frequency'))

    # Creating a connection to the database
    conn = create_connection()
    cursor = conn.cursor()

    # Updating the default servicing frequency for the specified machine
    query = "UPDATE Machines SET default_frequency = %s WHERE machine_id = %s"
    cursor.execute(query, (frequency, machine_id))
    conn.commit()

    # Closing the connection
    cursor.close()
    conn.close()

    return 'Default servicing frequency updated successfully', 200


@app.route('/set_default_frequency', methods=['POST'])
def set_default_frequency():
    machine_id = int(request.form.get('machine_id'))
    frequency = int(request.form.get('frequency'))

    # Update default frequency in the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE machines SET default_frequency = ? WHERE machine_id = ?",
        (frequency, machine_id)
    )
    conn.commit()
    conn.close()

    return "Default frequency updated successfully!"

@app.route('/set_service_by_date', methods=['POST'])
def set_service_by_date():
    machine_id = int(request.form.get('machine_id'))
    service_by = request.form.get('service_by')  # Date in 'YYYY-MM-DD' format

    # Update service by date in the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE machines SET service_by = ? WHERE machine_id = ?",
        (service_by, machine_id)
    )
    conn.commit()
    conn.close()

    return "Service by date updated successfully!"

@app.route('/view_machines', methods=['GET'])
def view_machines():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM machines")
    machines = cursor.fetchall()
    conn.close()

    machine_info = []
    for machine in machines:
        machine_id, description, photo_url, default_frequency, service_by, notes = machine
        next_service_date = datetime.datetime.strptime(service_by, '%Y-%m-%d') - relativedelta(days=default_frequency)
        machine_info.append({
            'machine_id': machine_id,
            'description': description,
            'photo_url': photo_url,
            'default_frequency': default_frequency,
            'service_by': service_by,
            'notes': notes,
            'next_service_date': next_service_date.strftime('%Y-%m-%d')
        })

    return {'machines': machine_info}


from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# Function to send email
def send_email(to, subject, body):
    msg = Message(subject, recipients=[to])
    msg.body = body
    mail.send(msg)

# Function to check upcoming services and send email alerts
def check_upcoming_services():
    conn = create_connection()
    cursor = conn.cursor()

    # Query to get machines with upcoming services (adjust the query as needed)
    query = "SELECT * FROM Machines WHERE service_by_date <= CURDATE() + INTERVAL 7 DAY"
    cursor.execute(query)
    machines = cursor.fetchall()

    for machine in machines:
        # Get contact details (e.g., from the Companies table)
        contact_email = 'contact@example.com'  # Replace with actual query
        subject = f"Upcoming Service for Machine {machine[0]}"
        body = f"Service is due for machine {machine[2]} by {machine[6]}"
        send_email(contact_email, subject, body)

    cursor.close()
    conn.close()

# Schedule the task to run daily
scheduler = BackgroundScheduler()
scheduler.add_job(check_upcoming_services, 'interval', days=1)
scheduler.start()


if __name__ == '__main__':
    app.run(debug=True)
