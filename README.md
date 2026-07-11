# Student Performance Prediction System

A machine learning project that predicts a student's academic performance using
attendance, assignment scores, internal assessments, and other academic/lifestyle
indicators. Built as part of an ML internship project.

---

## Objective

To predict student academic performance using attendance, assignment scores,
internal assessments, and other academic indicators — using a **regression model**
that can be deployed as an interactive web app.

---

##  Machine Learning Concepts Covered

- **Data Cleaning** — handling missing values, duplicates, outliers, and inconsistent formats
- **Feature Engineering** — encoding categorical variables, building a composite performance index
- **Regression Models** — Linear Regression used to predict a continuous performance score
- **Model Evaluation** — R² Score, MAE, MSE, RMSE, and Actual vs Predicted visualization

---

##  Project Structure

```
student_performance_project/
│
├── data/
│   └── student_performance_dataset.csv     # Raw dataset
│
├── notebooks/
│   └── MNIT_project.ipynb                 # Full workflow: cleaning, EDA, training, evaluation
│
├── app.py                                  # Streamlit web app for live predictions
└── README.md                               # Project documentation (this file) 
└──Documentation                    # Documentation about the project                     


```

---

## Dataset Description

| Column | Type | Description |
|---|---|---|
| `student_id` | Text | Unique student identifier |
| `attendance_percentage` | Numeric | Attendance percentage (0–100) |
| `assignment_score` | Numeric | Average assignment score (0–100) |
| `internal_assessment_score` | Numeric | Internal exam score (0–100) |
| `study_hours_per_week` | Numeric | Self-reported weekly study hours |
| `previous_semester_gpa` | Numeric | GPA from the previous semester (0–10) |
| `sleep_hours` | Numeric | Average daily sleep hours |
| `extracurricular_participation` | Binary (0/1) | Participates in extracurricular activities |
| `part_time_job` | Binary (0/1) | Has a part-time job |
| `parental_education_level` | Categorical | High School / Undergraduate / Postgraduate |
| `family_income_level` | Categorical | Low / Medium / High |
| `performance_index` | Numeric (Target) | Composite score representing overall academic performance (0–100) |
| `academic_performance` | Categorical | Poor / Average / Good / Excellent (derived label) |

> **Note:** `final_exam_score` and `academic_performance` are excluded from model
> training to avoid data leakage, since they are derived from or closely tied to the target variable.

---

## Data Cleaning Steps

1. Removed inconsistent formatting (e.g. `"85%"` strings in attendance converted to numeric)
2. Filled missing values using column median (numeric) / mode (categorical)
3. Removed impossible values (e.g. attendance > 100, negative scores)
4. Detected and removed outliers using **Z-score method** (|z| > 3)
5. Removed duplicate rows

---

## Exploratory Data Analysis (EDA)

- **Univariate Analysis** — distribution of each feature (histograms, `.describe()`)
- **Bivariate Analysis** — relationship between each feature and `performance_index` (scatter plots, box plots)
- **Correlation Analysis** — heatmap to identify which features most strongly influence performance, and to check for multicollinearity between features

---

##  Feature Engineering

- Binary encoding applied to `extracurricular_participation` and `part_time_job`
- `performance_index` engineered as a weighted composite of attendance, assignment
  scores, internal assessment, study hours, GPA, sleep, extracurricular participation,
  and part-time job status

---

## Model

**Algorithm used:** Linear Regression

**Why Linear Regression:**
- The relationship between the input indicators and performance is largely linear/additive
- Highly interpretable — coefficients directly show each feature's impact
- Dataset size (600 rows) is small, so a simple model avoids overfitting

**Training process:**
```python
model = LinearRegression()
model.fit(x_train, y_train)
```

---

## Model Evaluation

| Metric | Description |
|---|---|
| **R² Score** | Proportion of variance in performance explained by the model |
| **MAE** | Average absolute prediction error |
| **MSE** | Average squared prediction error (penalizes large errors more) |
| **RMSE** | Square root of MSE, in the same units as the target |

Results are visualized using an **Actual vs Predicted scatter plot**, where points
closer to the diagonal reference line indicate more accurate predictions.

---

##  How to Run This Project

### 1. Clone / download this project folder

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Retrain the model
```bash
python train_model.py
```
This regenerates `model.pkl`, `feature_columns.pkl`, and `feature_ranges.pkl`.

### 4. Run the Streamlit app
```bash
streamlit run app.py
```
This opens a browser window where you can input a student's attendance, scores,
and other indicators to get a live performance prediction.

---


## Ayush pal

Internship Project — Student Performance Prediction System
