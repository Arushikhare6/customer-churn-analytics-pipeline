import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from preprocessing import preprocess_training_data

data = pd.read_excel(
    "data/Prediction_Data.xlsx",
    sheet_name="vw_ChurnData"
)

data, label_encoders = preprocess_training_data(data)

X = data.drop("Customer_Status", axis=1)
y = data["Customer_Status"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train, y_train)

predictions = rf_model.predict(X_test)

print(classification_report(
    y_test,
    predictions
))

joblib.dump(
    rf_model,
    "models/random_forest_model.pkl"
)

joblib.dump(
    label_encoders,
    "models/label_encoders.pkl"
)