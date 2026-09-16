# import os
# import joblib
# import pandas as pd


# # =========================================================
# # BASE DIRECTORY
# # =========================================================

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# # =========================================================
# # ML MODEL PATH
# # =========================================================

# MODEL_PATH = os.path.join(
#     BASE_DIR,
#     "maternal_risk_model.pkl"
# )


# # =========================================================
# # ENCODER PATH
# # =========================================================

# ENCODER_PATH = os.path.join(
#     BASE_DIR,
#     "maternal_risk_encoder.pkl"
# )


# # =========================================================
# # MATERNAL RISK PREDICTION
# # =========================================================

# def predict_maternal_risk(data):

#     try:

#         # Check model file
#         if not os.path.exists(MODEL_PATH):

#             return {
#                 "risk": "Model Not Found",
#                 "message": "maternal_risk_model.pkl file not found."
#             }

#         # Load trained model
#         model = joblib.load(MODEL_PATH)

#         # Convert input into DataFrame
#         if isinstance(data, dict):

#             df = pd.DataFrame([data])

#         else:

#             df = pd.DataFrame(data)

#         # Prediction
#         prediction = model.predict(df)

#         return {
#             "risk": str(prediction[0]),
#             "message": "Prediction completed successfully."
#         }

#     except Exception as e:

#         return {
#             "risk": "Error",
#             "message": str(e)
#         }


# # =========================================================
# # NUTRITION RECOMMENDATIONS
# # =========================================================

# def nutrition_recommendations(data=None):

#     recommendations = [

#         "Eat fresh fruits and vegetables regularly.",

#         "Include protein-rich foods such as eggs, pulses and nuts.",

#         "Drink sufficient water throughout the day.",

#         "Include iron-rich foods such as spinach and legumes.",

#         "Include calcium-rich foods such as milk and curd.",

#         "Eat whole grains and fiber-rich foods.",

#         "Avoid excessive processed and junk foods."

#     ]

#     return recommendations

import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'Dataset', 'maternal_risk_model.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'Dataset', 'risk_label_encoder.pkl')
FEATURES = ['age', 'systolicbp', 'diastolicbp', 'blood_sugar', 'bodytemp', 'heartrate']


def predict_maternal_risk(age, systolicbp, diastolicbp, blood_sugar, bodytemp, heartrate):
    try:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH):
            return {'label': 'Model Not Found', 'confidence': None, 'error': 'Upload/train the maternal dataset from the Administrator panel.'}
        model = joblib.load(MODEL_PATH)
        encoder = joblib.load(ENCODER_PATH)
        row = [[float(age), float(systolicbp), float(diastolicbp), float(blood_sugar), float(bodytemp), float(heartrate)]]
        pred = model.predict(row)[0]
        label = encoder.inverse_transform([int(pred)])[0]
        confidence = round(float(max(model.predict_proba(row)[0]) * 100), 2) if hasattr(model, 'predict_proba') else None
        return {'label': str(label).title(), 'confidence': confidence, 'error': None}
    except Exception as exc:
        return {'label': 'Prediction Error', 'confidence': None, 'error': str(exc)}


def nutrition_recommendations(query=''):
    try:
        from Administrator.models import tbl_Nutrition
        qs = tbl_Nutrition.objects.all()
        if query:
            qs = qs.filter(name__icontains=query) | qs.filter(category__icontains=query)
        items = list(qs[:12])
        if items:
            return items
    except Exception:
        pass
    return [
        'Eat fresh fruits and vegetables regularly.',
        'Include protein-rich foods such as eggs, pulses and nuts.',
        'Drink sufficient water throughout the day.',
        'Include iron-rich foods such as spinach and legumes.',
        'Include calcium-rich foods such as milk and curd.',
        'Eat whole grains and fiber-rich foods.',
        'Avoid excessive processed and junk foods.'
    ]
