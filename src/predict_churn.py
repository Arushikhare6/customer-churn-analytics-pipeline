import pandas as pd
import joblib
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Paths
DATA_FILE = BASE_DIR / "data" / "Prediction_Data.xlsx"
MODEL_FILE = BASE_DIR / "models" / "random_forest_model.pkl"
ENCODER_FILE = BASE_DIR / "models" / "label_encoders.pkl"
OUTPUT_FILE = BASE_DIR / "data" / "Predictions.csv"

# Load trained model and encoders
rf_model = joblib.load(MODEL_FILE)
label_encoders = joblib.load(ENCODER_FILE)

# Read prediction data
new_data = pd.read_excel(
    DATA_FILE,
    sheet_name="vw_JoinData"
)

# Keep original copy
original_data = new_data.copy()

# Drop unnecessary columns
new_data = new_data.drop(
    [
        "Customer_ID",
        "Customer_Status",
        "Churn_Category",
        "Churn_Reason"
    ],
    axis=1
)

# Encode categorical columns
for column in new_data.select_dtypes(include=["object"]).columns:
    new_data[column] = label_encoders[column].transform(
        new_data[column]
    )

# Predict
predictions = rf_model.predict(new_data)

# Add predictions
original_data["Customer_Status_Predicted"] = predictions

# Keep only predicted churners
predicted_churners = original_data[
    original_data["Customer_Status_Predicted"] == 1
]

# Save results
predicted_churners.to_csv(
    OUTPUT_FILE,
    index=False
)

print(f"Predicted churners: {len(predicted_churners)}")
print(f"Results saved to: {OUTPUT_FILE}")