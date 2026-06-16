import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_training_data(data):
    data = data.drop(
        ['Customer_ID', 'Churn_Category', 'Churn_Reason'],
        axis=1
    )

    columns_to_encode = [
        'Gender', 'Married', 'State', 'Value_Deal',
        'Phone_Service', 'Multiple_Lines',
        'Internet_Service', 'Internet_Type',
        'Online_Security', 'Online_Backup',
        'Device_Protection_Plan', 'Premium_Support',
        'Streaming_TV', 'Streaming_Movies',
        'Streaming_Music', 'Unlimited_Data',
        'Contract', 'Paperless_Billing',
        'Payment_Method'
    ]

    label_encoders = {}

    for col in columns_to_encode:
        encoder = LabelEncoder()
        data[col] = encoder.fit_transform(data[col])
        label_encoders[col] = encoder

    data['Customer_Status'] = data[
        'Customer_Status'
    ].map({
        'Stayed': 0,
        'Churned': 1
    })

    return data, label_encoders