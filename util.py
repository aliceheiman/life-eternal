###########################
# LIBRARIES
###########################

import os
import requests

###########################
# FUNCTIONS
###########################


def generate(prompt, length, temperature, top_p):
    """Requests the GPT-SWE Completions AI and returns the response.

    Args:
        prompt (string): Text prompt for the model.
        length (int): The maximum number of tokens to generate.
        temperature (float): Temperature parameter.
        top_p (float): Top-P parameter.

    Returns:
        string: The answer
    """

    # Use the completion endpoint
    URL = "http://10.167.0.10:8080/v1/engines/gpt-sw3/completions"

    # Use JSON
    HEADERS = {"accept": "application/json", "Content-type": "application/json"}

    # Set up the API parameters
    PAYLOAD = {
        "prompt": prompt,
        "max_tokens": length,
        "temperature": temperature,
        "top_p": top_p,
        "n": 1,
        "stream": False,
        "stop": "<|endoftext|>",
    }

    # Make the request
    r = requests.post(url=URL, headers=HEADERS, json=PAYLOAD)

    # Check if the request came through
    if r.status_code == 200:

        # Convert response to json
        data = r.json()

        try:
            # Extract text answer from response
            answer = data["choices"][0]["text"]
        except:
            # Something failed
            answer = False

    else:
        # Something failed
        answer = False

    # Return the answer
    return answer
