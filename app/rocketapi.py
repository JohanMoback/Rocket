from flask import Flask, request, jsonify
import time
import requests
import concurrent.futures

app = Flask(__name__)
@app.route('/rocket', methods=['POST'])
def send_requests():
    data = request.json
    url = data.get('url')
    num_requests = data.get('numRequests')
    ramp_up_duration = data.get('rampUpDuration', 10)  # Duration of the ramp-up in seconds
    timeout = data.get('timeout', 10)  # Maximum time to wait for a response (in seconds)

    if not url or not num_requests:
        return jsonify({'error': 'Missing URL or numRequests in the request'}), 400

    def send_request():
        try:
            response = requests.get(url, timeout=timeout)
            return response
        except Exception as e:
            return f"Error: {str(e)}"

    start_time = time.time()
    responses = []

    def send_with_ramp_up(concurrent_requests, step_size, max_concurrent_requests):
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            futures = [executor.submit(send_request) for _ in range(concurrent_requests)]
            for future in concurrent.futures.as_completed(futures):
                response = future.result()
                responses.append(response)

            if concurrent_requests < max_concurrent_requests:
                time.sleep(ramp_up_duration / max_concurrent_requests)
                send_with_ramp_up(concurrent_requests + step_size, step_size, max_concurrent_requests)

    max_concurrent_requests = num_requests
    step_size = max_concurrent_requests // (ramp_up_duration // 1)

    send_with_ramp_up(step_size, step_size, max_concurrent_requests)

    end_time = time.time()
    total_time = (end_time - start_time) * 1000  # Convert to milliseconds

    data_transferred = sum(len(response.content) for response in responses if hasattr(response, 'content'))
    successful_responses = len([response for response in responses if hasattr(response, 'content') and response.status_code == 200])
    error_responses = num_requests - successful_responses

    response_data = {
        'total_time_ms': total_time,
        'average_response_time_ms': total_time / num_requests,
        'throughput_rps': num_requests / (end_time - start_time),
        'data_transferred_bytes': data_transferred,
        'successful_responses': successful_responses,
        'error_responses': error_responses
    }

    return jsonify(response_data)



if __name__ == '__main__':
    app.run(debug=True)
