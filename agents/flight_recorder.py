from datetime import datetime
from typing import List, Dict

class FlightRecorder:
    def __init__(self):
        self.events: List[Dict] = []

    def log(self, agent: str, action: str, detail: str, status: str = "OK"):
        self.events.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "agent": agent,
            "action": action,
            "detail": detail,
            "status": status,
        })

    def reset(self):
        self.events = []
