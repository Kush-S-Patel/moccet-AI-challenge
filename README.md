# Moccet AI Notification Generator + React Preview

This project generates simulated notification data based on configurable scenarios and visualizes it in a React mockup UI.

---

## Getting Started

Follow these steps to generate and view mock notifications:

### 1. Clone the Repository

git clone https://github.com/Kush-S-Patel/moccet-AI-challenge.git

cd /moccet-AI-challenge/

---

### 2. Configure and Generate Data

Open `main.py` and adjust the scenario settings inside `configure_scenario()`:

scenario = {
  "bad_sleep": False,
  "low_activity_midday": False,
  "high_email_load": True,
  "urgent_email_burst": True,
  "meeting_heavy_day": False,
  "email_burst_pattern": True
}

Then run:

python main.py

This will:

* Simulate user behavior
* Generate notifications
* Optimize them
* Output `optimized_notifications.json` to:
  `react_mockup/src/`

---

### 3. Launch the React Mockup

cd react_mockup

Install dependencies (first time only):

npm install

Start the development server:

npm start

---

### 4. View the UI

Open your browser and go to:

http://localhost:3000

You should now see your generated notifications rendered in the mock UI.

## Notes

* The `react_mockup/src` directory will be auto-created if it does not exist
* If changes don’t appear, try restarting the React server

---

## 📁 Project Structure

moccet-AI-challenge/
├── main.py
├── optimized_notifications.json
└── react_mockup/
    └── src/
        └── optimized_notifications.json

---

