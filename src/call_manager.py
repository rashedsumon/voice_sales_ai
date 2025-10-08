from twilio.rest import Client
from .config import Config
import time
import logging

logger = logging.getLogger(__name__)

class CallManager:
    def __init__(self):
        self.simulation = Config.SIMULATION_MODE
        if not self.simulation:
            if not Config.TWILIO_SID or not Config.TWILIO_AUTH:
                raise RuntimeError("Twilio credentials not configured.")
            self.client = Client(Config.TWILIO_SID, Config.TWILIO_AUTH)
            self.from_number = Config.TWILIO_FROM

    def make_outbound_call(self, to_number, twiml_url=None, callback_url=None):
        """
        Make an outbound call using Twilio. The `twiml_url` should host TwiML that drives call flow,
        or you can use Twilio's <Say> or <Play> to speak.
        In simulation mode, we return a simulated call record.
        """
        if self.simulation:
            logger.info(f"[SIM] Calling {to_number}")
            # simulate call lifecycle
            time.sleep(1)
            return {"sid": "SIM123", "status": "completed", "to": to_number}
        # real call
        call = self.client.calls.create(
            to=to_number,
            from_=self.from_number,
            url=twiml_url
        )
        return {"sid": call.sid, "status": call.status, "to": to_number}

    def record_call_outcome(self, call_sid, outcome, notes=""):
        # In production, write to DB or CRM
        logger.info(f"Recording call {call_sid}: {outcome} - {notes}")
        return True
