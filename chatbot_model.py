import pickle
import json
import pandas as pd


def load_resources():
    with open("model/disease_model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("model/symptom_encoder.pkl", "rb") as f:
        all_symptoms, label_encoder = pickle.load(f)

    with open("model/disease_info.json", "r") as f:
        disease_info = json.load(f)

    return model, all_symptoms, label_encoder, disease_info


def predict_disease(selected_symptoms, model, all_symptoms, label_encoder):
    selected_symptoms = set(sym.lower() for sym in selected_symptoms)

    input_vector = [1 if symptom in selected_symptoms else 0 for symptom in all_symptoms]
    input_df = pd.DataFrame([input_vector], columns=all_symptoms)

    pred_encoded = model.predict(input_df)[0]
    predicted_disease = label_encoder.inverse_transform([pred_encoded])[0]

    return predicted_disease


def get_disease_info(disease_name, disease_info):
    return disease_info.get(disease_name, {
        "description": "No description available.",
        "precautions": []
    })
