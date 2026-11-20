import numpy as np
from sklearn.linear_model import LinearRegression

def predict_price(current_price):
    """
    Demo prediction model trained on a small synthetic downward price trend.
    Replace with real historical daily prices for meaningful predictions.
    """
    days = np.array([0, 7, 14, 21, 28, 35, 42, 49]).reshape(-1, 1)
    prices = np.array([1.00, .99, .965, .97, .94, .93, .915, .91]) * float(current_price)
    model = LinearRegression()
    model.fit(days, prices)
    predicted = float(model.predict(np.array([[14]]))[0])
    predicted = max(predicted, current_price * 0.70)
    change = ((predicted - current_price) / current_price) * 100 if current_price else 0
    return {
        "current": round(float(current_price), 2),
        "predicted_14_days": round(predicted, 2),
        "change_percent": round(change, 2),
        "note": "Educational demo estimate trained on synthetic sample trend; not a guaranteed forecast."
    }
