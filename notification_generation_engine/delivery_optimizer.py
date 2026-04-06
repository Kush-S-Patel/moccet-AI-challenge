# 2. Delivery Optimization
#    • Not every candidate notification should be sent. Implement a delivery filter that suppresses low-value notifications.
#    • Enforce a daily notification budget (e.g. max 5 notifications per day). If more than 5 candidates exist, rank and send only the top 5.
#    • Respect quiet hours (no notifications between 10pm and 7am unless critical)
#    • Batch related notifications ("You have 3 unread emails from your team" instead of 3 separate pings)
#    • Implement cooldown logic so the same notification type doesn't fire back-to-back (e.g. no two health nudges within 4 hours)

# 3. Notification Content
#    • Each notification should have: a short title (under 50 characters), a body (1 to 2 sentences), the source service, a deep link action ("Open meeting prep" or "View email"), and a dismiss option
#    • The content should be personalized and contextual, not generic. "Meeting with Sarah in 15 min" not "You have an upcoming event"
#    • Include source pills in the notification body so the user knows where the info came from ([Calendar] [Gmail])
#basing these based on importance and typical frequency of these notifications
import datetime
from collections import defaultdict

QUIET_HOURS = (22, 7)
MAX_PER_DAY = 5

COOLDOWN_HOURS = {
    "email": 2,
    "health": 4,
    "calendar": 1,
    "system": 6
}

MIN_SCORE_THRESHOLD = 0.5  # suppress low-value notifications


# ------------------------
# Helpers
# ------------------------

def parse_ts(n):
    return datetime.datetime.fromisoformat(str(n["timestamp"]))


def is_quiet_hour(ts):
    return ts.hour >= QUIET_HOURS[0] or ts.hour < QUIET_HOURS[1]


# ------------------------
# 1. Low Value Filter
# ------------------------

def filter_low_value(notifs):
    return [n for n in notifs if n["score"] >= MIN_SCORE_THRESHOLD]


# ------------------------
# 2. Quiet Hours
# ------------------------

def apply_quiet_hours(notifs):
    filtered = []

    for n in notifs:
        ts = parse_ts(n)

        if is_quiet_hour(ts):
            if n["priority"] >= 0.9:  # allow critical
                filtered.append(n)
        else:
            filtered.append(n)

    return filtered


# ------------------------
# 3. Cooldown
# ------------------------

def apply_cooldown(notifs):
    last_sent = {}
    result = []

    for n in sorted(notifs, key=lambda x: x["timestamp"]):
        ts = parse_ts(n)
        src = n["source"]

        if src in last_sent:
            diff = (ts - last_sent[src]).total_seconds() / 3600
            if diff < COOLDOWN_HOURS.get(src, 2):
                continue

        last_sent[src] = ts
        result.append(n)

    return result


# ------------------------
# 4. Email Batching (KEY)
# ------------------------

def batch_emails(notifs):
    batched = []
    email_groups = defaultdict(list)

    for n in notifs:
        if n["source"] == "email":
            ts = parse_ts(n)
            key = (ts.date(), ts.hour // 2)  # batch per 2 hour window
            email_groups[key].append(n)
        else:
            batched.append(n)

    for (day, hour), group in email_groups.items():
        if len(group) == 1:
            batched.append(group[0])
            continue

        # batch multiple emails
        latest = max(group, key=lambda x: x["timestamp"])

        batched.append({
            "id": f"batch-{day}-{hour}",
            "timestamp": latest["timestamp"],
            "source": "email",
            "type": "email_batch",
            "priority": max(n["priority"] for n in group),
            "urgency": max(n["urgency"] for n in group),
            "relevance": max(n["relevance"] for n in group),
            "score": max(n["score"] for n in group),
            "content": {
                "title": f"{len(group)} unread emails",
                "body": "Multiple senders [Gmail]",
                "deep_link": "app://email",
                "dismissible": True
            }
        })

    return batched


# ------------------------
# 5. Content Normalization
# ------------------------

def normalize_content(notifs):
    for n in notifs:
        content = n.get("content", {})

        # enforce title length
        if "title" in content:
            content["title"] = content["title"][:50]

        # ensure dismiss
        content["dismissible"] = True

        # ensure deep link exists
        if "deep_link" not in content:
            content["deep_link"] = f"app://{n['source']}"

        # enforce source pill if missing
        if "[" not in content.get("body", ""):
            content["body"] += f" [{n['source'].capitalize()}]"

        n["content"] = content

    return notifs


# ------------------------
# 6. Group by Day
# ------------------------

def group_by_day(notifs):
    grouped = defaultdict(list)

    for n in notifs:
        ts = parse_ts(n)
        grouped[ts.date()].append(n)

    return grouped


# ------------------------
# 7. Daily Budget
# ------------------------

def apply_daily_budget(grouped):
    final = []

    for day, items in grouped.items():
        items.sort(key=lambda x: x["score"], reverse=True)

        selected = items[:MAX_PER_DAY]
        selected.sort(key=lambda x: x["timestamp"])

        final.extend(selected)

    return final


# ------------------------
# MASTER PIPELINE
# ------------------------

def optimize_notifications(notifications):
    step1 = filter_low_value(notifications)
    step2 = apply_quiet_hours(step1)
    step3 = batch_emails(step2)
    step4 = apply_cooldown(step3)
    step5 = normalize_content(step4)

    grouped = group_by_day(step5)
    final = apply_daily_budget(grouped)

    return final