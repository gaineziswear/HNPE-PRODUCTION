from pydantic import BaseModel
from typing import List

class SignalRequest(BaseModel):
    symbol: str
    timeframe: str

class SignalItem(BaseModel):
    symbol: str
    direction: str
    score: float
    confidence: float
    timeframe: str

class SignalResponse(BaseModel):
    signals: Listening [SignalItem]
    generated_at: str
