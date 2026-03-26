import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle
import os

class PricePredictor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.window_size = 5  # kaç geçmiş veriyle tahmin yapılacak

    def predict(self, prices: list[float]) -> dict:
        if len(prices) < self.window_size:
            return {"error": "Yeterli veri yok", "min_required": self.window_size}

        data = np.array(prices).reshape(-1, 1)
        scaled = self.scaler.fit_transform(data)

        # Basit ağırlıklı ortalama (LSTM olmadan, veri gelince LSTM'e geçilecek)
        weights = np.array([0.1, 0.15, 0.2, 0.25, 0.3])
        last_window = scaled[-self.window_size:].flatten()
        weighted_avg = float(np.dot(weights, last_window))

        predicted_scaled = np.array([[weighted_avg]])
        predicted_price = float(self.scaler.inverse_transform(predicted_scaled)[0][0])

        trend = "artış" if predicted_price > prices[-1] else "düşüş"
        change_pct = ((predicted_price - prices[-1]) / prices[-1]) * 100

        return {
            "predicted_price": round(predicted_price, 2),
            "trend": trend,
            "change_percent": round(change_pct, 2),
            "confidence": round(min(0.95, 0.6 + len(prices) * 0.01), 2)
        }


class AnomalyDetector:
    def __init__(self, contamination: float = 0.1):
        self.contamination = contamination  # beklenen anomali oranı

    def detect(self, transactions: list[float]) -> dict:
        if len(transactions) < 3:
            return {"anomalies": [], "message": "Yeterli veri yok"}

        data = np.array(transactions)
        mean = np.mean(data)
        std = np.std(data)
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        anomalies = []
        for i, val in enumerate(data):
            z_score = abs((val - mean) / std) if std > 0 else 0
            is_iqr_anomaly = val < lower or val > upper

            if z_score > 2 or is_iqr_anomaly:
                anomalies.append({
                    "index": i,
                    "value": round(float(val), 2),
                    "z_score": round(z_score, 2),
                    "severity": "yüksek" if z_score > 3 else "orta",
                    "direction": "yüksek" if val > upper else "düşük"
                })

        return {
            "total_transactions": len(data),
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "stats": {
                "mean": round(float(mean), 2),
                "std": round(float(std), 2),
                "lower_bound": round(float(lower), 2),
                "upper_bound": round(float(upper), 2),
            }
        }