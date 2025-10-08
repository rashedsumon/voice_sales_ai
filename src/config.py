# Legal / Safety

# Do not run this against real numbers without consent. Confirm local laws before deploying.

# Folder structure

# (See repository root)

# Notes

# This demo includes simulation mode so you can test flows without placing calls.

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_FROM = os.getenv("TWILIO_FROM_NUMBER")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    SIMULATION_MODE = os.getenv("SIMULATION_MODE", "true").lower() in ("1", "true", "yes")
