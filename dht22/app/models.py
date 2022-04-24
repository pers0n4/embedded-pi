from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Record(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    humidity: float
    temperature: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
