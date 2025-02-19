# -*- coding: utf-8 -*-
"""ML_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uhwngaZ3hP1JRkzxyM5V1ydvLSnkDVyZ
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score, roc_curve, auc

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('/content/alzheimers_disease_data (1).csv')
df.head()

df.shape

df.info()

df.describe()

df.isnull().sum()

df.duplicated().sum()

df.drop(['PatientID','DoctorInCharge'],axis=1,inplace=True)

plt.figure(figsize=(30,15))
sns.heatmap(df.corr(),annot=True)
# plt.savefig("plot0.png")
plt.show()

fig, axes = plt.subplots(nrows=11, ncols=3, figsize=(20, 55))
fig.subplots_adjust(hspace=0.5)

numerical_columns = ['Age', 'BMI', 'AlcoholConsumption', 'PhysicalActivity', 'DietQuality', 'SleepQuality',
                     'SystolicBP', 'DiastolicBP', 'CholesterolTotal', 'CholesterolLDL', 'CholesterolHDL',
                     'CholesterolTriglycerides', 'MMSE', 'FunctionalAssessment', 'ADL']

categorical_columns = ['Gender', 'Ethnicity', 'EducationLevel', 'Smoking', 'FamilyHistoryAlzheimers',
                       'CardiovascularDisease', 'Diabetes', 'Depression', 'HeadInjury', 'Hypertension',
                       'MemoryComplaints', 'BehavioralProblems', 'Confusion', 'Disorientation',
                       'PersonalityChanges', 'DifficultyCompletingTasks', 'Forgetfulness', 'Diagnosis']

for idx, col in enumerate(numerical_columns):
    sns.histplot(df[col], kde=True, bins=30, ax=axes[idx // 3, idx % 3])
    axes[idx // 3, idx % 3].set_title(f'Distribution of {col}')

for idx, col in enumerate(categorical_columns):
    sns.countplot(x=col, data=df, ax=axes[(len(numerical_columns) + idx) // 3, (len(numerical_columns) + idx) % 3])
    axes[(len(numerical_columns) + idx) // 3, (len(numerical_columns) + idx) % 3].set_title(f'Count of {col}')

plt.tight_layout()
# plt.savefig("plot1.png")
plt.show()

fig, axes = plt.subplots(nrows=5, ncols=3, figsize=(20, 30))
fig.subplots_adjust(hspace=0.5)

for idx, col in enumerate(numerical_columns):
    sns.boxplot(x=df[col], ax=axes[idx // 3, idx % 3])
    axes[idx // 3, idx % 3].set_title(f'Box Plot of {col}')

plt.tight_layout()
# plt.savefig("plot2.png")
plt.show()

plt.figure(figsize=(10, 6))

sns.histplot(data=df, x='Age', hue='Diagnosis', kde=True, multiple="stack")
plt.title('Age Distribution by Alzheimer\'s Diagnosis')
plt.xlabel('Age')
plt.ylabel('Count')
plt.legend(title='Diagnosis', labels=['No Alzheimer\'s', 'Alzheimer\'s'])
# plt.savefig("plot3.png")
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(x='Gender', hue='Diagnosis', data=df)
plt.title('Comparison of Gender and Alzheimer\'s Diagnosis')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.xticks(ticks=[0, 1], labels=['Male', 'Female'])
plt.legend(title='Diagnosis', labels=['No Alzheimer\'s', 'Alzheimer\'s'])
# plt.savefig("plot4.png")
plt.show()

fig, axes = plt.subplots(nrows=6, ncols=3, figsize=(20, 30))
fig.subplots_adjust(hspace=0.5)
lifestyle_factors = ['Smoking', 'AlcoholConsumption', 'PhysicalActivity', 'DietQuality', 'SleepQuality']
health_conditions = ['CardiovascularDisease', 'Diabetes', 'Depression', 'HeadInjury', 'Hypertension']
cholesterol_levels = ['CholesterolTotal', 'CholesterolLDL', 'CholesterolHDL', 'CholesterolTriglycerides']
other_factors = ['FamilyHistoryAlzheimers', 'EducationLevel', 'Ethnicity']
all_factors = lifestyle_factors + health_conditions + cholesterol_levels + other_factors

for idx, col in enumerate(all_factors):
    if col in cholesterol_levels or col in lifestyle_factors:
        sns.boxplot(x='Diagnosis', y=col, data=df, ax=axes[idx // 3, idx % 3])
        axes[idx // 3, idx % 3].set_title(f'{col} by Diagnosis')
    else:
        sns.countplot(x=col, hue='Diagnosis', data=df, ax=axes[idx // 3, idx % 3])
        axes[idx // 3, idx % 3].set_title(f'{col} by Diagnosis')

plt.tight_layout()
# plt.savefig("plot5.png")
plt.show()

bmi_categories = pd.cut(df['BMI'], bins=[0, 18.5, 24.9, 29.9, float('inf')],
                        labels=['Underweight', 'Normal weight', 'Overweight', 'Obesity'])

df['BMI_Category'] = bmi_categories

plt.figure(figsize=(10, 6))
sns.countplot(x='BMI_Category', hue='Diagnosis', data=df)
plt.title('BMI Category Distribution by Alzheimer\'s Diagnosis')
plt.xlabel('BMI Category')
plt.ylabel('Count')
plt.legend(title='Diagnosis', labels=['No Alzheimer\'s', 'Alzheimer\'s'])
# plt.savefig("plot6.png")
plt.show()

df = pd.get_dummies(df, columns=['BMI_Category'], drop_first=True)
X = df.drop('Diagnosis', axis=1)
y = df['Diagnosis']

def evaluate_model(model, X_test, y_test, y_pred_prob):
    classification_rep = classification_report(y_test, model.predict(X_test))
    conf_matrix = confusion_matrix(y_test, model.predict(X_test))
    roc_auc = roc_auc_score(y_test, y_pred_prob)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    return classification_rep, conf_matrix, roc_auc, accuracy

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'SVM': SVC(probability=True),
    'Random Forest': RandomForestClassifier(random_state=42)
}

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

results = pd.DataFrame(columns=['Model', 'Stage', 'Accuracy', 'ROC AUC'])

print("Before SMOTE")
for name, model in models.items():
    y_pred_prob = cross_val_predict(model, x_train_scaled, y_train, cv=5, method='predict_proba')[:, 1]
    model.fit(x_train_scaled, y_train)
    y_pred_prob_test = model.predict_proba(x_test_scaled)[:, 1]
    classification_rep, conf_matrix, roc_auc, accuracy = evaluate_model(model, x_test_scaled, y_test, y_pred_prob_test)
    new_row = pd.DataFrame({'Model': [name], 'Stage': ['Before SMOTE'], 'Accuracy': [accuracy], 'ROC AUC': [roc_auc]})
    results = pd.concat([results, new_row], ignore_index=True)
    print(f"\n{name}")
    print("Classification Report:\n", classification_rep)
    print("Confusion Matrix:\n", conf_matrix)
    print("ROC AUC Score:", roc_auc)
    print("Accuracy:", accuracy)

"""Using SMOTE on your train data and then test on your test data"""

smote = SMOTE(random_state=42)
x_train_resampled, y_train_resampled = smote.fit_resample(x_train_scaled, y_train)

print("After SMOTE on training data")
for name, model in models.items():
    y_pred_prob = cross_val_predict(model, x_train_resampled, y_train_resampled, cv=5, method='predict_proba')[:, 1]
    model.fit(x_train_resampled, y_train_resampled)
    y_pred_prob_test = model.predict_proba(x_test_scaled)[:, 1]
    classification_rep, conf_matrix, roc_auc, accuracy = evaluate_model(model, x_test_scaled, y_test, y_pred_prob_test)
    new_row = pd.DataFrame({'Model': [name], 'Stage': ['After SMOTE'], 'Accuracy': [accuracy], 'ROC AUC': [roc_auc]})
    results = pd.concat([results, new_row], ignore_index=True)
    print(f"\n{name}")
    print("Classification Report:\n", classification_rep)
    print("Confusion Matrix:\n", conf_matrix)
    print("ROC AUC Score:", roc_auc)
    print("Accuracy:", accuracy)

param_grids = {
    'Logistic Regression': {
        'C': [0.1, 1, 10, 100]
    },
    'SVM': {
        'C': [0.1, 1, 10, 100],
        'kernel': ['linear', 'rbf']
    },
    'Random Forest': {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30]
    }
}

print("\nAfter Hyperparameter Tuning (Original Data)")
for name, model in models.items():
    grid_search = GridSearchCV(model, param_grids[name], cv=5, scoring='roc_auc')
    grid_search.fit(x_train_scaled, y_train)
    best_model = grid_search.best_estimator_
    y_pred_prob_tuned = best_model.predict_proba(x_test_scaled)[:, 1]
    classification_rep, conf_matrix, roc_auc, accuracy = evaluate_model(best_model, x_test_scaled, y_test, y_pred_prob_tuned)
    new_row = pd.DataFrame({'Model': [name], 'Stage': ['After Tuning (Original)'], 'Accuracy': [accuracy], 'ROC AUC': [roc_auc]})
    results = pd.concat([results, new_row], ignore_index=True)
    print(f"\n{name} (Tuned - Original Data)")
    print("Best Parameters:", grid_search.best_params_)
    print("Classification Report:\n", classification_rep)
    print("Confusion Matrix:\n", conf_matrix)
    print("ROC AUC Score:", roc_auc)
    print("Accuracy:", accuracy)

print("\nAfter Hyperparameter Tuning (SMOTE Data)")
for name, model in models.items():
    grid_search = GridSearchCV(model, param_grids[name], cv=5, scoring='roc_auc')
    grid_search.fit(x_train_resampled, y_train_resampled)
    best_model = grid_search.best_estimator_
    y_pred_prob_tuned = best_model.predict_proba(x_test_scaled)[:, 1]
    classification_rep, conf_matrix, roc_auc, accuracy = evaluate_model(best_model, x_test_scaled, y_test, y_pred_prob_tuned)
    new_row = pd.DataFrame({'Model': [name], 'Stage': ['After Tuning (SMOTE)'], 'Accuracy': [accuracy], 'ROC AUC': [roc_auc]})
    results = pd.concat([results, new_row], ignore_index=True)
    print(f"\n{name} (Tuned - SMOTE Data)")
    print("Best Parameters:", grid_search.best_params_)
    print("Classification Report:\n", classification_rep)
    print("Confusion Matrix:\n", conf_matrix)
    print("ROC AUC Score:", roc_auc)
    print("Accuracy:", accuracy)

print(results)

plt.figure(figsize=(15, 10))
for name, model in models.items():
    model.fit(x_train_resampled, y_train_resampled)
    y_pred_prob = model.predict_proba(x_test_scaled)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.2f})')

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc="lower right")
# plt.savefig("plot7.png")
plt.show()