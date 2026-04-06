
# 1. Notification Generation Engine
#    • Simulate 4 notification sources: calendar alerts (upcoming meetings with context), health nudges (sleep/activity anomalies), email digests (important unread emails), and system alerts (low credit balance, new feature)
#    • Each source generates candidate notifications with a priority score, urgency level, and relevance context
#    • Generate at least 48 hours of candidate notifications for a simulated user (some periods busy, some quiet)

#Notification Generation Engine
# This module implements the core logic for generating notifications based on the synthetic data created by the data generator. It simulates 4 notification sources: calendar alerts, health nudges, email digests, and system alerts. 
# Each source generates candidate notifications with a priority score, urgency level, and relevance context.

import json
import os   
import uuid
from datetime import datetime, timedelta, time

DATA_DIR = "data"
URGENCY_WEIGHT = 0.5
PRIORITY_WEIGHT = 0.2
RELEVANCE_WEIGHT = 0.3

# ------------------------
# Helpers
# ------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def compute_score(priority, urgency, relevance):
    return round(
        URGENCY_WEIGHT * urgency +
        RELEVANCE_WEIGHT * relevance +
        PRIORITY_WEIGHT * priority,
        3
    )


# ------------------------
# Calendar Notifications
# ------------------------

def generate_calendar_notifications(meetings):
    notifications = []
    now = datetime.now()

    for m in meetings:
        meeting_time = datetime.fromisoformat(m["time"])
        minutes_to_meeting = (meeting_time - now).total_seconds() / 60

        if minutes_to_meeting <= 0:
            continue

        # ------------------------
        # 1. 1-Hour Before (Prep)
        # ------------------------
        if minutes_to_meeting <= 24 * 60:
            notif_time = meeting_time - timedelta(hours=1)

            priority = 0.85
            urgency = 0.6
            relevance = 0.9

            title = f"{m['title']} in 1 hour"
            body = f"{m['context']} [Calendar]"

            notifications.append({
                "id": str(uuid.uuid4()),
                "timestamp": notif_time,
                "source": "calendar",
                "type": "meeting_prep",
                "priority": priority,
                "urgency": urgency,
                "relevance": relevance,
                "score": compute_score(priority, urgency, relevance),
                "content": {
                    "title": title[:50],
                    "body": body,
                    "deep_link": "app://calendar"
                }
            })

        # ------------------------
        # 2. 15-Min Before (Urgent)
        # ------------------------
        if minutes_to_meeting <= 24 * 60:
            notif_time = meeting_time - timedelta(minutes=15)

            priority = 0.9
            urgency = 1.0
            relevance = 0.9

            title = f"{m['title']} in 15 min"
            body = f"{m['context']} [Calendar]"

            notifications.append({
                "id": str(uuid.uuid4()),
                "timestamp": notif_time,
                "source": "calendar",
                "type": "meeting_soon",
                "priority": priority,
                "urgency": urgency,
                "relevance": relevance,
                "score": compute_score(priority, urgency, relevance),
                "content": {
                    "title": title[:50],
                    "body": body,
                    "deep_link": "app://calendar"
                }
            })

        # ------------------------
        # 3. Starting Now
        # ------------------------
        if minutes_to_meeting <= 10:
            notif_time = meeting_time

            priority = 1.0
            urgency = 1.0
            relevance = 0.95

            title = f"{m['title']} starting now"
            body = f"{m['context']} [Calendar]"

            notifications.append({
                "id": str(uuid.uuid4()),
                "timestamp": notif_time,
                "source": "calendar",
                "type": "meeting_now",
                "priority": priority,
                "urgency": urgency,
                "relevance": relevance,
                "score": compute_score(priority, urgency, relevance),
                "content": {
                    "title": title[:50],
                    "body": body,
                    "deep_link": "app://calendar"
                }
            })

    return notifications


# ------------------------
# Email Notifications
# ------------------------
def generate_email_notifications(emails):
    notifications = []

    buckets = {}

    for e in emails:
        if e.get("read", False):
            continue

        ts = datetime.fromisoformat(e["timestamp"])

        bucket_key = (
            ts.date(),
            ts.hour,
            ts.minute // 30
        )

        buckets.setdefault(bucket_key, []).append((e, ts))

    for group in buckets.values():

        # ------------------------
        # SINGLE EMAIL
        # ------------------------
        if len(group) == 1:
            e, ts = group[0]

            notifications.append({
                "id": str(uuid.uuid4()),
                "timestamp": ts,
                "source": "email",
                "type": "email",
                "priority": 0.8,
                "urgency": 0.7,
                "relevance": 0.8,
                "score": compute_score(0.8, 0.7, 0.8),
                "content": {
                    "title": "New email",
                    "body": f"{e['sender']}: {e['subject']} [Gmail]",
                    "deep_link": "app://email",
                    "dismissible": True
                }
            })

        # ------------------------
        # BATCHED EMAILS
        # ------------------------
        else:
            latest = max(group, key=lambda x: x[1])  

            notifications.append({
                "id": str(uuid.uuid4()),
                "timestamp": latest[1], 
                "source": "email",
                "type": "email_batch",
                "priority": 0.85,
                "urgency": 0.75,
                "relevance": 0.85,
                "score": compute_score(0.85, 0.75, 0.85),
                "content": {
                    "title": f"{len(group)} unread emails",
                    "body": "Multiple senders [Gmail]",
                    "deep_link": "app://email",
                    "dismissible": True
                }
            })

    return notifications
# ------------------------
# Health Notifications
# ------------------------

def generate_health_notifications(health_logs):
    notifications = []

    for log in health_logs:
        log_date = datetime.fromisoformat(log["date"])
        sleep_diff = log["sleep_hours"] - log["avg_sleep"]

        if sleep_diff < -1:
            priority = 0.7
            urgency = 0.6
            relevance = 0.9

            title = "Low sleep detected"
            body = f"{abs(sleep_diff)}h below average. Take it easy today [Health]"

            notif = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.combine(
                    datetime.fromisoformat(str(log["date"])),
                    datetime.min.time()
                ) + timedelta(hours=9),
                "source": "health",
                "type": "sleep_alert",
                "priority": priority,
                "urgency": urgency,
                "relevance": relevance,
                "score": compute_score(priority, urgency, relevance),
                "content": {
                    "title": title[:50],
                    "body": body,
                    "deep_link": "app://health"
                }
            }

            notifications.append(notif)

        print("SLEEP:", log["sleep_hours"], "AVG:", log["avg_sleep"])
        #So ideally we'd want a notifcation like the below to be pushed sometime midday, not late night when the user is likely asleep. but for simplicity of the simulation, we'll just set it to a fixed time in the afternoon. in a real system, we'd want to personalize the timing based on the user's typical activity patterns (like when they usually go for walks or workouts) and also add some randomness so it's not always at the same time.
        # if log["steps"] < 4000:
        #     priority = 0.5
        #     urgency = 0.4
        #     relevance = 0.6

        #     title = "Low activity today"
        #     body = f"Only {log['steps']} steps so far [Health]"

        #     notif = {
        #         "id": str(uuid.uuid4()),
        #         "timestamp": datetime.now().replace(hour=15, minute=0),
        #         "source": "health",
        #         "type": "activity_alert",
        #         "priority": priority,
        #         "urgency": urgency,
        #         "relevance": relevance,
        #         "score": compute_score(priority, urgency, relevance),
        #         "content": {
        #             "title": title[:50],
        #             "body": body,
        #             "deep_link": "app://health"
        #         }
        #     }
        
        #     notifications.append(notif)
        #going to actually make a change from here and generate the synthetic data to track steps on a distribution over time (like Apple health) rather than a fixed amount, so we can send targeted notifs
        
        # ------------------------
        # Steps Alert Logic
        # ------------------------
        hourly = log["hourly_steps"]

        # cumulative steps until 5pm (can personalize this later based on user's health steps patterns, to track anomalies and send notifcations when step counts are off)
        steps_until_5pm = sum(h["steps"] for h in hourly if h["hour"] <= 17)

        if steps_until_5pm < 4000: #can also personalize the 4000 number based on user's typical step patterns
            priority = 0.6
            urgency = 0.5
            relevance = 0.8

            notif = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.combine(log_date, time(hour=17)),
                "source": "health",
                "type": "midday_activity_alert",
                "priority": priority,
                "urgency": urgency,
                "relevance": relevance,
                "score": compute_score(priority, urgency, relevance),
                "content": {
                    "title": "Low activity so far",
                    "body": f"Only {steps_until_5pm} steps by 5PM [Health]",
                    "deep_link": "app://health"
                }
            }

            notifications.append(notif)

        # ------------------------
        # Inactivity Alert Logic
        # ------------------------
        for i in range(3, 24):
            last_3_hours = hourly[i-3:i]
            steps_last_3 = sum(h["steps"] for h in last_3_hours)

            # skip likely sleeping hours (also would personalize this to be when user actually sleeps based on previous data)
            if i < 9 or i > 20: 
                continue

            if steps_last_3 < 300:
                priority = 0.65
                urgency = 0.6
                relevance = 0.7

                notif_time = datetime.combine(log_date, time(hour=i))

                notif = {
                    "id": str(uuid.uuid4()),
                    "timestamp": notif_time,
                    "source": "health",
                    "type": "inactivity_alert",
                    "priority": priority,
                    "urgency": urgency,
                    "relevance": relevance,
                    "score": compute_score(priority, urgency, relevance),
                    "content": {
                        "title": "You've been inactive",
                        "body": f"Very little movement in the past 3 hours [Health]",
                        "deep_link": "app://health"
                    }
                }

                notifications.append(notif)

                # cooldown: only send one inactivity alert per day
                break
                #the above implementation is a "smart" version of our total step count. it lets the user actually know when they are being more inactive than usual, rather than a vague "you have less than 4000 steps"
    return notifications


# ------------------------
# System Notifications
# ------------------------

def generate_system_notifications(alerts):
    notifications = []

    for a in alerts:
        timestamp = datetime.fromisoformat(a["timestamp"])

        if a["type"] == "low_credit":
            priority = 1.0
            urgency = 0.9 if a["days_left"] <= 2 else 0.7
            relevance = 0.9

            title = "Credits running low"
            body = f"{a['days_left']} days remaining [System]"

        elif a["type"] == "feature_release":
            priority = 0.4
            urgency = 0.3
            relevance = 0.5

            title = "New feature available"
            body = f"Try {a['feature']} now [System]"

        else:
            continue

        notif = {
            "id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "source": "system",
            "type": a["type"],
            "priority": priority,
            "urgency": urgency,
            "relevance": relevance,
            "score": compute_score(priority, urgency, relevance),
            "content": {
                "title": title[:50],
                "body": body,
                "deep_link": "app://system"
            }
        }

        notifications.append(notif)

    return notifications


# ------------------------
# Master Engine
# ------------------------

def generate_all_notifications():
    calendar = load_json(os.path.join(DATA_DIR, "calendar_meetings/meetings.json"))
    emails = load_json(os.path.join(DATA_DIR, "emails/emails.json"))
    health = load_json(os.path.join(DATA_DIR, "health/health.json"))
    system = load_json(os.path.join(DATA_DIR, "system_alerts/alerts.json"))

    notifications = []
    notifications += generate_calendar_notifications(calendar)
    notifications += generate_email_notifications(emails)
    notifications += generate_health_notifications(health)
    notifications += generate_system_notifications(system)

    # sort chronologically
    notifications.sort(key=lambda x: x["timestamp"])

    return notifications


if __name__ == "__main__":
    notifs = generate_all_notifications()
    #sorting by score for analysis
    notifs.sort(key=lambda x: x["score"], reverse=True)

    output_path = os.path.join(os.path.dirname(__file__), "notifications_output.json")

    with open(output_path, "w") as f:
        json.dump(notifs, f, indent=2, default=str)

    print(f"Saved {len(notifs)} notifications (sorted by score) to {output_path}")