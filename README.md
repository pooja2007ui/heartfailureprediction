# 🫀 Heart Failure Prediction Using Machine Learning

An end-to-end clinical Machine Learning system and predictive healthcare analytics pipeline built with **Python**, **Scikit-Learn**, **Pandas**, and **Matplotlib**.

---

## 🏛️ Academic & Institutional Details
- **Student Name:** **Poojitha Talari**
- **Roll Number:** **24691A32I6**
- **Degree & Branch:** B.Tech in Computer Science & Engineering - Data Science
- **Course:** **23CSD107 – Machine Learning**
- **Institution:** Madanapalle Institute of Technology & Science (MITS / UGC - Autonomous), affiliated to JNTUA
- **Internal Guide:** **Mrs.Anuradha Prudhivi**, Assistant Professor, Dept. of CSE - Data Science

---

## 🔬 System Overview
This project applies supervised Machine Learning algorithms to stratify patient risk for **Congestive Heart Failure (CHF)** and **Cardiovascular Events** based on 13 clinical biomarkers (Age, Sex, Chest Pain Type, Resting BP, Serum Cholesterol, Fasting Blood Sugar, Resting ECG, Max Heart Rate, Exercise Angina, ST Depression [Oldpeak], ST Slope, Ejection Fraction, and Serum Creatinine).

### 🤖 Evaluated Machine Learning Classifiers:
1. **Logistic Regression** (L2 Regularized Baseline)
2. **Support Vector Machine (SVM)** (RBF Kernel with Probability Calibration)
3. **K-Nearest Neighbors (KNN)** (Distance-Weighted)
4. **Random Forest Classifier** (150 Estimators, Gini Impurity)
5. **Gradient Boosting Classifier (GBDT)** (120 Estimators, Learning Rate 0.08)
6. **Multi-Layer Perceptron (ANN)** (2 Hidden Layers: 64 $\times$ 32 Neurons)
7. **Soft Voting Ensemble** (Weighted Average of RF, GBDT, and Logistic Regression)

---

## 📁 Project Directory Structure

```
heart_failure_prediction_ml/
├── data/
│   └── heart_failure.csv               # 1,200 patient records across 13 clinical biomarkers
├── images/
│   ├── Figure_1_correlation_and_demographics.png    # Clinical correlation heatmap & age cohorts
│   ├── Figure_2_model_performance_comparison.png    # Benchmark of Accuracy, F1, Recall, AUC
│   ├── Figure_3_roc_curves.png                      # Multi-model ROC & AUC comparison
│   ├── Figure_4_feature_importance.png              # Biomarker risk ranking
│   └── Figure_5_confusion_matrices.png              # Confusion matrix diagnostics
├── models/
│   ├── best_heart_failure_model.joblib # Persisted champion classifier
│   ├── scaler.joblib                   # Persisted StandardScaler
│   └── model_comparison_metrics.csv    # Benchmark metric table
├── generate_data.py                    # Synthetic cardiology cohort generator
├── train_models.py                     # Training, 5-fold CV, and benchmarking script
├── generate_report_charts.py           # 300-DPI academic figure rendering script
├── predict.py                          # Interactive patient risk diagnostic tool
├── heart_failure_prediction.ipynb      # Interactive Jupyter Notebook
├── HEART_FAILURE_PROJECT_REPORT.md     # 15-Chapter institutional project report
└── README.md                           # Documentation and setup guide
```

---

## 🚀 How to Run the Project

### 1. Requirements Installation
Ensure Python (3.10+) is installed:
```bash
python -m pip install scikit-learn pandas numpy matplotlib joblib
```

### 2. Generate / Refresh Patient Dataset
```bash
python generate_data.py
```

### 3. Train Models & Benchmark Classifiers
```bash
python train_models.py
```

### 4. Render High-Resolution 300-DPI Academic Figures
```bash
python generate_report_charts.py
```

### 5. Run Clinical Diagnostic Risk Assessment on a Patient
```bash
python predict.py
```

### 6. Interactive Exploration in Jupyter Notebook
```bash
jupyter lab heart_failure_prediction.ipynb
```

---

## 📊 Key Experimental Results Summary

| Model Architecture | Accuracy | Precision | Recall (Sensitivity) | F1-Score | ROC-AUC | 5-Fold CV Accuracy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | **82.08%** | **78.08%** | **67.86%** | **72.61%** | **0.8728** | **78.02% (±3.40%)** |
| **Gradient Boosting** | 81.25% | 76.00% | 67.86% | 71.70% | 0.8478 | 75.31% (±2.20%) |
| **Voting Ensemble** | 80.42% | 74.67% | 66.67% | 70.44% | 0.8678 | 78.12% (±2.03%) |
| **Support Vector Machine** | 79.17% | 76.56% | 58.33% | 66.22% | 0.8603 | 75.73% (±2.85%) |
| **Random Forest** | 78.75% | 75.38% | 58.33% | 65.77% | 0.8479 | 77.60% (±1.86%) |
| **K-Nearest Neighbors** | 74.17% | 64.86% | 57.14% | 60.76% | 0.8173 | 74.79% (±2.48%) |
| **Multi-Layer Perceptron** | 72.50% | 61.84% | 55.95% | 58.75% | 0.7719 | 71.04% (±1.82%) |

### 🩺 Dominant Clinical Predictors:
1. **ST Depression (Oldpeak)** (14.2% Gini Importance)
2. **ST Slope** (13.1% Gini Importance)
3. **Exercise-Induced Angina** (12.4% Gini Importance)
4. **Chest Pain Type (Asymptomatic Ischemia)** (11.0% Gini Importance)
5. **Ejection Fraction & Max Heart Rate** (9.3% Gini Importance)
