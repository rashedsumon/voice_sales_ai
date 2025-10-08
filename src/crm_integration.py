# Lightweight CRM stubs — implement connectors (HubSpot, Salesforce, Zoho)
import logging
logger = logging.getLogger(__name__)

class CRMStub:
    def __init__(self):
        # In production configure official SDKs & OAuth flows
        self.store = {}

    def get_lead(self, phone_or_id):
        # search simulated store
        return self.store.get(phone_or_id, None)

    def update_lead(self, phone_or_id, updates: dict):
        if phone_or_id not in self.store:
            self.store[phone_or_id] = {}
        self.store[phone_or_id].update(updates)
        logger.info(f"CRM updated {phone_or_id}: {updates}")
        return True

    def log_call(self, phone_or_id, call_data):
        # append call record
        self.store.setdefault(phone_or_id, {}).setdefault("calls", []).append(call_data)
        return True
