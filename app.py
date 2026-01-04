from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from sklearn.tree import DecisionTreeRegressor
import json
import os

app = Flask(__name__)

APPOINTMENTS_FILE = 'appointments.json'
ALLOWED_HOURS = [8, 9, 10, 11, 13, 14, 15]

if not os.path.exists(APPOINTMENTS_FILE):
    with open(APPOINTMENTS_FILE, 'w') as f:
        json.dump([], f)

def load_appointments():
    with open(APPOINTMENTS_FILE, 'r') as f:
        return json.load(f)

def save_appointments(appointments):
    with open(APPOINTMENTS_FILE, 'w') as f:
        json.dump(appointments, f)

def train_model(appointments):
    X=[]
    slots = []


    for a in appointments:
        dt = datetime.strptime(f"{a['date']} {a['time']}", "%Y-%m-%d %H:%M")
        day = dt.weekday()
        hour = dt.hour
        X.append([day, hour])
        slots.append((day, hour))
    frequency_counts = {}
    for slot in slots:
        if slot in frequency_counts:
            frequency_counts[slot] += 1
        else:
            frequency_counts[slot] = 1

    X=[]
    Y=[]

    for slot, count in frequency_counts.items():
        X.append([slot[0], slot[1]]) 
        Y.append(count)   

    model = DecisionTreeRegressor()            
    model.fit(X, Y)

    return model


def suggest_time(model):
    suggestions = []

    for day in range(7):  # Monday–Sunday
        for hour in ALLOWED_HOURS:
            score = model.predict([[day, hour]])[0]
            suggestions.append((day, hour, score))

    # Manual sort by score (least busy first)
    for i in range(len(suggestions)):
        for j in range(i + 1, len(suggestions)):
            if suggestions[j][2] < suggestions[i][2]:
                suggestions[i], suggestions[j] = suggestions[j], suggestions[i]

    return suggestions[:5]


@app.route('/')
def form():
    appointments = load_appointments()
    suggestions = []

    if len(appointments) > 0:
        model = train_model(appointments)
        suggestions = suggest_time(model)

    return render_template('form.html', suggestions=suggestions)


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    date = request.form.get('date')
    time = request.form.get('time')
    hour = int(time.split(":")[0])

    if hour not in ALLOWED_HOURS:
        return "This time is not allowed", 400
    

    new_appointment = {
        "name": name,
        "date": date,
        "time": time
    }

    appointments = load_appointments()
    appointments.append(new_appointment)
    save_appointments(appointments)

    return redirect(url_for('appointments'))

@app.route('/appointments')
def appointments():
    appointments = load_appointments()
    return render_template('appointments.html', appointments=appointments)
@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run()