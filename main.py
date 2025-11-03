import tkinter as tk
from tkinter import ttk, messagebox
import database
from scheduler import sort_appointments_fcfs

# Initialize / create fresh DB (since new database requested)
# Remove existing DB if present to start clean
try:
    import os
    if os.path.exists("hospital.db"):
        os.remove("hospital.db")
except Exception:
    pass

database.create_tables()

root = tk.Tk()
root.title("Hospital Patient Scheduling System")
root.geometry("900x600")
root.resizable(False, False)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ---------- TAB 1: ADD DOCTOR ----------
frame_doctor = ttk.Frame(notebook)
notebook.add(frame_doctor, text="Add Doctor")

ttk.Label(frame_doctor, text="Doctor Name:").grid(row=0, column=0, padx=10, pady=8, sticky="e")
ttk.Label(frame_doctor, text="Specialization:").grid(row=1, column=0, padx=10, pady=8, sticky="e")

doc_name_entry = ttk.Entry(frame_doctor, width=40)
doc_spec_entry = ttk.Entry(frame_doctor, width=40)
doc_name_entry.grid(row=0, column=1)
doc_spec_entry.grid(row=1, column=1)

def add_doctor():
    name = doc_name_entry.get().strip()
    spec = doc_spec_entry.get().strip()
    if not name or not spec:
        messagebox.showwarning("Input Error", "Please enter doctor name and specialization.")
        return
    database.add_doctor(name, spec)
    messagebox.showinfo("Success", f"Doctor '{name}' added.")
    doc_name_entry.delete(0, tk.END); doc_spec_entry.delete(0, tk.END)
    refresh_doctors_table(); refresh_doctor_combobox()

ttk.Button(frame_doctor, text="Add Doctor", command=add_doctor).grid(row=2, column=0, columnspan=2, pady=10)

# Doctor table
doc_table = ttk.Treeview(frame_doctor, columns=("ID","Name","Spec"), show="headings", height=8)
for col,w in zip(("ID","Name","Spec"), (60,300,300)):
    doc_table.heading(col, text=col); doc_table.column(col, width=w, anchor="center")
doc_table.grid(row=3, column=0, columnspan=2, pady=10)

def refresh_doctors_table():
    for r in doc_table.get_children():
        doc_table.delete(r)
    for did, name, spec in database.get_doctors():
        doc_table.insert("", "end", values=(did, name, spec))

refresh_doctors_table()

# ---------- TAB 2: ADD PATIENT ----------
frame_patient = ttk.Frame(notebook)
notebook.add(frame_patient, text="Add Patient")

ttk.Label(frame_patient, text="Patient Name:").grid(row=0, column=0, padx=10, pady=8, sticky="e")
ttk.Label(frame_patient, text="Age:").grid(row=1, column=0, padx=10, pady=8, sticky="e")
ttk.Label(frame_patient, text="Select Doctor:").grid(row=2, column=0, padx=10, pady=8, sticky="e")

patient_name_entry = ttk.Entry(frame_patient, width=40)
patient_age_entry = ttk.Entry(frame_patient, width=10)
patient_name_entry.grid(row=0, column=1)
patient_age_entry.grid(row=1, column=1, sticky="w")

doctor_values = [f"{d[1]} - {d[2]}" for d in database.get_doctors()]
doctor_combobox = ttk.Combobox(frame_patient, values=doctor_values, state="readonly", width=37)
doctor_combobox.grid(row=2, column=1, sticky="w")

def refresh_doctor_combobox():
    doctor_combobox['values'] = [f"{d[1]} - {d[2]}" for d in database.get_doctors()]

def add_patient():
    name = patient_name_entry.get().strip()
    age = patient_age_entry.get().strip()
    doc_display = doctor_combobox.get().strip()
    if not name or not age or not doc_display:
        messagebox.showwarning("Input Error", "Fill all fields and select a doctor.")
        return
    try:
        age_i = int(age)
    except ValueError:
        messagebox.showwarning("Input Error", "Age must be a number.")
        return
    # find doctor id
    doc_id = None
    for d in database.get_doctors():
        display = f"{d[1]} - {d[2]}"
        if display == doc_display:
            doc_id = d[0]; break
    if doc_id is None:
        messagebox.showerror("Error", "Selected doctor not found. Refresh doctors list.")
        return
    patient_id, app_no = database.add_patient_and_create_appointment(name, age_i, doc_id)
    messagebox.showinfo("Appointment Created", f"Patient added with Appointment No. {app_no} for the selected doctor.")
    patient_name_entry.delete(0, tk.END); patient_age_entry.delete(0, tk.END)
    refresh_schedule_table()

ttk.Button(frame_patient, text="Add Patient & Create Appointment", command=add_patient).grid(row=3, column=0, columnspan=2, pady=10)

# ---------- TAB 3: VIEW SCHEDULE ----------
frame_schedule = ttk.Frame(notebook)
notebook.add(frame_schedule, text="View Schedule")

cols = ("Appt ID", "Appt No", "Patient", "Age", "Doctor", "Specialization", "Start", "End")
schedule_table = ttk.Treeview(frame_schedule, columns=cols, show="headings", height=16)
for col, w in zip(cols, (80,90,200,60,180,140,100,100)):
    schedule_table.heading(col, text=col); schedule_table.column(col, width=w, anchor="center")
schedule_table.pack(fill="both", expand=True, padx=10, pady=10)

def refresh_schedule_table():
    for r in schedule_table.get_children():
        schedule_table.delete(r)
    rows = database.get_appointments()
    rows = sort_appointments_fcfs(rows)
    for appt_id, appt_no, pname, age, dname, spec, start, end, did in rows:
        schedule_table.insert("", "end", values=(appt_id, appt_no, pname, age, dname, spec, start or "-", end or "-"))

ttk.Button(frame_schedule, text="Refresh Schedule", command=refresh_schedule_table).pack(pady=6)
ttk.Button(frame_schedule, text="Refresh Doctor List", command=refresh_doctor_combobox).pack(pady=2)

def clear_all():
    if not messagebox.askyesno("Confirm", "This will delete ALL patients and appointments. Continue?"):
        return
    database.clear_patients_and_appointments()
    refresh_schedule_table()
    messagebox.showinfo("Cleared", "All patients and appointments deleted.")

ttk.Button(frame_schedule, text="Clear Schedules", command=clear_all).pack(pady=6)

refresh_schedule_table()

root.mainloop()
