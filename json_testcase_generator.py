import json
from datetime import datetime, timedelta

ALLOWED_HOURS = [8, 9, 10, 11, 13, 14, 15]
START_DATE = datetime(2026, 1, 1)  # arbitrary starting Monday

appointments = []

for i in range(7):  # 7 days: Monday=0 .. Sunday=6
    date = (START_DATE + timedelta(days=i)).strftime("%Y-%m-%d")
    for hour in ALLOWED_HOURS:
        for n in range(5):  # 5 bookings per slot
            appointments.append({
                "name": f"User_{date}_{hour}_{n+1}",
                "date": date,
                "time": f"{hour:02d}:00"
            })

rare_slots = [
    ("2026-01-02", 8),
    ("2026-01-03", 9),
    ("2026-01-04", 10),
    ("2026-01-05", 13),
    ("2026-01-06", 15),
]

appointments = [a for a in appointments if (a["date"], int(a["time"].split(":")[0])) not in rare_slots]

for date, hour in rare_slots:
    appointments.append({
        "name": f"Rare_{date}_{hour}",
        "date": date,
        "time": f"{hour:02d}:00"
    })

with open("appointments.json", "w") as f:
    json.dump(appointments, f, indent=2)

print("Test dataset created: appointments.json")
