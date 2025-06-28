# models.py

from pydantic import BaseModel
from typing import Optional

class EventRequest(BaseModel):
    summary: str
    start_time: str  # RFC3339 timestamp
    end_time: str    # RFC3339 timestamp
    description: Optional[str] = None
    location: Optional[str] = None
    