import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier

# 1. Connect to PostgreSQL Database
db_password = "manjyot"
engine = create_engine(f'postgresql+psycopg2://postgres:{db_password}@localhost:5432/credit_risk_db')
print("Fetching engineered features from PostgreSQL...")
df = pd.read_sql_query("SELECT * FROM vw_engineered_credit_features", engine)

# Handle potential infinite or null values
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(0, inplace=True)

# 2. Prepare Features & Target Variable
X = df.drop(columns=['client_id', 'default_next_month'])
y = df['default_next_month']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 3. Train XGBoost Classifier
imbalance_ratio = (y_train == 0).sum() / (y_train == 1).sum()

print("Training XGBoost Probability of Default (PD) model...")
model = XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=imbalance_ratio,
    random_state=42,
    eval_metric='auc'
)
model.fit(X_train, y_train)

# 4. Evaluate Model Performance
y_pred_proba = model.predict_proba(X_test)[:, 1]
auc_score = roc_auc_score(y_test, y_pred_proba)
print(f"Validation ROC-AUC Score: {auc_score:.4f}")

# 5. Score Portfolio & Calculate Expected Loss
print("Calculating Expected Loss and Risk Tiers...")
df['prob_default_pd'] = model.predict_proba(X)[:, 1]
df['exposure_at_default_ead'] = np.maximum(df['limit_bal'] * df['current_utilization_ratio'], 0)

LGD = 0.75
df['expected_loss_el'] = df['prob_default_pd'] * LGD * df['exposure_at_default_ead']

conditions = [
    (df['prob_default_pd'] < 0.20),
    (df['prob_default_pd'].between(0.20, 0.50)),
    (df['prob_default_pd'].between(0.50, 0.75)),
    (df['prob_default_pd'] > 0.75)
]
tiers = ['Tier 1: Low Risk', 'Tier 2: Moderate Watch', 'Tier 3: High Risk', 'Tier 4: Critical / Freeze']
df['risk_tier'] = np.select(conditions, tiers, default='Tier 2: Moderate Watch')

# 6. Export Scored Portfolio
df.to_csv('scored_credit_portfolio.csv', index=False)
print("Success! Scored portfolio exported to 'scored_credit_portfolio.csv'.")