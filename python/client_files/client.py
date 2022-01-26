import requests
import json

def get_good_tube_api_response(task: str, parametrs: dict) -> str:    
    base_url = "http://92.255.108.65:12345"
    request = f"{base_url}/{task}"

    response = requests.get(request, params=parametrs)
    
    data = json.loads(response.text)

    return data    
