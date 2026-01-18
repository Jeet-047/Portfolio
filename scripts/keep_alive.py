import os
import requests

CONTACT_API_URL = os.getenv("CONTACT_API_URL")

if not CONTACT_API_URL:
    raise RuntimeError("CONTACT_API_URL is not set")

payload = {
    "name": "System Keep Alive",
    "email": "system@keepalive.bot",
    "subject": "Supabase Keep Alive",
    "message": "Automated keep-alive message to prevent Supabase pausing."
}

response = requests.post(CONTACT_API_URL, json=payload, timeout=10)

if response.status_code != 200:
    raise RuntimeError(
        f"Keep-alive failed: {response.status_code} {response.text}"
    )

print("✅ Keep-alive! Message sent successfully")
