"""
Interactive Clinical Inference Tool for Heart Failure Prediction
Loads the persisted best model and standard scaler to predict heart failure probability
and risk tier for individual patient biomarkers.
"""

import os
import joblib
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def predict_patient_risk(patient_dict, models_dir=os.path.join(BASE_DIR, "models")):
    model_path = os.path.join(models_dir, "best_heart_failure_model.joblib")
    scaler_path = os.path.join(models_dir, "scaler.joblib")
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Trained model or scaler not found in '{models_dir}'. Please run train_models.py first.")
        
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    feature_order = [
        "Age", "Sex", "ChestPainType", "RestingBP", "Cholesterol", "FastingBS",
        "RestingECG", "MaxHR", "ExerciseAngina", "Oldpeak", "ST_Slope",
        "EjectionFraction", "SerumCreatinine"
    ]
    
    # Format input
    input_df = pd.DataFrame([patient_dict])[feature_order]
    input_scaled = scaler.transform(input_df)
    
    pred_class = model.predict(input_scaled)[0]
    pred_prob = model.predict_proba(input_scaled)[0][1] if hasattr(model, "predict_proba") else 0.5
    
    # Risk Stratification
    if pred_prob >= 0.75:
        risk_tier = "CRITICAL RISK (Immediate Clinical Consultation Required)"
        badge = "🔴"
    elif pred_prob >= 0.50:
        risk_tier = "HIGH RISK (Cardiology Referral & Diagnostic Stress Test)"
        badge = "🟠"
    elif pred_prob >= 0.25:
        risk_tier = "MODERATE RISK (Lifestyle Modification & Monitoring)"
        badge = "🟡"
    else:
        risk_tier = "LOW RISK (Healthy Baseline / Routine Annual Checkup)"
        badge = "🟢"
        
    print("\n" + "=" * 70)
    print("      CLINICAL HEART FAILURE RISK ASSESSMENT REPORT")
    print("=" * 70)
    print(f"Patient Assessment Result: {'POSITIVE (Heart Failure Detected)' if pred_class == 1 else 'NEGATIVE (Normal)'}")
    print(f"Estimated Probability:    {pred_prob * 100:.2f}%")
    print(f"Risk Stratification:      {badge} {risk_tier}")
    print("-" * 70)
    print("Patient Biomarker Summary:")
    print(f"  - Age / Gender:          {patient_dict['Age']} yrs | {'Male' if patient_dict['Sex'] == 1 else 'Female'}")
    print(f"  - Resting BP:            {patient_dict['RestingBP']} mmHg")
    print(f"  - Serum Cholesterol:     {patient_dict['Cholesterol']} mg/dL")
    print(f"  - Ejection Fraction:     {patient_dict['EjectionFraction']}%")
    print(f"  - Serum Creatinine:      {patient_dict['SerumCreatinine']} mg/dL")
    print(f"  - Exercise Angina:       {'Present' if patient_dict['ExerciseAngina'] == 1 else 'Absent'}")
    print(f"  - ST Depression (Oldpeak):{patient_dict['Oldpeak']} mm")
    print("=" * 70)
    
    return pred_class, pred_prob, risk_tier

if __name__ == "__main__":
    # Test with two contrasting clinical patient scenarios
    print("\n--- TEST CASE 1: High-Risk Patient (Elderly, Low Ejection Fraction, Exercise Angina) ---")
    patient_high_risk = {
        "Age": 68, "Sex": 1, "ChestPainType": 3, "RestingBP": 160, "Cholesterol": 285,
        "FastingBS": 1, "RestingECG": 2, "MaxHR": 105, "ExerciseAngina": 1,
        "Oldpeak": 2.8, "ST_Slope": 2, "EjectionFraction": 25, "SerumCreatinine": 2.4
    }
    predict_patient_risk(patient_high_risk)
    
    print("\n--- TEST CASE 2: Low-Risk Patient (Young, Healthy Ejection Fraction, High MaxHR) ---")
    patient_low_risk = {
        "Age": 38, "Sex": 0, "ChestPainType": 1, "RestingBP": 115, "Cholesterol": 180,
        "FastingBS": 0, "RestingECG": 0, "MaxHR": 172, "ExerciseAngina": 0,
        "Oldpeak": 0.0, "ST_Slope": 0, "EjectionFraction": 60, "SerumCreatinine": 0.8
    }
    predict_patient_risk(patient_low_risk)
