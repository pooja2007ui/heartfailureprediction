"""
Comprehensive Machine Learning Training Pipeline for Heart Failure Prediction
Compares:
1. Logistic Regression
2. Support Vector Classifier (SVC)
3. K-Nearest Neighbors (KNN)
4. Random Forest Classifier
5. Gradient Boosting Classifier (GBDT)
6. Multi-Layer Perceptron (MLP / Neural Network)
7. Soft Voting Ensemble Classifier

Performs:
- Stratified 80/20 Train-Test Split
- Standard Scaling of clinical biomarkers
- 5-Fold Stratified Cross Validation
- Comprehensive metric benchmarking (Accuracy, Precision, Recall, F1, ROC-AUC)
- Confusion Matrix computation
- Model persistence using joblib
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report, roc_curve, precision_recall_curve
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_ml_pipeline(
    data_path=os.path.join(BASE_DIR, "data", "heart_failure.csv"),
    models_dir=os.path.join(BASE_DIR, "models")
):
    os.makedirs(models_dir, exist_ok=True)
    print("=" * 80)
    print("HEART FAILURE PREDICTION: MACHINE LEARNING BENCHMARKING PIPELINE")
    print("=" * 80)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Run generate_data.py first.")
        
    df = pd.read_csv(data_path)
    print(f"Dataset successfully loaded: {df.shape[0]} patient samples across {df.shape[1]} columns.")
    
    # 1. Feature & Target Isolation
    feature_cols = [col for col in df.columns if col not in ["Patient_ID", "HeartDisease"]]
    X = df[feature_cols]
    y = df["HeartDisease"]
    
    print("\nClinical Features Used:")
    for i, col in enumerate(feature_cols, 1):
        print(f"  {i:2d}. {col:18s} (Type: {str(X[col].dtype):8s})")
        
    print(f"\nTarget Class Distribution:")
    pos_count = y.sum()
    neg_count = len(y) - pos_count
    print(f"  - Positive (Heart Failure): {pos_count} ({pos_count/len(y)*100:.2f}%)")
    print(f"  - Negative (No Failure):    {neg_count} ({neg_count/len(y)*100:.2f}%)")
    
    # 2. Stratified Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"\nDataset Partitioning:")
    print(f"  - Training Set: {X_train.shape[0]} samples")
    print(f"  - Testing Set:  {X_test.shape[0]} samples")
    
    # 3. Feature Normalization (StandardScaler)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, os.path.join(models_dir, "scaler.joblib"))
    print("StandardScaler fitted on training data and persisted.")
    
    # 4. Model Architectures
    base_svc = SVC(kernel="rbf", C=1.0, random_state=42)
    calibrated_svc = CalibratedClassifierCV(base_svc, ensemble=False)
    
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, C=1.0),
        "Support Vector Machine": calibrated_svc,
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=7, weights="distance"),
        "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=8, min_samples_split=4, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=120, learning_rate=0.08, max_depth=4, random_state=42),
        "Multi-Layer Perceptron": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=700, activation='relu', random_state=42)
    }
    
    # Add Soft Voting Ensemble (RF + GBDT + LR)
    voting_ensemble = VotingClassifier(
        estimators=[
            ('rf', models["Random Forest"]),
            ('gbdt', models["Gradient Boosting"]),
            ('lr', models["Logistic Regression"])
        ],
        voting='soft'
    )
    models["Voting Ensemble"] = voting_ensemble
    
    # 5. Training & Evaluation Loop
    results = []
    trained_models = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    print("\n" + "=" * 80)
    print(f"{'Model Name':<25} | {'Acc':<6} | {'Prec':<6} | {'Recall':<6} | {'F1':<6} | {'ROC-AUC':<8} | {'5-Fold CV Acc':<12}")
    print("-" * 80)
    
    best_f1 = -1
    best_model_name = ""
    
    for name, model in models.items():
        # Cross validation on scaled training data
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='accuracy')
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()
        
        # Fit model
        model.fit(X_train_scaled, y_train)
        trained_models[name] = model
        
        # Test predictions
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, "predict_proba") else None
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob) if y_prob is not None else 0.0
        
        results.append({
            "Model": name,
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1_Score": f1,
            "ROC_AUC": auc,
            "CV_Mean": cv_mean,
            "CV_Std": cv_std,
            "Confusion_Matrix": confusion_matrix(y_test, y_pred)
        })
        
        print(f"{name:<25} | {acc*100:5.2f}% | {prec*100:5.2f}% | {rec*100:5.2f}% | {f1*100:5.2f}% | {auc:8.4f} | {cv_mean*100:5.2f}% (±{cv_std*100:4.2f}%)")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            
    print("=" * 80)
    print(f"\n🏆 Best Performing Architecture: {best_model_name} (F1-Score: {best_f1*100:.2f}%)")
    
    # Save Best Model
    best_model = trained_models[best_model_name]
    joblib.dump(best_model, os.path.join(models_dir, "best_heart_failure_model.joblib"))
    print(f"Persisted best model ({best_model_name}) to '{os.path.join(models_dir, 'best_heart_failure_model.joblib')}'")
    
    # Save evaluation results summary dataframe
    df_results = pd.DataFrame(results).drop(columns=["Confusion_Matrix"])
    df_results.to_csv(os.path.join(models_dir, "model_comparison_metrics.csv"), index=False)
    
    # Save confusion matrices for chart generation
    cm_dict = {res["Model"]: res["Confusion_Matrix"].tolist() for res in results}
    joblib.dump(cm_dict, os.path.join(models_dir, "confusion_matrices.joblib"))
    
    return results, trained_models, feature_cols, X_test_scaled, y_test

if __name__ == "__main__":
    run_ml_pipeline()
