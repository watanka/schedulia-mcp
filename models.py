from pydantic import BaseModel
from datetime import datetime

class Time(BaseModel):
    start_time: datetime
    end_time: datetime

    def duration_minutes(self) -> int:
        return int((self.end_time - self.start_time).total_seconds() / 60)
