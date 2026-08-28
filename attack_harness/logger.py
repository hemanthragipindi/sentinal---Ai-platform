import json
import os
from datetime import datetime
from attack_harness.models import AttackResult

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

class AttackLogger:
    def __init__(self):
        self.run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(LOG_DIR, f"attack_run_{self.run_id}.jsonl")
        
    def record(self, result: AttackResult, params=None):
        record_data = result.model_dump()
        record_data["timestamp"] = record_data["timestamp"].isoformat()
        if params:
            record_data["params"] = params.model_dump()
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(record_data) + "\n")
            
        print(f"[{result.attack_type}] Success: {result.success}")

logger = AttackLogger()
