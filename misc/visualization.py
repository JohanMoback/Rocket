import json
import yaml
import requests
import streamlit as st
import pandas as pd
import time
from io import StringIO
from st_on_hover_tabs import on_hover_tabs

st.set_page_config(layout="wide")
# Set Rocket image in Streamlit
image_path = "../resources/Rocket.png"  # Replace with the path to your image file
st.image(image_path, use_column_width=False)


st.markdown('<style>' + open('../streamlit/style.css').read() + '</style>', unsafe_allow_html=True)


with st.sidebar:
    tabs = on_hover_tabs(tabName=['Dashboard', 'Collections', 'Admin'],
                         iconName=['dashboard', 'money', 'economy'], default_choice=0)

if tabs =='Dashboard':
    st.title("Rocket Dashboard")
    #st.write('Name of option is {}'.format(tabs))

elif tabs == 'Collections':
    st.title("Collections")
    st.write('Name of option is {}'.format(tabs))

elif tabs == 'Admin':
    st.title("Admin")
    st.write('Name of option is {}'.format(tabs))


# On button call the API
if st.button("Execute API Call"):
    # Load the YAML file with test cases
    with open(config, "r") as config_file:
        config = yaml.safe_load(config_file)

    responses = []

    # Loop through test cases and execute requests
    for test_case_name, test_case_params in config.items():
        endpoint = test_case_params["endpoint"]
        method = test_case_params.get("method", "POST")
        payload = test_case_params.get("payload", {})

        # Make the HTTP request and record the time before and after the request
        start_time = time.time()
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
            st.success("API call successful")

            try:
                # Try to load the response as JSON
                response_data = response.json()

                # Check if the response_data is a list or dictionary
                if isinstance(response_data, (list, dict)):
                    # Display the response data as a DataFrame
                    response_df = pd.json_normalize(response_data) if isinstance(response_data, dict) else pd.DataFrame(response_data)
                    st.write("Response Data:")
                    st.write(response_df)

            except json.JSONDecodeError:
                st.warning("Failed to decode JSON response.")

    # Calculate average response time after all API calls
    avg_response_time = pd.DataFrame(responses).groupby("test_case")["response_time"].mean()

    # Display the average response time as a line chart
    st.line_chart(avg_response_time)
