from fastapi import APIRouter
from ..api.models import SignalRequest, SignalResponse

router = APIRouter()

@router.get('/health')
async def health():
    return {"ok": True}

@router.post('/predict', response_model=SignalResponse)
async def predict(req: SignalRequest):
    from ..core.predictor import Predictor
    pred = Predictor()
    sig = await pred.generate_signal(req.symbol, req.timeframe)
    return sig
