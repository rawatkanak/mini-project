# mini-project
#  Hospital Patient Scheduling System

##  Overview
A mini-project integrating **Python**, **ADBMS (SQLite)**, and **DAA (FCFS Scheduling Algorithm)**.

This system helps schedule patients to doctors based on the **First-Come-First-Serve (FCFS)** principle.
It includes doctor & patient management, automatic appointment number generation, and real-time schedule viewing.

---

##  Modules

| File | Description |
|------|--------------|
| `main.py` | GUI built using Tkinter |
| `database.py` | Database creation & management |
| `scheduler.py` | FCFS scheduling and refresh logic |

---

##  Database Design (ER Model)

Entities:
- **Doctor**(`doctor_id`, `name`, `specialization`)
- **Patient**(`patient_id`, `name`, `age`)
- **Appointment**(`appointment_id`, `doctor_id`, `patient_id`, `appointment_no`)

Relationships:
- One Doctor → Many Appointments
- One Patient → Many Appointments

Refer to **`assets/ER_Diagram.png`** for the full E-R model.

---

## ▶ How to Run

```bash
cd Hospital_Patient_Scheduling_System/src
python main.py
```

---

##  Requirements
Install required packages using:
```bash
pip install -r requirements.txt
```

---

##  Features
- Doctor registration
- Automatic appointment number generation
- Per-doctor FCFS patient scheduling
- Schedule refresh and reset options

---


