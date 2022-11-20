### optimizer 
import requests

def dispatch_module(json_data):
    
    resp = requests.post(f"http://julia.eng.usf.edu:4532/pdp", json=json_data)
    result = resp.json()

    return result, json_data['coordinates']