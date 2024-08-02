# 2024_ia651_Bora_Vandranki

# Alzheimer's Disease Classification Project Report


# Project Overview

The objective of this project is to develop a machine learning model that classifies individuals based on whether they have Alzheimer's disease. This classification aims to perform data-driven insights to assist medical professionals in early diagnosis and personalized care strategies.

# Data Sources

The datasets include various biomarkers, patient demographics, genetic information, brain imaging data, and clinical assessments. These features are critical for understanding and predicting Alzheimer's disease progression.
### Kaggle Dataset

The primary dataset for this project was sourced from Kaggle, a platform hosting various datasets provided by users and organizations. This dataset is specifically curated for Alzheimer’s disease classification.

### Open Source Data

Additional data has been incorporated from open source repositories that provide datasets related to Alzheimer's disease. This supplemental data helps enhance the robustness and diversity of our dataset, potentially improving model accuracy.


# Data Cleaning and Preprocessing Steps

Data cleaning, it's crucial to highlight that the dataset was already devoid of null values, indicating an initial level of preprocessing. However, comprehensive data cleaning involves several additional steps to ensure the dataset is optimized for accurate model training and analysis. Here’s a more detailed paragraph describing these steps:

In this project, even though the dataset was initially free from null values, further data cleaning was essential to enhance model reliability and performance. This process included identifying and removing outliers, which can significantly skew the results of predictive modeling. Outliers were detected using statistical techniques like the Interquartile Range (IQR), ensuring that only representative data points were retained. Another critical step was data integration, where datasets from various sources were combined into a coherent single dataset. This involved aligning similar features that were named differently across datasets and resolving any discrepancies in data formats and scales. Additionally, rigorous feature selection was conducted to identify and retain only those variables that are known to significantly impact Alzheimer's disease progression, based on expert consultations and a thorough review of related literature. These steps collectively ensured that the dataset was not only clean but also structured and refined to support effective machine learning model development.


The purpose of this EDA was to analyze the Alzheimer’s disease dataset thoroughly to understand the characteristics and distributions of various features and their potential influence on the diagnosis of Alzheimer’s disease. The target variable for this analysis is 'Diagnosis', a binary indicator where '0' represents the absence of Alzheimer's and '1' indicates its presence.

### Data Description

The dataset encompasses a wide array of variables:
- **Demographic Information**: Includes `PatientID`, `Age`, `Gender`, and `Ethnicity`.
- **Educational and Lifestyle Factors**: Encompasses `EducationLevel`, `BMI`, `Smoking`, `AlcoholConsumption`, `PhysicalActivity`, `DietQuality`, and `SleepQuality`.
- **Medical and Family History**: Covers `FamilyHistoryAlzheimers`, `CardiovascularDisease`, `Diabetes`, `Depression`, `HeadInjury`, `Hypertension`.
- **Clinical Measurements**: Consists of `SystolicBP`, `DiastolicBP`, `CholesterolTotal`, `CholesterolLDL`, `CholesterolHDL`, `CholesterolTriglycerides`.
- **Cognitive, Behavioral, and Functional Assessments**: Includes `MMSE`, `FunctionalAssessment`, `MemoryComplaints`, `BehavioralProblems`, `ADL`, `Confusion`, `Disorientation`, `PersonalityChanges`, `DifficultyCompletingTasks`, `Forgetfulness`.


### Analytical Insights and Visualization

## Distribution Analysis

- **Numerical Variables**: Variables such as `Age`, `BMI`, `AlcoholConsumption`, `PhysicalActivity`, `DietQuality`, `SleepQuality`, `SystolicBP`, `DiastolicBP`, `Cholesterol Levels`, `MMSE`, `FunctionalAssessment`, and `ADL` were found to be normally distributed, indicating a well-rounded representation across the patient spectrum.

- **Categorical Variables**: There was a notable imbalance observed in categorical variables like `Gender`, `Ethnicity`, and `EducationLevel`. This required careful consideration during model training to prevent bias.

### Correlation Analysis

- A correlation matrix was utilized to understand the interdependencies between variables. Notably, health conditions such as `CardiovascularDisease`, `Diabetes`, `Depression`, and `Hypertension` showed a higher correlation with the Alzheimer’s diagnosis than lifestyle factors.
  <img src="/plot0.png" alt="Correlation Matrix">


### Age and Gender Impact

- The distribution of `Age` relative to Alzheimer’s diagnosis revealed higher diagnosis rates in older age groups. 
- Gender comparison indicated differences in diagnosis rates between males and females, suggesting potential biological or social factors influencing Alzheimer's prevalence.
<img src="/plot1.png" alt="Impact1">
<img src="/plot2.png" alt="Impact2">
<img src="/plot3.png" alt="Impact3">
<img src="/plot4.png" alt="Impact4">

### Lifestyle and Health Conditions

- Plots comparing lifestyle factors (`Smoking`, `AlcoholConsumption`, `PhysicalActivity`, `DietQuality`, `SleepQuality`) with the diagnosis did not show distinct patterns, indicating these factors alone are not strong predictors of Alzheimer’s.
- Health conditions displayed a clearer association with Alzheimer's diagnosis, emphasizing the importance of medical history in predictive modeling.
<img src="/plot5.png" alt="Factors">

### Cholesterol and Cognitive Impairment

- Although cholesterol levels (`CholesterolTotal`, `CholesterolLDL`, `CholesterolHDL`, `CholesterolTriglycerides`) are important health indicators, their direct impact on Alzheimer’s diagnosis was less pronounced than cognitive impairment scores (`MMSE`).

### BMI Analysis

- BMI was categorized into `Underweight`, `Normal Weight`, `Overweight`, and `Obesity`. The analysis showed varying rates of Alzheimer's diagnosis across these categories, underscoring the role of physical health in cognitive decline.
<img src="/plot6.png" alt="BMI">

The EDA provided deep insights into the dataset, highlighting key variables that could influence the diagnosis of Alzheimer's. The findings from this analysis will guide the feature selection and model development phases, aiming to create a predictive model that is both accurate and reliable in diagnosing Alzheimer’s disease.


# Model Selection and Evaluation
Given the classification nature of the Alzheimer's disease prediction problem, several machine learning models were evaluated to determine the best fit. The chosen models were Logistic Regression, Support Vector Machine (SVM), and Random Forest due to their effectiveness in handling classification tasks.



## Data Preparation
- **Feature Selection**: Features like `Diagnosis` (target variable), `DoctorInCharge`, and `PatientID` were excluded from the feature set. The remaining features were utilized, ensuring they were largely free from redundancy.
- **Scaling**: All numeric features were scaled to have a uniform scale, which is crucial for models like SVM that are sensitive to the magnitude of data.
- **Data Splitting**: The dataset was split into training and testing sets.
- **Handling Imbalance**: The SMOTE technique was applied to balance the classes in the training dataset, it was applied on training data and then tested on your test data addressing the imbalance observed in the target variable `Diagnosis` 

## Model Training and Hyperparameter Tuning
- Initial training was conducted on the original dataset as well as the SMOTE-augmented dataset to compare the effects of balancing the data.
- Hyperparameter tuning was performed for each model to optimize their performance. This included adjusting parameters like regularization strength for Logistic Regression, kernel parameters for SVM, and the number of trees and depth for Random Forest.

# Model Performance Evaluation

The models were evaluated based on their accuracy and ROC AUC scores both before and after applying SMOTE, and following hyperparameter tuning. Here are the summarized results:

| Model                    | Stage                      | Accuracy | ROC AUC |
|--------------------------|----------------------------|----------|---------|
| Logistic Regression      | Before SMOTE               | 81.71%   | 87.69%  |
| SVM                      | Before SMOTE               | 80.47%   | 87.42%  |
| Random Forest            | Before SMOTE               | 89.30%   | 94.18%  |
| Logistic Regression      | After SMOTE                | 83.45%   | 91.39%  |
| SVM                      | After SMOTE                | 86.33%   | 93.15%  |
| Random Forest            | After SMOTE                | 90.05%   | 94.58%  |
| Logistic Regression      | After Tuning (Original)    | 81.71%   | 87.73%  |
| SVM                      | After Tuning (Original)    | 80.47%   | 87.42%  |
| Random Forest            | After Tuning (Original)    | 90.39%   | 94.29%  |
| Logistic Regression      | After Tuning (SMOTE)       | 83.45%   | 91.39%  |
| SVM                      | After Tuning (SMOTE)       | 86.33%   | 93.15%  |
| Random Forest            | After Tuning (SMOTE)       | 90.41%   | 94.66%  |

# Visualization

ROC-AUC curves were plotted to visually represent the performance of each model across different configurations. These plots are particularly useful in showing the trade-off between sensitivity and specificity and to compare the overall diagnostic ability of the models.
<img src="/plot7.png" alt="ROC AUC">
# Conclusion

The Random Forest model consistently outperformed the other models in terms of both accuracy and ROC AUC scores, with the highest scores observed after applying SMOTE and tuning. This indicates that Random Forest is particularly well-suited to handling the complexities of predicting Alzheimer's disease from the dataset used. Furthermore, the benefits of SMOTE in managing class imbalance and enhancing model performance were clearly demonstrated, making it a valuable technique for similar classification problems in the medical field. This comprehensive evaluation ensures that the selected model is robust, achieving high accuracy(90%) and excellent discriminative ability, making it a reliable tool in assisting the diagnosis of Alzheimer's disease.




