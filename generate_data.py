"""
Synthetic Clinical Dataset Generator for Heart Failure Prediction
Based on clinical cardiology profiles from UCI Heart Disease & Kaggle Heart Failure records:
- Framingham Heart Study & BMC Medical Informatics standards (Chicco & Jurman, 2020)
- 1,200 patient observations across 13 clinical biomarkers and demographics.
"""

import os
import random
import numpy as np
import pandas as pd

def generate_heart_failure_dataset(output_path="data/heart_failure.csv", n_samples=1200, random_seed=42):
    np.random.seed(random_seed)
    random.seed(random_seed)
    
    # 1. Demographics
    age = np.random.normal(loc=54.5, scale=10.2, size=n_samples).astype(int)
    age = np.clip(age, 29, 80)
    
    # Sex: ~68% male in clinical cardiology cohorts (1 = Male, 0 = Female)
    sex = np.random.choice([1, 0], size=n_samples, p=[0.68, 0.32])
    
    # 2. Chest Pain Type (0: TA - Typical Angina, 1: ATA - Atypical Angina, 2: NAP - Non-Anginal, 3: ASY - Asymptomatic)
    # Asymptomatic ischemia is most prevalent in severe coronary heart disease
    chest_pain = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.10, 0.20, 0.22, 0.48])
    
    # 3. Resting Blood Pressure (mm Hg)
    resting_bp = np.random.normal(loc=132.5, scale=18.5, size=n_samples).astype(int)
    resting_bp = np.clip(resting_bp, 90, 200)
    
    # 4. Serum Cholesterol (mg/dL)
    cholesterol = np.random.normal(loc=240.0, scale=48.0, size=n_samples).astype(int)
    cholesterol = np.clip(cholesterol, 120, 480)
    
    # 5. Fasting Blood Sugar > 120 mg/dL (1: Diabetic/Elevated, 0: Normal)
    fasting_bs = np.random.choice([0, 1], size=n_samples, p=[0.78, 0.22])
    
    # 6. Resting ECG (0: Normal, 1: ST-T wave abnormality, 2: LVH - Left Ventricular Hypertrophy)
    resting_ecg = np.random.choice([0, 1, 2], size=n_samples, p=[0.55, 0.22, 0.23])
    
    # 7. Maximum Heart Rate Achieved (bpm) - roughly inversely related to age
    base_max_hr = 220 - age
    noise_hr = np.random.normal(loc=-25, scale=18, size=n_samples)
    max_hr = (base_max_hr + noise_hr).astype(int)
    max_hr = np.clip(max_hr, 65, 202)
    
    # 8. Exercise Induced Angina (1: Yes, 0: No)
    # Probability increases with age and ASY chest pain
    angina_prob = 0.2 + 0.003 * (age - 30) + 0.25 * (chest_pain == 3)
    angina_prob = np.clip(angina_prob, 0.05, 0.85)
    exercise_angina = (np.random.rand(n_samples) < angina_prob).astype(int)
    
    # 9. Oldpeak (ST depression induced by exercise relative to rest in mm)
    oldpeak = np.random.exponential(scale=1.0, size=n_samples) + (exercise_angina * 0.8)
    oldpeak = np.round(np.clip(oldpeak, 0.0, 6.2), 1)
    
    # 10. ST Slope (0: Upsloping [benign], 1: Flat [moderate risk], 2: Downsloping [severe risk])
    slope_probs = []
    for op, ea in zip(oldpeak, exercise_angina):
        if op > 1.8 or ea == 1:
            slope_probs.append([0.15, 0.65, 0.20])
        else:
            slope_probs.append([0.65, 0.30, 0.05])
    st_slope = np.array([np.random.choice([0, 1, 2], p=p) for p in slope_probs])
    
    # 11. Ejection Fraction (%) - Percentage of blood leaving the heart (Normal: 50-70%, Reduced: <40%)
    ejection_fraction = np.random.normal(loc=44.0, scale=11.5, size=n_samples).astype(int)
    ejection_fraction = np.clip(ejection_fraction, 14, 75)
    
    # 12. Serum Creatinine (mg/dL) - Renal biomarker indicator
    serum_creatinine = np.random.lognormal(mean=0.15, sigma=0.45, size=n_samples)
    serum_creatinine = np.round(np.clip(serum_creatinine, 0.5, 9.4), 2)
    
    # 13. Target Calculation: Heart Disease / Heart Failure Occurrence (1 = Positive, 0 = Negative)
    # Logistic clinical risk scoring formula combining established risk markers
    logit = (
        -4.8 
        + 0.045 * (age - 50)
        + 0.85 * sex
        + 0.70 * (chest_pain == 3) # Asymptomatic ischemia
        + 0.015 * (resting_bp - 120)
        + 0.005 * (cholesterol - 200)
        + 0.65 * fasting_bs
        + 0.40 * (resting_ecg > 0)
        - 0.025 * (max_hr - 140)
        + 1.10 * exercise_angina
        + 0.65 * oldpeak
        + 0.90 * (st_slope == 1) + 1.45 * (st_slope == 2)
        - 0.065 * (ejection_fraction - 45) # Lower EF significantly elevates risk
        + 0.45 * (serum_creatinine - 1.0)
    )
    
    risk_prob = 1.0 / (1.0 + np.exp(-logit))
    # Add minor stochastic perturbation
    heart_disease = (np.random.rand(n_samples) < risk_prob).astype(int)
    
    # Build DataFrame
    df = pd.DataFrame({
        "Patient_ID": [f"PID_{i:05d}" for i in range(1, n_samples + 1)],
        "Age": age,
        "Sex": sex,
        "ChestPainType": chest_pain,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": fasting_bs,
        "RestingECG": resting_ecg,
        "MaxHR": max_hr,
        "ExerciseAngina": exercise_angina,
        "Oldpeak": oldpeak,
        "ST_Slope": st_slope,
        "EjectionFraction": ejection_fraction,
        "SerumCreatinine": serum_creatinine,
        "HeartDisease": heart_disease
    })
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully created at '{output_path}'")
    print(f"Total Cohort: {len(df)} patients | Positive Cases (Heart Failure): {df['HeartDisease'].sum()} ({df['HeartDisease'].mean()*100:.1f}%)")
    return df

if __name__ == "__main__":
    generate_heart_failure_dataset()
