from chatbot_model import load_resources, predict_disease, get_disease_info

def main():
    print("=== Disease Predictor Chatbot ===")
    model, all_symptoms, le, disease_info = load_resources()

    print("Enter symptoms separated by commas (e.g. headache, fever, cough)")
    while True:
        user_input = input("\nEnter symptoms (or type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        symptoms = [sym.strip() for sym in user_input.split(",") if sym.strip()]
        if not symptoms:
            print("Please enter at least one symptom.")
            continue

        disease = predict_disease(symptoms, model, all_symptoms, le)
        info = get_disease_info(disease, disease_info)

        print(f"\nPredicted Disease: {disease}")
        print(f"Description: {info['description']}")
        if info['precautions']:
            print("Precautions:")
            for i, prec in enumerate(info['precautions'], 1):
                print(f"  {i}. {prec}")
        else:
            print("No precautions info available.")

if __name__ == "__main__":
    main()
