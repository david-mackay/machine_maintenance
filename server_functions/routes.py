from app import app, create_connection
from flask import request, jsonify
from flask_mail import Message
import os
@app.route("/upload_machine", methods=["POST"])
def upload_machine():
    machine_name = request.form["machine_name"]
    description = request.form["description"]

    photo = request.files["photo"]
    if photo and photo.filename != "":
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)
        photo.save(photo_path)
    else:
        photo_path = None

    conn = create_connection()
    cursor = conn.cursor()
    query = (
        "INSERT INTO Machines (machine_name, description, photo_url)"
        "VALUES (%s, %s, %s)"
    )
    cursor.execute(query, (machine_name, description, photo_path))

    conn.commit()
    cursor.close()
    conn.close()

    return "Machine uploaded successfully!"


@app.route("/view_machines", methods=["GET"])
def view_machines():
    conn = create_connection()
    cursor = conn.cursor()

    query = """
        SELECT m.machine_id, m.machine_name, m.description, m.photo_url, 
               ms.status, 
               sl.service_date AS last_service_date, sl.next_service_date
        FROM Machines AS m
        LEFT JOIN (
            SELECT machine_id, status
            FROM machine_status
            WHERE (machine_id, updated_at) IN (
                SELECT machine_id, MAX(updated_at)
                FROM machine_status
                GROUP BY machine_id
            )
        ) AS ms ON m.machine_id = ms.machine_id
        LEFT JOIN (
            SELECT machine_id, MAX(service_date) AS service_date, next_service_date
            FROM service_logs
            GROUP BY machine_id
        ) AS sl ON m.machine_id = sl.machine_id
    """
    cursor.execute(query)
    machines = cursor.fetchall()

    result = []
    for machine in machines:
        result.append(
            {
                "machine_id": machine[0],
                "machine_name": machine[1],
                "description": machine[2],
                "photo_url": machine[3],
                "status": machine[4],
                "last_service_date": machine[5],
                "next_service_date": machine[6]
            }
        )

    cursor.close()
    conn.close()

    return jsonify(result)


@app.route("/get_machine_list", methods=["GET"])
def get_machine_list():
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT machine_id, machine_name FROM Machines"
    cursor.execute(query)
    machines = cursor.fetchall()

    result = [{"machine_id": machine[0], "machine_name": machine[1]} for machine in machines]

    cursor.close()
    conn.close()

    return jsonify(result)

@app.route("/service_machine", methods=["POST"])
def service_machine():
    machine_id = request.form.get("machine_id")
    service_date = request.form.get("service_date")
    next_service_date = request.form.get("next_service_date")
    notes = request.form.get("notes")

    conn = create_connection()
    cursor = conn.cursor()

    query = (
        "INSERT INTO ServiceLogs (machine_id, service_date, service_notes) "
        "VALUES (%s, %s, %s)"
    )
    cursor.execute(query, (machine_id, service_date, notes))
    conn.commit()

    query = "UPDATE Machines SET service_by_date = %s WHERE machine_id = %s"
    cursor.execute(query, (next_service_date, machine_id))
    conn.commit()

    cursor.close()
    conn.close()

    return "Service details logged successfully!"
