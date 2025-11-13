import requests

def send_tts_command(robot_ip, text, flush=False, utterance_id=None):
    # Define the endpoint URL
    url = f"http://{robot_ip}/api/tts/speak"
    
    # Prepare the payload with required and optional fields
    payload = {
        "Text": text,
        "Flush": flush
    }
    
    # Include UtteranceId if provided
    if utterance_id:
        payload["UtteranceId"] = utterance_id

    try:
        # Send the POST request
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Output the JSON response for success confirmation
        result = response.json()
        if result.get("Result", False):
            print("Command executed successfully:", result)
        else:
            print("Command execution encountered issues:", result)
    except requests.exceptions.RequestException as e:
        # Handle any errors (network issues, timeout, etc.)
        print(f"Request failed: {e}")

# Example usage
robot_ip = "192.168.1.237"  # Replace with the actual IP address of the robot
text = (
    "<speak>"
    "Hi there! I'm Misty, your personal robot assistant. "
    "This is an example of my text-to-speech."
    "</speak>"
)
flush = False  # Set to True if you want to flush the queue
utterance_id = "First"  # An optional unique identifier for this speech command

send_tts_command(robot_ip, text, flush, utterance_id)
