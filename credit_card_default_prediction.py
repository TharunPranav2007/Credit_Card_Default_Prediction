import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Create a Streamlit web app
st.title("Credit Card Default Prediction Dashboard")

# Add input fields for user input
st.sidebar.header("User Input Features")

# Input fields for each feature
limit_bal = st.sidebar.number_input("LIMIT_BAL (Amount of Credit in NT dollars)", min_value=0, value=50000)
sex = st.sidebar.radio("SEX (Gender)", ["Male", "Female"], index=0)
education = st.sidebar.selectbox("EDUCATION (Education Level)", 
                               ["Graduate School", "University", "High School", "Others"], 
                               index=1)
marriage = st.sidebar.selectbox("MARRIAGE (Marital Status)", 
                              ["Married", "Single", "Others"], 
                              index=1)
age = st.sidebar.number_input("AGE (Age in years)", min_value=18, max_value=100, value=30)

# Payment status inputs with description
st.sidebar.markdown("**Payment Status Codes:**")
st.sidebar.markdown("-2: No consumption<br>-1: Paid in full<br>0: Revolving credit<br>1+: Months delayed", unsafe_allow_html=True)

pay_status_sept = st.sidebar.number_input("PAY_0 (Repayment status in September)", min_value=-2, max_value=8, value=0)
pay_status_aug = st.sidebar.number_input("PAY_2 (Repayment status in August)", min_value=-2, max_value=8, value=0)
pay_status_jul = st.sidebar.number_input("PAY_3 (Repayment status in July)", min_value=-2, max_value=8, value=0)
pay_status_jun = st.sidebar.number_input("PAY_4 (Repayment status in June)", min_value=-2, max_value=8, value=0)
pay_status_may = st.sidebar.number_input("PAY_5 (Repayment status in May)", min_value=-2, max_value=8, value=0)
pay_status_apr = st.sidebar.number_input("PAY_6 (Repayment status in April)", min_value=-2, max_value=8, value=0)

# Bill amounts
st.sidebar.header("Bill Amounts (NT dollar)")
bill_amt_sept = st.sidebar.number_input("BILL_AMT1 (September)", min_value=0.0, value=5000.0)
bill_amt_aug = st.sidebar.number_input("BILL_AMT2 (August)", min_value=0.0, value=5000.0)
bill_amt_jul = st.sidebar.number_input("BILL_AMT3 (July)", min_value=0.0, value=5000.0)
bill_amt_jun = st.sidebar.number_input("BILL_AMT4 (June)", min_value=0.0, value=5000.0)
bill_amt_may = st.sidebar.number_input("BILL_AMT5 (May)", min_value=0.0, value=5000.0)
bill_amt_apr = st.sidebar.number_input("BILL_AMT6 (April)", min_value=0.0, value=5000.0)

# Payment amounts
st.sidebar.header("Payment Amounts (NT dollar)")
pay_amt_sept = st.sidebar.number_input("PAY_AMT1 (September)", min_value=0.0, value=500.0)
pay_amt_aug = st.sidebar.number_input("PAY_AMT2 (August)", min_value=0.0, value=500.0)
pay_amt_jul = st.sidebar.number_input("PAY_AMT3 (July)", min_value=0.0, value=500.0)
pay_amt_jun = st.sidebar.number_input("PAY_AMT4 (June)", min_value=0.0, value=500.0)
pay_amt_may = st.sidebar.number_input("PAY_AMT5 (May)", min_value=0.0, value=500.0)
pay_amt_apr = st.sidebar.number_input("PAY_AMT6 (April)", min_value=0.0, value=500.0)

# Convert education and marriage to numerical values
education_mapping = {
    "Graduate School": 1,
    "University": 2,
    "High School": 3,
    "Others": 4
}

marriage_mapping = {
    "Married": 1,
    "Single": 2,
    "Others": 3
}

# Prepare input data
input_data = {
    'LIMIT_BAL': float(limit_bal),
    'SEX': 1 if sex == "Male" else 2,
    'EDUCATION': education_mapping[education],
    'MARRIAGE': marriage_mapping[marriage],
    'AGE': int(age),
    'PAY_0': int(pay_status_sept),
    'PAY_2': int(pay_status_aug),
    'PAY_3': int(pay_status_jul),
    'PAY_4': int(pay_status_jun),
    'PAY_5': int(pay_status_may),
    'PAY_6': int(pay_status_apr),
    'BILL_AMT1': float(bill_amt_sept),
    'BILL_AMT2': float(bill_amt_aug),
    'BILL_AMT3': float(bill_amt_jul),
    'BILL_AMT4': float(bill_amt_jun),
    'BILL_AMT5': float(bill_amt_may),
    'BILL_AMT6': float(bill_amt_apr),
    'PAY_AMT1': float(pay_amt_sept),
    'PAY_AMT2': float(pay_amt_aug),
    'PAY_AMT3': float(pay_amt_jul),
    'PAY_AMT4': float(pay_amt_jun),
    'PAY_AMT5': float(pay_amt_may),
    'PAY_AMT6': float(pay_amt_apr),
    'entry_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Define comprehensive prediction logic
def predict_default(input_data):
    risk_score = 0
    
    # 1. Payment Delays Analysis
    payment_status = [input_data[f'PAY_{i}'] for i in [0, 2, 3, 4, 5, 6]]  # Note: PAY_1 is missing in your original data
    severe_delays = sum(1 for status in payment_status if status >= 2)
    if severe_delays >= 2:
        risk_score += 3
    
    # 2. Recent Default Status
    if input_data['PAY_0'] >= 1:
        risk_score += 2
    
    # 3. Credit Utilization
    bill_amounts = [input_data[f'BILL_AMT{i}'] for i in range(1, 7)]
    utilizations = [amt/input_data['LIMIT_BAL'] for amt in bill_amounts if input_data['LIMIT_BAL'] > 0]
    if len(utilizations) >= 3 and utilizations[-1] > 0.8:  # Over 80% utilization
        risk_score += 1
    
    # 4. Payment Amount vs Bill Amount
    pay_amounts = [input_data[f'PAY_AMT{i}'] for i in range(1, 7)]
    payment_ratios = []
    for pay, bill in zip(pay_amounts, bill_amounts):
        if bill > 0:
            payment_ratios.append(pay/bill)
    
    if len(payment_ratios) >= 3 and payment_ratios[-1] < 0.5 and payment_ratios[-1] < payment_ratios[-2]:
        risk_score += 1
    
    # 5. Only Minimum Payments
    if len(payment_ratios) >= 3 and all(0.02 <= ratio <= 0.05 for ratio in payment_ratios[-3:]):
        risk_score += 2
    
    # 6. Demographic Risk Factors
    demographic_risk = 0
    if input_data['AGE'] < 30:
        demographic_risk += 1
    if input_data['EDUCATION'] in [3, 4]:  # High school or other
        demographic_risk += 1
    if input_data['MARRIAGE'] == 2:  # Single
        demographic_risk += 1
    if demographic_risk >= 2:
        risk_score += 0.5
    
    # 7. Balance Accumulation
    if len(bill_amounts) >= 4 and bill_amounts[-4] > 0:
        growth_rate = (bill_amounts[-1] - bill_amounts[-4]) / bill_amounts[-4]
        if growth_rate > 0.3:  # 30%+ increase
            risk_score += 1
    
    return 1 if risk_score >= 4 else 0  # 1 = default, 0 = no default

# Make prediction
prediction = predict_default(input_data)
input_data['default.payment.next.month'] = prediction

# Display results with better visualization
st.header("Prediction Results")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Risk Assessment")
    if prediction == 1:
        st.error("High Default Risk (1: default)")
    else:
        st.success("Low Default Risk (0: no default)")

with col2:
    st.subheader("Recommendation")
    if prediction == 1:
        st.warning("Consider credit limit reduction or additional monitoring")
    else:
        st.info("Customer appears low risk")

# Show detailed analysis
st.markdown("---")
st.subheader("Detailed Analysis")

# Payment behavior analysis
st.write("**Payment Behavior:**")
payment_status_desc = {
    -2: "No consumption",
    -1: "Paid in full",
    0: "Revolving credit",
    1: "1 month delay",
    2: "2 months delay",
    # ... up to 8
}
for i, month in enumerate(["September", "August", "July", "June", "May", "April"]):
    status = input_data[f'PAY_{[0,2,3,4,5,6][i]}']  # Handle the PAY_1 missing case
    st.write(f"{month}: {payment_status_desc.get(status, f'{status} months delay')}")

# Credit utilization
current_utilization = (input_data['BILL_AMT1'] / input_data['LIMIT_BAL']) if input_data['LIMIT_BAL'] > 0 else 0
st.write(f"\n**Credit Utilization:** {current_utilization:.1%}")
if current_utilization > 0.8:
    st.warning("High utilization (over 80%) may indicate risk")

# Payment ratio
current_payment_ratio = (input_data['PAY_AMT1'] / input_data['BILL_AMT1']) if input_data['BILL_AMT1'] > 0 else 0
st.write(f"**Payment Ratio (Payment/Bill):** {current_payment_ratio:.1%}")
if current_payment_ratio < 0.5:
    st.warning("Low payment ratio (under 50%) may indicate risk")

# Demographic factors
st.write("\n**Demographic Factors:**")
st.write(f"Age: {input_data['AGE']} ({'Young' if input_data['AGE'] < 30 else 'Middle-aged' if input_data['AGE'] < 50 else 'Senior'})")
st.write(f"Education: {education}")
st.write(f"Marital Status: {marriage}")

# Save data to CSV
def save_to_csv(data):
    # Create dataframe from the input data
    df = pd.DataFrame([data])
    
    # Reorder columns to match standard format
    columns_order = [
        'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
        'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
        'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
        'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6',
        'default.payment.next.month', 'entry_timestamp'
    ]
    df = df[columns_order]
    
    # Check if file exists
    file_path = 'credit_card_predictions.csv'
    if os.path.exists(file_path):
        # Append to existing file
        existing_df = pd.read_csv(file_path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv(file_path, index=False)
    else:
        # Create new file
        df.to_csv(file_path, index=False)
    
    return file_path

# Add save button
if st.button("Save Prediction"):
    file_path = save_to_csv(input_data)
    st.success(f"Prediction saved to {file_path}")
    st.balloons()
