from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

APPOINTMENTS_FILE = 'appointments.json'

if not os.path.exists(APPOINTMENTS_FILE):
    with open(APPOINTMENTS_FILE, 'w') as f:
        json.dump([], f)

def load_appointments():
    with open(APPOINTMENTS_FILE, 'r') as f:
        return json.load(f)

def save_appointments(appointments):
    with open(APPOINTMENTS_FILE, 'w') as f:
        json.dump(appointments, f)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    date = request.form.get('date')
    time = request.form.get('time')

    new_appointment = {
        "name": name,
        "date": date,
        "time": time
    }

    appointments = load_appointments()
    appointments.append(new_appointment)
    save_appointments(appointments)

    return redirect(url_for('appointments'))
    return redirect(url_for('appointments'))

@app.route('/appointments')
def appointments():
    appointments = load_appointments()
    return render_template('appointments.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)