###
# Requirements:

# 1. Notification Generation Engine
#    • Simulate 4 notification sources: calendar alerts (upcoming meetings with context), health nudges (sleep/activity anomalies), email digests (important unread emails), and system alerts (low credit balance, new feature)
#    • Each source generates candidate notifications with a priority score, urgency level, and relevance context
#    • Generate at least 48 hours of candidate notifications for a simulated user (some periods busy, some quiet)

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

# 4. iOS Notification Simulation
#    • Build a simple React or SwiftUI mockup that renders the notification feed as it would appear on an iPhone lock screen
#    • Show the 48-hour timeline with notifications appearing at the right times
#    • Include the quiet hours gap and the batching behavior visually
###

