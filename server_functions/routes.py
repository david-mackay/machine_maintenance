from app import app, create_connection
from flask import request, jsonify
from flask_mail import Message
import os
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

