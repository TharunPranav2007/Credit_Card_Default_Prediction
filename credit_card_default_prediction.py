import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Set page config
st.set_page_config(
    page_title="Credit Card Default Prediction",
    layout="wide"
)

# Main title and team members
st.markdown("<h1 style='text-align: center; color: #4b0082;'>CASTLE CRYSTALS</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color:  #4b0082;'>CREDIT CARD DEFAULT PREDICTION</h2>",unsafe_allow_html=True)
st.markdown("### Team Members:")
st.markdown("""
1. **THARUN PRANAV T**\t          ✉tharunpranavt2606@gmail.com  
2. **SARAN S**\t                               ✉saransam8840@gmail.com  
3. **THINAKAR V**\t                        ✉thinakar2410@gmail.com
4. **SRIRAM PRASATH V S**\t      ✉sriram10721s@gmail.com
""")

st.markdown("---")

# Add input fields for user input
st.sidebar.header("User Input Features")

# Input fields for each feature
limit_bal = st.sidebar.number_input("LIMIT_BAL", min_value=0, value=500000)
sex = st.sidebar.radio("SEX", ["Male", "Female"], index=0)
education = st.sidebar.selectbox("EDUCATION", 
                               ["Graduate School", "University", "High School", "Others"], 
                               index=1)
marriage = st.sidebar.selectbox("MARRIAGE", 
                              ["Married", "Single", "Others"], 
                              index=1)
age = st.sidebar.number_input("AGE (years)", min_value=18, max_value=100, value=30)

# Payment status inputs with description
st.sidebar.markdown("**Payment Status Codes:**")
st.sidebar.markdown("-2: No consumption<br>-1: Paid in full<br>0: Revolving credit<br>+1: Months delayed", unsafe_allow_html=True)

st.sidebar.header("Repayment Status")
pay_status1 = st.sidebar.number_input("PAY_1", min_value=-2, max_value=8, value=0)
pay_status2 = st.sidebar.number_input("PAY_2", min_value=-2, max_value=8, value=0)
pay_status3 = st.sidebar.number_input("PAY_3", min_value=-2, max_value=8, value=0)
pay_status4 = st.sidebar.number_input("PAY_4", min_value=-2, max_value=8, value=0)
pay_status5 = st.sidebar.number_input("PAY_5", min_value=-2, max_value=8, value=0)
pay_status6 = st.sidebar.number_input("PAY_6", min_value=-2, max_value=8, value=0)

# Bill amounts
st.sidebar.header("Bill Amounts")
bill_amt1 = st.sidebar.number_input("BILL_AMT1", min_value=0.0, value=5000.0)
bill_amt2 = st.sidebar.number_input("BILL_AMT2", min_value=0.0, value=5000.0)
bill_amt3 = st.sidebar.number_input("BILL_AMT3", min_value=0.0, value=5000.0)
bill_amt4 = st.sidebar.number_input("BILL_AMT4", min_value=0.0, value=5000.0)
bill_amt5 = st.sidebar.number_input("BILL_AMT5", min_value=0.0, value=5000.0)
bill_amt6 = st.sidebar.number_input("BILL_AMT6", min_value=0.0, value=5000.0)

# Payment amounts
st.sidebar.header("Payment Amounts")
pay_amt1 = st.sidebar.number_input("PAY_AMT1", min_value=0.0, value=500.0)
pay_amt2 = st.sidebar.number_input("PAY_AMT2", min_value=0.0, value=500.0)
pay_amt3 = st.sidebar.number_input("PAY_AMT3", min_value=0.0, value=500.0)
pay_amt4 = st.sidebar.number_input("PAY_AMT4", min_value=0.0, value=500.0)
pay_amt5 = st.sidebar.number_input("PAY_AMT5", min_value=0.0, value=500.0)
pay_amt6 = st.sidebar.number_input("PAY_AMT6", min_value=0.0, value=500.0)

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
    'PAY_1': int(pay_status1),
    'PAY_2': int(pay_status2),
    'PAY_3': int(pay_status3),
    'PAY_4': int(pay_status4),
    'PAY_5': int(pay_status5),
    'PAY_6': int(pay_status6),
    'BILL_AMT1': float(bill_amt1),
    'BILL_AMT2': float(bill_amt2),
    'BILL_AMT3': float(bill_amt3),
    'BILL_AMT4': float(bill_amt4),
    'BILL_AMT5': float(bill_amt5),
    'BILL_AMT6': float(bill_amt6),
    'PAY_AMT1': float(pay_amt1),
    'PAY_AMT2': float(pay_amt2),
    'PAY_AMT3': float(pay_amt3),
    'PAY_AMT4': float(pay_amt4),
    'PAY_AMT5': float(pay_amt5),
    'PAY_AMT6': float(pay_amt6),
    'entry_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Define comprehensive prediction logic
def predict_default(input_data):
    risk_score = 0
    
    # 1. Payment Delays Analysis
    payment_status = [input_data[f'PAY_{i}'] for i in [1, 2, 3, 4, 5, 6]]
    severe_delays = sum(1 for status in payment_status if status >= 2)
    if severe_delays >= 2:
        risk_score += 3
    
    # 2. Recent Default Status
    if input_data['PAY_1'] >= 1:
        risk_score += 2
    
    # 3. Credit Utilization
    bill_amounts = [input_data[f'BILL_AMT{i}'] for i in range(1, 7)]
    utilizations = [amt/input_data['LIMIT_BAL'] for amt in bill_amounts if input_data['LIMIT_BAL'] > 0]
    if len(utilizations) >= 3 and utilizations[-1] > 0.8:
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
    if input_data['EDUCATION'] in [3, 4]:
        demographic_risk += 1
    if input_data['MARRIAGE'] == 2:
        demographic_risk += 1
    if demographic_risk >= 2:
        risk_score += 0.5
    
    # 7. Balance Accumulation
    if len(bill_amounts) >= 4 and bill_amounts[-4] > 0:
        growth_rate = (bill_amounts[-1] - bill_amounts[-4]) / bill_amounts[-4]
        if growth_rate > 0.3:
            risk_score += 1
    
    return 1 if risk_score >= 4 else 0

# Make prediction
prediction = predict_default(input_data)
input_data['default.payment.next.month'] = prediction

# Display results
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

# Expandable Detailed Analysis section
with st.expander("📊 Detailed Analysis", expanded=False):
    st.write("**Payment Behavior:**")
    payment_status_desc = {
        -2: "No consumption",
        -1: "Paid in full",
        0: "Revolving credit",
        1: "1 month delay",
        2: "2 months delay",
    }
    for i, pay_var in enumerate(['PAY_1', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']):
        status = input_data[pay_var]
        st.write(f"{pay_var}: {payment_status_desc.get(status, f'{status} months delay')}")

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

# Expandable Demographic Factors section
with st.expander("👥 Demographic Factors", expanded=False):
    st.write(f"**Age:** {input_data['AGE']} ({'Young' if input_data['AGE'] < 30 else 'Middle-aged' if input_data['AGE'] < 50 else 'Senior'})")
    st.write(f"**Education:** {education}")
    st.write(f"**Marital Status:** {marriage}")
    st.write(f"**Gender:** {sex}")

# Save data to CSV
def save_to_csv(data):
    df = pd.DataFrame([data])
    
    columns_order = [
        'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
        'PAY_1', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
        'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
        'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6',
        'default.payment.next.month', 'entry_timestamp'
    ]
    df = df[columns_order]
    
    file_path = 'credit_card_predictions.csv'
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, index=False)
    
    return file_path

    # Add save button
    if st.button("Save Prediction"):
        file_path = save_to_csv(input_data)
        st.success(f"Prediction saved to {file_path}")
        st.balloons()
