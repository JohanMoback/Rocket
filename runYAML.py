import json
import yaml
import requests
import streamlit as st
import pandas as pd
import time
from st_on_hover_tabs import on_hover_tabs

st.set_page_config(layout="wide")

# Set Rocket image in Streamlit
image_path = "resources/Rocket.png"  # Replace with the path to your image file
st.image(image_path, use_column_width=False)

# Set UI tabs
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)
with st.sidebar:
    tabs = on_hover_tabs(tabName=['Dashboard', 'Collections', 'Admin'],
                         iconName=['dashboard', 'money', 'economy'], default_choice=0)
if tabs =='Dashboard':
    st.title("Rocket Dashboard")
    def execute_api_calls(test_cases):
        responses = []

        # Loop through test cases and execute requests
        for test_case_name, test_case_params in test_cases.items():
            endpoint = test_case_params["endpoint"]
            method = test_case_params.get("method", "POST")
            payload = test_case_params.get("payload", {})
            test_duration = test_case_params.get("testDuration", 60)  # Default to 60 seconds if not specified

            # Continue executing requests until the specified duration is reached
            start_time = time.time()
            while time.time() - start_time < test_duration:
                if method == "POST":
                    response = requests.post(endpoint, json=payload)
                elif method == "GET":
                    response = requests.get(endpoint)
                end_time = time.time()

                responses.append({
                    "test_case": test_case_name,
                    "status_code": response.status_code,
                    "content": response.text,
                    "response_time": end_time - start_time
                })

            # Process the response as needed
            # Check if the API call was successful
            if response.status_code == 200:
                st.success(f"Test Case: {test_case_name} - API call successful")

                try:
                    # Try to load the response as JSON
                    response_data = response.json()

                    # Check if the response_data is a list or dictionary
                    if isinstance(response_data, (list, dict)):
                        # Display the response data as a DataFrame
                        response_df = pd.json_normalize(response_data) if isinstance(response_data,
                                                                                     dict) else pd.DataFrame(
                            response_data)
                        st.write(f"Response Data for Test Case {test_case_name}:")
                        st.write(response_df)

                except json.JSONDecodeError:
                    st.warning(f"Failed to decode JSON response for Test Case {test_case_name}.")

            else:
                st.error(f"Test Case: {test_case_name} - Failed (Status Code: {response.status_code})")
                st.write(f"Response Content for Test Case {test_case_name}: {response.text}")

        # Calculate average response time after all API calls
        avg_response_time = pd.DataFrame(responses).groupby("test_case")["response_time"].mean()

        # Display the average response time as a line chart
        st.line_chart(avg_response_time)

    # Streamlit UI
    st.title("API Load Test with YAML Configuration")

    uploaded_file = st.file_uploader("Upload a YAML file with test cases", type=["yaml", 'yml'])

    if uploaded_file is not None:
        # Load the YAML file with test cases
        try:
            config = yaml.safe_load(uploaded_file)
        except yaml.YAMLError as e:
            st.error(f"Error loading YAML file: {e}")
            st.stop()

        # Display the loaded test cases
        st.write("Loaded Test Cases:")
        st.write(config)
        if st.button("Execute API Call"):
            # Execute API calls based on the loaded test cases
            execute_api_calls(config)



elif tabs == 'Collections':
    st.title("Collections")
elif tabs == 'Admin':
    st.title("Admin")

# Execute API call when uploading YAML file
