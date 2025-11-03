import sqlite3

DB_NAME = "hospital.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Doctors table
    c.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL
        )
    """)
    # Patients table (basic patient info)
    c.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        )
    """)
    # Appointments table - links patient to doctor and stores a per-doctor appointment_no
    c.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_no INTEGER NOT NULL,
            start_time TEXT,
            end_time TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)
        )
    """)
    conn.commit()
    conn.close()

def add_doctor(name, specialization):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO doctors (name, specialization) VALUES (?, ?)", (name, specialization))
    conn.commit()
    conn.close()

def get_doctors():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT doctor_id, name, specialization FROM doctors ORDER BY doctor_id")
    rows = c.fetchall()
    conn.close()
    return rows

def add_patient_and_create_appointment(name, age, doctor_id):
    """
    Adds patient and creates an appointment for the given doctor.
    Appointment number is generated per-doctor using FCFS (max + 1).
    Returns (patient_id, appointment_no).
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Insert patient
    c.execute("INSERT INTO patients (name, age) VALUES (?, ?)", (name, age))
    patient_id = c.lastrowid
    # compute next appointment_no for this doctor
    c.execute("SELECT MAX(appointment_no) FROM appointments WHERE doctor_id=?", (doctor_id,))
    row = c.fetchone()
    next_no = 1 if row is None or row[0] is None else row[0] + 1
    # insert appointment (start_time/end_time can be assigned by scheduler later)
    c.execute("""INSERT INTO appointments (patient_id, doctor_id, appointment_no, start_time, end_time)
                 VALUES (?, ?, ?, ?, ?)""", (patient_id, doctor_id, next_no, None, None))
    conn.commit()
    conn.close()
    return patient_id, next_no

def get_appointments():
    """
    Returns list of appointments joined with patient and doctor names,
    ordered by doctor and appointment_no (FCFS per doctor).
    Each row: (appointment_id, appointment_no, patient_name, age, doctor_name, specialization, start_time, end_time)
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT a.appointment_id, a.appointment_no, p.name, p.age, d.name, d.specialization, a.start_time, a.end_time, a.doctor_id
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        ORDER BY d.name ASC, a.appointment_no ASC
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def clear_patients_and_appointments():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM appointments")
    c.execute("DELETE FROM patients")
    conn.commit()
    conn.close()

def reset_database():
    """Delete the DB file to start fresh. Use with caution."""
    try:
        import os
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)
    except Exception:
        pass
