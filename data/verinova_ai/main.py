from model import PricePredictor, AnomalyDetector
predictor = PricePredictor()
detector = AnomalyDetector()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import numpy as np
import random
import pandas as pd 
import io
from fastapi import File, UploadFile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Modeller ──────────────────────────────────────────

class PriceRequest(BaseModel):
    coin: str
    prices: List[float]  # geçmiş fiyatlar

class PortfolioRequest(BaseModel):
    portfolio: Dict[str, float]  # {"BTC": 0.5, "ETH": 2.0}

class AnomalyRequest(BaseModel):
    transactions: List[float]  # işlem tutarları

# ── Endpointler ───────────────────────────────────────

@app.get("/api/ai/health")
def health():
    return {"status": "AI servisi çalışıyor ✅"}


@app.post("/api/ai/prediction")
def predict_price(req: PriceRequest):
    result = predictor.predict(req.prices)
    result["coin"]=req.coin
    return result


@app.post("/api/ai/analysis")
def analyze_portfolio(req: PortfolioRequest):
    total = sum(req.portfolio.values())
    
    insights = []
    for coin, amount in req.portfolio.items():
        percentage = (amount / total) * 100 if total > 0 else 0
        if percentage > 60:
            insights.append(f"{coin} portföyün %{percentage:.0f}'ini oluşturuyor, çeşitlendirmeyi düşün.")
        elif percentage < 5:
            insights.append(f"{coin} pozisyonu çok küçük.")

    return {
        "total_value": total,
        "distribution": {k: round((v/total)*100, 1) for k, v in req.portfolio.items()},
        "insights": insights if insights else ["Portföy dengeli görünüyor."],
        "risk_level": "yüksek" if max(req.portfolio.values()) / total > 0.7 else "orta"
    }


@app.post("/api/ai/anomaly")
def detect_anomaly(req: AnomalyRequest):
    result = detector.detect(req.transactions)
    


@app.post("/api/ai/recommend")
def recommend(req: PortfolioRequest):
    recommendations = []
    total = sum(req.portfolio.values())

    for coin, amount in req.portfolio.items():
        pct = (amount / total) * 100 if total > 0 else 0
        if pct > 50:
            recommendations.append({
                "coin": coin,
                "action": "sat",
                "reason": f"Aşırı yoğunlaşma (%{pct:.0f}), riski azalt"
            })
        elif pct < 10:
            recommendations.append({
                "coin": coin,
                "action": "tut",
                "reason": "Küçük pozisyon, izlemeye devam"
            })
        else:
            recommendations.append({
                "coin": coin,
                "action": "tut",
                "reason": "Dengeli pozisyon"
            })

    return {"recommendations": recommendations}


@app.post("/api/ai/upload")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    
    # Sütunları ve özet istatistikleri döndür
    return {
        "columns": list(df.columns),
        "row_count": len(df),
        "preview": df.head(5).to_dict(orient="records"),
        "stats": df.describe().to_dict()
    }

@app.post("/api/ai/analyze-csv")
async def analyze_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    results = {}
    
    for col in numeric_cols:
        values = df[col].dropna().tolist()
        results[col] = predictor.predict(values[-30:] if len(values) > 30 else values)
    
    return {
        "analyzed_columns": numeric_cols,
        "predictions": results,
        "anomalies": {
            col: detector.detect(df[col].dropna().tolist())
            for col in numeric_cols
        }
    }

@app.post("/api/ai/upload")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    
    return {
        "columns": list(df.columns),
        "row_count": len(df),
        "numeric_columns": numeric_cols,
        "preview": df.head(3).to_dict(orient="records"),
    }