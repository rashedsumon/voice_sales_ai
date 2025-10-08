import streamlit as st
import pandas as pd
import time

from src.config import Config
from src.data_prep import load_kaggle_dataset, prepare_intent_training
from src.call_manager import CallManager
from src.crm_integration import CRMStub
from src.nlu import IntentClassifier, generate_agent_response

# -----------------------------------------------------------
# Streamlit App Configuration
# -----------------------------------------------------------
st.set_page_config(page_title="Voice Sales AI", layout="wide")
st.title("🎧 Voice Sales AI — Cold Calling & Sales Assistant Demo")

# -----------------------------------------------------------
# Sidebar: Settings
# -----------------------------------------------------------
st.sidebar.header("⚙️ Settings")
sim_mode = st.sidebar.checkbox(
    "Simulation Mode (no real calls)",
    value=Config.SIMULATION_MODE
)
st.sidebar.info("For production, configure credentials via environment variables or Streamlit secrets.")

# -----------------------------------------------------------
# Load Kaggle Dataset
# -----------------------------------------------------------
st.header("📂 Dataset Preview")

try:
    df = load_kaggle_dataset("/kaggle/input/call-center-transcripts-dataset")
    st.success("✅ Dataset loaded from `/kaggle/input/call-center-transcripts-dataset`")
    st.dataframe(df.head(10))
except Exception as e:
    st.error(f"❌ Could not load dataset automatically: {e}")
    st.info("If running locally, update the data folder path or upload the file manually.")
    df = None

# -----------------------------------------------------------
# Intent Classifier Training (Demo)
# -----------------------------------------------------------
st.header("🧠 Train Simple Intent Classifier")

col1, col2 = st.columns([2, 1])
with col1:
    intent_text_col = st.text_input("Transcript Text Column", value="transcript")
    intent_label_col = st.text_input("Intent Label Column", value="intent")

with col2:
    if st.button("Prepare & Train Classifier (Demo)"):
        if df is None:
            st.error("⚠️ Dataset not loaded.")
        else:
            X, y = prepare_intent_training(df, text_column=intent_text_col, label_column=intent_label_col)
            if y is None:
                st.warning("No labeled intents found. Label a subset manually for training.")
            else:
                classifier = IntentClassifier()
                classifier.train(X, y)
                st.session_state["classifier"] = classifier
                st.success("🎯 Intent classifier trained successfully. Try a prediction below!")

# -----------------------------------------------------------
# Agent Demo — Simulated Call (Text-Based)
# -----------------------------------------------------------
st.header("🤖 AI Agent Demo — Simulated Call")

with st.form("call_simulation_form"):
    phone = st.text_input("Lead Phone (CRM Lookup)", value="+12025550123")
    lead_text = st.text_area(
        "Simulated Lead Utterance",
        value="Hi, I'm not interested in switching providers."
    )
    submit = st.form_submit_button("Run Demo")

    if submit:
        # --- CRM Stub ---
        crm = CRMStub()
        crm.update_lead(phone, {"name": "Test Lead", "status": "new"})
        st.info("📇 CRM Lookup: Found Lead Stub")

        # --- Intent Classification ---
        if "classifier" in st.session_state:
            label = st.session_state["classifier"].predict(lead_text)
            st.success(f"Intent Classifier Prediction: **{label}**")
        else:
            st.warning("No trained classifier found — using simple rule-based intent.")
            label = "negative" if "not interested" in lead_text.lower() else "neutral"
            st.write(f"Rule-based Intent: **{label}**")

        # --- LLM Agent Response ---
        st.write("💬 Generating AI Agent Reply...")
        try:
            system_prompt = (
                "You are a professional, empathetic sales agent. "
                "Respond briefly and include a qualifying question when appropriate."
            )
            conversation = f"Lead: {lead_text}\nAgent:"
            response = generate_agent_response(system_prompt, conversation, temperature=0.3, max_tokens=80)

            st.markdown("**🗣️ Agent Reply (LLM):**")
            st.write(response)
        except Exception as e:
            st.warning(f"LLM generation skipped (missing OPENAI_API_KEY): {e}")

# -----------------------------------------------------------
# Call Orchestration (Simulated / Twilio)
# -----------------------------------------------------------
st.header("📞 Call Orchestration Demo")

with st.expander("Simulate or Place Outbound Call"):
    cm = CallManager()
    call_to = st.text_input("Call To (Phone Number)", value="+12025550123", key="call_to")
    twiml_url = st.text_input("TwiML URL (optional for Twilio)", value="", key="twiml")

    if st.button("Make Call"):
        if sim_mode:
            st.warning("🔁 Running in Simulation Mode — no real call placed.")
        result = cm.make_outbound_call(call_to, twiml_url or None)
        st.write("📋 Call Result:", result)

        outcome = st.selectbox("Call Outcome", [
            "interested", "not_interested", "call_later", "voicemail", "no_answer"
        ])
        notes = st.text_area("Notes", placeholder="Enter any call notes here...")

        if st.button("Record Outcome"):
            cm.record_call_outcome(result.get("sid", "SIM"), outcome, notes)
            st.success("✅ Call outcome recorded successfully.")

# -----------------------------------------------------------
# Footer
# -----------------------------------------------------------
st.markdown("---")
st.caption("🔧 This is a demo orchestration layer — extend each module with real STT, TTS, and CRM connectors.")
