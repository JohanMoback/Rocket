import requests
import streamlit as st
import pandas as pd

data = {
    "url": "https://example.com",
    "numRequests": 10,
    "concurrentRequests": 2,
    "rampUpDuration": 1,
    "timeout": 5
}

headers = {
    "Content-Type": "application/json"
}

# Define the Streamlit app
st.title("API Call and Dashboard Visualization")

# Create a button to trigger the API call
if st.button("Execute API Call"):
    # Define the API endpoint URL
    api_endpoint = "http://127.0.0.1:5000/rocket"

    # Make the API call
    response = requests.post(api_endpoint, data=data, headers=headers)

    # Check if the API call was successful
    if response.status_code == 200:
        st.success("API call successful")

        # Visualize the response (assuming the response is in JSON format)
        response_data = response.json()

        # Display the response data as a DataFrame
        response_df = pd.DataFrame(response_data)
        st.write("Response Data:")
        st.write(response_df)

        # You can add more visualization components here based on your data

    else:
        st.error(f"API call failed with status code: {response.status_code}")
        st.write(response.text)  # Display the response content for error details

