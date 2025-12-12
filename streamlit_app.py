"""
streamlit_app.py - Simple UI for Credit Risk Prediction

This app demonstrates:
1. A frontend (Streamlit) calling a backend API (FastAPI)
2. The model lives in FastAPI, not here
3. We only send HTTP requests and display results

Run with:
    streamlit run streamlit_app.py

Make sure FastAPI is running on http://localhost:8000 first!
"""

import requests
import streamlit as st

# ============================================================
# CONFIGURATION
# ============================================================
# This is where our FastAPI server is running
# Streamlit will send HTTP requests to this URL
# If using Docker: still localhost:8000 (Docker publishes the port)
API_URL = "http://localhost:8000/predict"

# ============================================================
# PAGE SETUP
# ============================================================
# set_page_config must be the first Streamlit command
# It sets the browser tab title, icon, and page layout
st.set_page_config(
    page_title="Credit Risk Predictor",
    page_icon="💳",
    layout="centered"
)

st.title("💳 Credit Risk Predictor")
st.markdown("Enter customer details below to get a **risk prediction** from the ML model.")
st.markdown("---")

# ============================================================
# INPUT FORM
# ============================================================
# st.columns() creates a horizontal layout - items placed in col1 appear left,
# items in col2 appear right. This makes the form more compact.
col1, col2 = st.columns(2)

with col1:
    checking_status = st.selectbox(
        "Checking Account",
        options=["low", "medium", "high", "none"],
        help="Balance level in checking account"
    )
    
    credit_history = st.selectbox(
        "Credit History",
        options=["bad", "ok", "good"],
        help="Overall credit history quality"
    )
    
    purpose = st.selectbox(
        "Loan Purpose",
        options=["car", "electronics", "furniture", "education", "other"]
    )
    
    savings_status = st.selectbox(
        "Savings Level",
        options=["low", "medium", "high", "none"]
    )

with col2:
    duration = st.slider(
        "Loan Duration (months)",
        min_value=6,
        max_value=72,
        value=24
    )
    
    credit_amount = st.number_input(
        "Credit Amount ($)",
        min_value=500,
        max_value=50000,
        value=5000,
        step=500
    )
    
    age = st.slider(
        "Age",
        min_value=18,
        max_value=75,
        value=35
    )
    
    employment = st.selectbox(
        "Employment Duration",
        options=["short", "medium", "long", "unemployed"]
    )

# ============================================================
# HIDDEN DEFAULTS (to keep UI simple)
# ============================================================
# The model needs ALL 20 features, but we only show 8 in the UI
# The rest use these default values (sent to API but not editable by user)
defaults = {
    "installment_commitment": 3,
    "personal_status": "single",
    "other_parties": "none",
    "residence_since": 2,
    "property_magnitude": "car",
    "other_payment_plans": "none",
    "housing": "own",
    "existing_credits": 1,
    "job": "skilled",
    "num_dependents": 1,
    "own_telephone": "yes",
    "foreign_worker": "no"
}

# ============================================================
# PREDICTION BUTTON
# ============================================================
st.markdown("---")

# st.button() returns True when clicked, False otherwise
# Streamlit reruns the entire script on each interaction
if st.button("🔮 Get Prediction", use_container_width=True):
    
    # Build the full payload - combine user inputs + hidden defaults
    # This dict will be converted to JSON and sent to FastAPI
    payload = {
        "checking_status": checking_status,
        "duration": duration,
        "credit_history": credit_history,
        "purpose": purpose,
        "credit_amount": credit_amount,
        "savings_status": savings_status,
        "employment": employment,
        "age": age,
        **defaults  # ** unpacks the dict, adding all key-value pairs
    }
    
    # Show a spinner while waiting for the API
    # st.spinner() displays a loading indicator until the block finishes
    with st.spinner("Calling the model API..."):
        try:
            # THIS IS THE KEY LINE: Send HTTP POST request to FastAPI
            # json=payload automatically converts dict to JSON string
            # timeout=10 means give up after 10 seconds
            response = requests.post(API_URL, json=payload, timeout=10)
            # raise_for_status() throws an exception if status code is 4xx or 5xx
            response.raise_for_status()
            # .json() parses the JSON response back into a Python dict
            result = response.json()
            
            # Display results
            st.markdown("### 📊 Prediction Result")
            
            # Use columns for nice layout
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.metric(
                    label="Default Probability",
                    value=f"{result['default_probability']:.1%}"
                )
            
            with res_col2:
                risk = result['risk_label']
                if risk == "high":
                    st.error(f"Risk Level: **{risk.upper()}** ⚠️")
                else:
                    st.success(f"Risk Level: **{risk.upper()}** ✅")
            
            # Show what was sent (for teaching purposes)
            with st.expander("See API request payload"):
                st.json(payload)
            
            with st.expander("See API response"):
                st.json(result)
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Is FastAPI running on http://localhost:8000?")
        except requests.exceptions.Timeout:
            st.error("❌ API request timed out.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ API error: {e}")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("This UI calls the FastAPI model service. The model is NOT in this app.")
