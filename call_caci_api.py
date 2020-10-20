import requests
import base64
from jose import jwk, jwt
from jose.utils import base64url_decode


def get_token():
    app_client_id = '<YOUR_CLIENT_ID>'
    app_client_secret = '<YOUR_CLIENT_SECRET>'

    plain_token_bytes = '{}:{}'.format(app_client_id, app_client_secret).encode('utf-8')
    basic_auth_token = base64.b64encode(plain_token_bytes).decode('utf-8')

    headers = {'authorization': 'Basic {}'.format(basic_auth_token)}

    data={
        'grant_type': 'client_credentials', 
        'scope': 'ocean/* ocean/segments'
    }

    r = requests.post("https://auth.api.caci.co.uk/oauth2/token", headers=headers, data=data)
    return r.json()['access_token']    

def run_ocean_call(access_token):
    url = "https://data.api.caci.co.uk/v1/ocean/single/"
    request_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)    
    }

    data = {
        "uid": "101",					
        "title": "<TITLE>",
        "forename": "<FORENAME>",
        "surname": "<SURNAME>",
        "address_line_1": "<ADDRESS_LINE_1>",
        "postcode": "<POSTCODE>"        
    }

    r = requests.post(url, headers=request_headers, json=data)

    if r.status_code == 200:
        return r.json()

def run_segments_call(access_token):
    url = "https://data.api.caci.co.uk/v1/segments/single/"
    request_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)    
    }

    data = {
        "uid": "101",					
        "title": "<TITLE>",
        "forename": "<FORENAME>",
        "surname": "<SURNAME>",
        "address_line_1": "<ADDRESS_LINE_1>",
        "postcode": "<POSTCODE>",
        "segment_params": {
            "ATP":	10,
            "SEEN_MATINEE":	"Y",
            "SEEN_WEEKEND":	"Y",
            "BOUGHT_PACKAGE": "Y",
            "SEEN_GIG_CONCERT":	"N",
            "CALL_CENTRE":	"Y",
            "OVER_COUNTER": "N"
        }
    }

    r = requests.post(url, headers=request_headers, json=data)
    if r.status_code == 200:
        return r.json()

token = get_token()
ocean_fresco = run_ocean_call(token)
segments = run_segments_call(token)

all_vars = {**ocean_fresco, **segments}
print(all_vars)