import pandas as pd
import streamlit as st

# Load your data
@st.cache
def load_data(file):
    return pd.read_excel(file)  # Adjust if using CSV

# Streamlit app title
st.title("Data Analysis App")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "csv"])

if uploaded_file:
    # Load the data
    data = load_data(uploaded_file)

    # Display raw data and column names
    st.subheader("Raw Data")
    st.write(data)
    st.write("Column Names:", data.columns.tolist())  # Display column names

    # Check for required columns
    required_columns = ['Date', 'Activity', 'Duration']
    if not all(col in data.columns for col in required_columns):
        st.error("Required columns are missing. Please ensure the file has 'Date', 'Activity', and 'Duration' columns.")
        st.stop()

    # Ensure 'Date' is datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Convert to datetime, handling errors

    # 1. Datewise total duration for inside and outside
    inside_duration = data[data['Activity'] == 'inside'].groupby(data['Date'].dt.date)['Duration'].sum()
    outside_duration = data[data['Activity'] == 'outside'].groupby(data['Date'].dt.date)['Duration'].sum()

    # Create a summary DataFrame
    summary_duration = pd.DataFrame({
        'Inside Duration': inside_duration,
        'Outside Duration': outside_duration
    }).fillna(0)  # Fill NaN values with 0

    st.subheader("Datewise Total Duration")
    st.line_chart(summary_duration)

    # 2. Datewise number of picking and placing activities
    picking_count = data[data['Activity'] == 'picking'].groupby(data['Date'].dt.date).size()
    placing_count = data[data['Activity'] == 'placing'].groupby(data['Date'].dt.date).size()

    # Create a summary DataFrame
    activity_count = pd.DataFrame({
        'Picking Count': picking_count,
        'Placing Count': placing_count
    }).fillna(0)

    st.subheader("Datewise Activity Count")
    st.line_chart(activity_count)

# Run the app with: streamlit run app.py
