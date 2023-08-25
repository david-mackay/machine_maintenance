from app import create_connection

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