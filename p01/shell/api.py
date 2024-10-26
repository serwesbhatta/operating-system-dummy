import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("API_URL")

def api(endpoint, method = "get", params=None, data=None, headers=None):

  url = f"{url}/{endpoint}"
  
  if headers is None:
    headers = {"Content-Type": "application/json"}

  if method.lower() == "get":
    try:
      response = requests.get(url,params=params, headers=headers)
    except:
      print("Bad get request")
  elif method.lower() == "post":
    try:
      response = requests.post(url, json=data, headers=headers)
    except:
      print("Bad post request")
  elif method.lower() == "put":
    try:
      response = requests.put(url, json=data, headers=headers)
    except:
      print("Bad put request")
  elif method.lower() == "delete":
    try:
      response = requests.delete(url, json=data, headers=headers)
    except:
      print("Bad delete request")
  else:
    raise ValueError("Unsupported HTTP method")
  
  if response.status_code == 200:
    return response.json()
  else:
    print(f"Status code : {response.status_code}. Bad Api call")