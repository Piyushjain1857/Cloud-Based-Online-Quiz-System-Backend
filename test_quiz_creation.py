import requests
import json

base_url = "http://localhost:3000/api"
admin_id = "1" # Assuming 'piyush@example.com' is ID 1 after seed

payload = {
    "title": "Backend Test Quiz",
    "subject": "Testing",
    "duration": "15",
    "points": "100",
    "date": "2026-03-25",
    "time": "11:00 AM",
    "questions": [
        {
            "text": "Does this work?",
            "options": ["Yes", "No"],
            "correctAnswer": 0
        }
    ]
}

headers = {
    "X-User-ID": admin_id,
    "Content-Type": "application/json"
}

try:
    response = requests.post(f"{base_url}/quizzes/full", data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
