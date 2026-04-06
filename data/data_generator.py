import random
import uuid
from datetime import datetime, timedelta
import json
import os

# ------------------------
# Config
# ------------------------

USER_NAME = "Kush Patel"
HOURS_TO_SIMULATE = 48
WORK_HOURS = (9, 17)

OUTPUT_DIRS = {
    "calendar": "data/calendar_meetings",
    "emails": "data/emails",
    "health": "data/health",
    "system": "data/system_alerts",
}

DEFAULT_SCENARIO = {
    "bad_sleep": False,
    "low_activity_midday": False,
    "high_email_load": False,
    "urgent_email_burst": False,
    "meeting_heavy_day": False,
    "email_burst_pattern": False,
}

# ------------------------
# Helpers
# ------------------------

def ensure_dirs():
    for path in OUTPUT_DIRS.values():
        os.makedirs(path, exist_ok=True)


def save_json(data, folder, filename):
    path = os.path.join(OUTPUT_DIRS[folder], filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def random_time(start):
    return start + timedelta(minutes=random.randint(0, HOURS_TO_SIMULATE * 60))


def is_work_hour(dt):
    return WORK_HOURS[0] <= dt.hour <= WORK_HOURS[1]


# ------------------------
# Calendar
# ------------------------

def generate_calendar_events(start_time, scenario):
    meetings = []

    base_count = random.randint(6, 10)
    if scenario.get("meeting_heavy_day"):
        base_count += 5

    for _ in range(base_count):
        time = random_time(start_time)

        while not is_work_hour(time):
            time = random_time(start_time)

        meetings.append({
            "id": str(uuid.uuid4()),
            "title": random.choice(["1:1 with Sarah", "Team Sync", "Client Call"]),
            "time": time,
            "context": random.choice(["Discuss roadmap", "Prep for launch", "Review updates"])
        })

    save_json(meetings, "calendar", "meetings.json")
    return meetings


# ------------------------
# Emails
# ------------------------

def generate_emails(start_time, scenario):
    emails = []

    base_count = random.randint(15, 25)
    if scenario.get("high_email_load"):
        base_count += 15

    for i in range(base_count):

        if scenario.get("email_burst_pattern"):
            base_hour = random.choice([9, 13, 18])  # common email spikes

            timestamp = start_time + timedelta(
                days=random.randint(0, 1),
                hours=base_hour,
                minutes=random.randint(0, 10)  # tight clustering
            )

        else:
            # default random distribution
            timestamp = start_time + timedelta(
                hours=random.randint(0, 48)
            )

        subject = random.choice([
            "Q3 Report Update",
            "Action Required",
            "Quick Sync",
            "Project Update"
        ])

        if scenario.get("urgent_email_burst") and i < 5:
            subject = "URGENT: Server Downtime"

        emails.append({
            "id": str(uuid.uuid4()),
            "sender": random.choice([
                "boss@company.com",
                "team@company.com",
                "sarah@company.com"
            ]),
            "important": random.random() > 0.5,
            "subject": subject,
            "timestamp": timestamp,
            "read": random.random() > 0.6
        })

    save_json(emails, "emails", "emails.json")
    return emails


# ------------------------
# Health
# ------------------------

def generate_health_data(start_time, scenario):
    health_logs = []

    for day in range(2):
        date = (start_time + timedelta(days=day)).date()

        # ---- Sleep ----
        if scenario.get("bad_sleep"):
            sleep_hours = random.choice([3, 4])
        else:
            sleep_hours = random.choice([6, 7, 8])

        hourly_steps = []
        total_steps = 0

        for hour in range(24):
            if scenario.get("low_activity_midday") and 10 <= hour <= 16:
                steps = random.randint(0, 100)
            else:
                if 0 <= hour <= 6:
                    steps = random.randint(0, 100)
                elif 7 <= hour <= 9:
                    steps = random.randint(200, 1500)
                elif 10 <= hour <= 16:
                    steps = random.randint(300, 2000)
                elif 17 <= hour <= 20:
                    steps = random.randint(500, 3000)
                else:
                    steps = random.randint(50, 500)

            hourly_steps.append({"hour": hour, "steps": steps})
            total_steps += steps

        health_logs.append({
            "date": str(date),
            "sleep_hours": sleep_hours,
            "avg_sleep": 6,
            "total_steps": total_steps,
            "hourly_steps": hourly_steps
        })

    save_json(health_logs, "health", "health.json")
    return health_logs


# ------------------------
# System
# ------------------------

def generate_system_alerts(start_time, scenario):
    alerts = []

    alerts.append({
        "id": str(uuid.uuid4()),
        "type": "low_credit",
        "days_left": random.randint(1, 5),
        "timestamp": start_time + timedelta(hours=random.randint(0, 48))
    })

    alerts.append({
        "id": str(uuid.uuid4()),
        "type": "feature_release",
        "feature": "Smart Summaries",
        "timestamp": start_time + timedelta(hours=random.randint(0, 48))
    })

    save_json(alerts, "system", "alerts.json")
    return alerts


# ------------------------
# Master
# ------------------------

def generate_all(scenario=None):
    ensure_dirs()

    # fallback if None passed
    if scenario is None:
        scenario = DEFAULT_SCENARIO.copy()

    start_time = datetime.now()

    print(f"Generating synthetic data for {USER_NAME}...")
    print(f"Scenario: {scenario}")

    return {
        "calendar": generate_calendar_events(start_time, scenario),
        "emails": generate_emails(start_time, scenario),
        "health": generate_health_data(start_time, scenario),
        "system": generate_system_alerts(start_time, scenario)
    }


if __name__ == "__main__":
    generate_all()