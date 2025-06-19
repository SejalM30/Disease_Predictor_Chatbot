import pandas as pd
import pickle
import os
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

os.makedirs("model", exist_ok=True)

# Load CSVs
train_df = pd.read_csv("data/training.csv")         # disease and symptoms
precautions_df = pd.read_csv("data/symptom_precaution.csv")  # disease and precautions columns
description_df = pd.read_csv("data/symptom_Description.csv")  # disease and description
severity_df = pd.read_csv("data/Symptom-severity.csv")       # symptom severity info (optional)

# For training, we'll use train_df
# Fill NaNs
train_df.fillna("", inplace=True)
precautions_df.fillna("", inplace=True)
description_df.fillna("", inplace=True)

# Extract all symptoms from training.csv symptom columns (usually columns: symptom_1, symptom_2,...)
# Get all symptom columns (exclude 'prognosis' or 'disease' column)
symptom_cols = [col for col in train_df.columns if col.lower().startswith("symptom")]

# Collect all unique symptoms from these columns
all_symptoms = sorted({sym.lower() for col in symptom_cols for sym in train_df[col].unique() if sym})

# Encode X (symptoms one-hot vector)
def encode_symptoms(row):
    present = set([str(row[col]).lower() for col in symptom_cols if str(row[col]).strip() != ''])
    return [1 if symptom in present else 0 for symptom in all_symptoms]

X = train_df.apply(encode_symptoms, axis=1, result_type='expand')
X.columns = all_symptoms

# Encode labels (diseases)
le = LabelEncoder()
y = le.fit_transform(train_df["Disease"])

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save model and encoders
with open("model/disease_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("model/symptom_encoder.pkl", "wb") as f:
    pickle.dump((all_symptoms, le), f)

# Prepare disease_info dictionary by merging precautions and description on disease/prognosis

# For precautions: Map disease to list of precautions (precaution_1, precaution_2, ...)
disease_precautions = {}
for _, row in precautions_df.iterrows():
    disease = row["Disease"].strip()
    precautions = [row[col] for col in precautions_df.columns if col != "Disease" and str(row[col]).strip() != ""]
    disease_precautions[disease] = precautions

# For description: map disease to description
disease_description = dict(zip(description_df["Disease"].str.strip(), description_df["Description"]))

# Combine into one dict
disease_info = {}
for disease in le.classes_:
    desc = disease_description.get(disease, "No description available.")
    precs = disease_precautions.get(disease, [])
    disease_info[disease] = {
        "description": desc,
        "precautions": precs
    }

# Save disease info JSON
with open("model/disease_info.json", "w") as f:
    json.dump(disease_info, f, indent=4)

print("✅ Training complete. Model, encoders, and disease info saved.")
