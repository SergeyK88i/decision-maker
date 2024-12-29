from typing import Dict, List
import sqlite3
from datetime import datetime

class HistoricalDatabase:
    def __init__(self):
        self.db_path = 'integration_history.db'
        self.init_db()
        
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS integrations (
                    source_id TEXT PRIMARY KEY,
                    start_date TEXT,
                    completion_date TEXT,
                    steps_data TEXT,
                    resources_used TEXT,
                    status TEXT
                )
            """)
            
    def get_completed_integrations(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM integrations WHERE status = 'completed'"
            )
            return [dict(row) for row in cursor.fetchall()]
