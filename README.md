# Voice Sales AI — Streamlit demo

## Overview
This repository demonstrates an automated voice-based system for cold-calling and sales calls. It includes:
- Dialing & call orchestration (example with Twilio)
- STT (speech-to-text) and TTS (text-to-speech) wrappers
- Simple NLU (intent classifier + optional LLM integration)
- CRM integration stubs
- A Streamlit front-end (`app.py`) for orchestration, simulation, and visual monitoring.

**Dataset**:
This demo references a Kaggle dataset at:
`/kaggle/input/call-center-transcripts-dataset`
Use it for training intent models and simulating calls.

## Quick start
1. Create a virtualenv with Python 3.11 and install requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
2. Set environment variables (prefer using Streamlit secrets or .env):

TWILIO_ACCOUNT_SID

TWILIO_AUTH_TOKEN

TWILIO_FROM_NUMBER

GOOGLE_APPLICATION_CREDENTIALS (if using Google Speech)

OPENAI_API_KEY (if using OpenAI)

3. Start local app:
streamlit run app.py

Legal / Safety

Do not run this against real numbers without consent. Confirm local laws before deploying.

Folder structure

(See repository root)

Notes

This demo includes simulation mode so you can test flows without placing calls.

---


