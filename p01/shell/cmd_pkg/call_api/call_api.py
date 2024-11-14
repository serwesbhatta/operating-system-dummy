import requests
from dotenv import load_dotenv
import os

load_dotenv()

base_url = os.getenv("API_URL")

def call_api(endpoint, method="get", params=None, data=None, headers=None):
    url = f"{base_url}{endpoint}"
    headers = {"Content-Type": "application/json"}

    try:
        if method.lower() == "get":
            response = requests.get(url, params=params, headers=headers)
        elif method.lower() == "post":
            response = requests.post(url, json=data, headers=headers)
        elif method.lower() == "put":
            response = requests.put(url, json=data, headers=headers)
        elif method.lower() == "delete":
            response = requests.delete(url, json=data, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")

        # Handle response status
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            print(f"API call failed with status code {response.status_code}: {response.text}")
            return None

    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None
