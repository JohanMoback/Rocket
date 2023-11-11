import json
import yaml
import requests
import streamlit as st
import pandas as pd

if st.button("Execute API Call"):
    # Load the YAML file with test cases
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    responses = {}

    # Loop through test cases and execute requests
    for test_case_name, test_case_params in config.items():
        endpoint = test_case_params["endpoint"]
        method = test_case_params.get("method", "POST")
        payload = test_case_params.get("payload", {})

        # Make the HTTP request
        if method == "POST":
            response = requests.post(endpoint, json=payload)
        elif method == "GET":
            response = requests.get(endpoint)

        responses[test_case_name] = {
            "status_code": response.status_code,
            "content": response.text
        }

        # Process the response as needed
        # Check if the API call was successful
        if response.status_code == 200:
            st.success("API call successful")

            try:
                # Try to load the response as JSON
                response_data = response.json()

                # Check if the response_data is a list or dictionary
                if isinstance(response_data, (list, dict)):
                    # Display the response data as a DataFrame
                    response_df = pd.json_normalize(response_data) if isinstance(response_data, dict) else pd.DataFrame(
                        response_data)
                    st.write("Response Data:")
                    st.write(response_df)
                else:
                    st.warning("Response data is not a valid structure for DataFrame.")

            except json.JSONDecodeError:
                st.warning("Failed to decode JSON response.")

        else:
            print(f"Test Case: {test_case_name} - Failed (Status Code: {response.status_code})")
            print(response.text)  # Display response content for error details
