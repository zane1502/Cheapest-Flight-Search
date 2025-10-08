import requests

# ------- SheetDB -------
APP_ID = "ishy23zt006uy"
SHEET_DB_ENDPOINT = "https://sheetdb.io/api/v1/ishy23zt006uy"
AUTH_TOKEN = "py8y7l9tpwxnaizap733qbha7v7efozd0ypjyvkk"
# -----------------------


# ........... AMADEUS FLIGHT SEARCH ...........
AMADEUS_CITIES_URL = 'https://test.api.amadeus.com/v1/reference-data/locations/cities'
API_KEY = 'kIOt0ww30zdmV4Xk6hkQ2hHVaqzkzbJS'
API_SECRET = 'OSUVGAihIZFqucb8'
OAUTH_URL = 'https://test.api.amadeus.com/v1/security/oauth2/token'

grant_type = 'client_credentials'
client_data = {
        'client_id' : API_KEY,
        'client_secret': API_SECRET,
        'grant_type': grant_type
    }
auth_response = requests.post(url=OAUTH_URL, data= client_data)
auth_token = auth_response.json()['access_token']

header = {'Authorization': f'Bearer {auth_token}'}

#..............................................
response = requests.get(url= SHEET_DB_ENDPOINT)

sheet_db_header = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {AUTH_TOKEN}'
          }

get_data = requests.get(url= SHEET_DB_ENDPOINT, headers=sheet_db_header)
json_data = get_data.json()

for i in range(len(json_data)):
    city_name = json_data[i]['City']
    lowest_price = json_data[i]['Lowest Price']

    param = {'keyword':city_name,
             'max': 1}

    city_data = requests.get(url=f'{AMADEUS_CITIES_URL}', params= param, headers=header)
    iata_code = city_data.json()['data'][0]['iataCode']
    data = [{
        'City': city_name,
        'IATA Code': iata_code,
        'Lowest Price': lowest_price
    }]

    put_IATA_CODE = requests.put(url=f'{SHEET_DB_ENDPOINT}/City/{city_name}', headers= sheet_db_header, json= data)
    print(put_IATA_CODE.status_code)

# new_entry = requests.put(url= f"{SHEET_DB_ENDPOINT}/id/5", headers=header, json=data)
# print(new_entry.status_code)