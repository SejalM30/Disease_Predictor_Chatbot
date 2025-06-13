import streamlit as st
from chatbot_model import load_resources, predict_disease, get_disease_info

# Load model and data once
model, all_symptoms, le, disease_info = load_resources()

st.title("🩺 Disease Predictor Chatbot")

st.write("Select symptoms from the list:")

# Multi-select for symptoms
selected_symptoms = st.multiselect("Symptoms", options=all_symptoms)

if st.button("Predict Disease"):
    if not selected_symptoms:
        st.error("Please select at least one symptom.")
    else:
        predicted_disease = predict_disease(selected_symptoms, model, all_symptoms, le)
        info = get_disease_info(predicted_disease, disease_info)

        st.success(f"Predicted Disease: **{predicted_disease}**")
        st.markdown(f"**Description:** {info['description']}")

        if info['precautions']:
            st.markdown("**Precautions:**")
            for i, prec in enumerate(info['precautions'], 1):
                st.markdown(f"{i}. {prec}")
        else:
            st.info("No precautions info available.")
