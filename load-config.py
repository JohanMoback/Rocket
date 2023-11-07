import yaml
import requests

# Load the YAML file with test cases
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

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

    # Process the response as needed
    if response.status_code == 200:
        print(f"Test Case: {test_case_name} - Successful")
        # Add additional processing for successful responses
    else:
        print(f"Test Case: {test_case_name} - Failed (Status Code: {response.status_code})")
        print(response.text)  # Display response content for error details
        # Add error handling and logging for failed responses
