import streamlit as st
import pandas as pd
import time
from src.config import Config
from src.data_prep import load_kaggle_dataset, prepare_intent_training
from src.call_manager import CallManager
from src.crm_integration import CRMStub
from src.nlu import IntentClassifier, generate_agent_response

st.set_page_config(page_title="Voice Sales AI", layout="wide")
st.title("Voice Sales AI — Cold Calling & Sales Demo")

# Sidebar: settings & API keys
st.sidebar.header("Settings")
sim_mode = st.sidebar.checkbox("Simulation mode (no real calls)", value=Config.SIMULATION_MODE)
st.sidebar.write("Set environment variables or Streamlit secrets for production credentials.")

# Load dataset preview
st.header("Dataset (Kaggle) preview")
try:
    df = load_kaggle_dataset("/kaggle/input/call-center-transcripts-dataset")
    st.write("Dataset loaded from `/kaggle/input/call-center-transcripts-dataset`")
    st.dataframe(df.head(10))
except Exception as e:
    st.error(f"Could not load dataset automatically: {e}")
    st.info("If running locally, point data folder to the Kaggle dataset path or upload file manually.")
    df = None

# Simple NLU training section
st.header("Train simple intent classifier (demo)")
col1, col2 = st.columns([2,1])
with col1:
    intent_text_col = st.text_input("Transcript text column name", value="transcript")
    intent_label_col = st.text_input("Label column (if present)", value="intent")

with col2:
    if st.button("Prepare & Train (demo)"):
        if df is None:
            st.error("Dataset not loaded.")
        else:
            X, y = prepare_intent_training(df, text_column=intent_text_col, label_column=intent_label_col)
            if y is None:
                st.warning("No labeled intents found. You can label a subset manually for training.")
            else:
                classifier = IntentClassifier()
                classifier.train(X, y)
                st.success("Intent classifier trained (demo). You can now run single predictions below.")
                st.session_state["classifier"] = classifier

# Single-prediction / agent demo
st.header("Agent demo: simulate a call (text-based)")
with st.form("call_sim"):
    phone = st.text_input("Lead phone (for CRM lookup)", value="+12025550123")
    lead_text = st.text_area("Simulated lead utterance (what lead says)", value="Hi, I'm not interested in switching providers.")
    submit = st.form_submit_button("Run demo")
    if submit:
        crm = CRMStub()
        crm.update_lead(phone, {"name": "Test Lead", "status": "new"})
        st.info("CRM: found lead stub")
        # If classifier available use it
        if "classifier" in st.session_state:
            label = st.session_state["classifier"].predict(lead_text)
            st.write("Intent classifier predicted:", label)
        else:
            st.write("No supervised classifier found — using simple rules.")
            label = "negative" if "not interested" in lead_text.lower() else "neutral"
            st.write("Rule-based label:", label)

        # LLM to craft agent reply (optional)
        st.write("Generating agent reply (LLM) if API key present...")
        try:
            system_prompt = "You are a helpful sales agent. Keep replies short and ask a qualifying question when appropriate."
            conversation_history = f"Lead: {lead_text}\nAgent:"
            resp = generate_agent_response(system_prompt, conversation_history, temperature=0.2, max_tokens=80)
            st.markdown("**Agent reply (LLM):**")
            st.write(resp)
        except Exception as e:
            st.warning(f"LLM generation skipped (needs OPENAI_API_KEY): {e}")

# Call orchestration demo (simulation or Twilio)
st.header("Call Orchestration")
with st.expander("Place single outbound call (simulated or Twilio)"):
    cm = CallManager()
    call_to = st.text_input("Call to (phone)", value="+12025550123", key="call_to")
    twiml_url = st.text_input("TwiML URL (optional for Twilio)", value="", key="twiml")
    if st.button("Make call"):
        if sim_mode:
            st.warning("Running in simulation mode.")
        result = cm.make_outbound_call(call_to, twiml_url if twiml_url else None)
        st.write("Call result:", result)
        # record outcome interactively
        outcome = st.selectbox("Outcome", ["interested","not_interested","call_later","voicemail","no_answer"])
        notes = st.text_area("Notes", value="")
        if st.button("Record outcome"):
            cm.record_call_outcome(result.get("sid", "SIM"), outcome, notes)
            st.success("Recorded.")

st.markdown("---")
st.write("This Streamlit app is a demo orchestration layer — extend each module to add real STT, TTS, and CRM connectors.")
