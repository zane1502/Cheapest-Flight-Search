#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import requests
from data_manager import DataManager
from flight_search import FlightSearch

# APIs, Keys and secrets
SHEET_DB_ENDPOINT = "https://sheetdb.io/api/v1/ishy23zt006uy"
AMADEUS_CITIES_URL = 'https://test.api.amadeus.com/v1/reference-data/locations/cities'
AMADEUS_FLIGHT_PRICES = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
AMADEUS_API_KEY = 'kIOt0ww30zdmV4Xk6hkQ2hHVaqzkzbJS'
AMADEUS_API_SECRET = 'OSUVGAihIZFqucb8'
AMADEUS_OAUTH_URL = 'https://test.api.amadeus.com/v1/security/oauth2/token'
SHEET_DB_AUTH_TOKEN = "py8y7l9tpwxnaizap733qbha7v7efozd0ypjyvkk"

# Authorization credentials
grant_type = 'client_credentials'
client_data = {
        'client_id' : AMADEUS_API_KEY,
        'client_secret': AMADEUS_API_SECRET,
        'grant_type': grant_type
    }
auth_response = requests.post(url=AMADEUS_OAUTH_URL, data= client_data)
amadeus_auth_token = auth_response.json()['access_token']

sheet = DataManager(SHEET_DB_ENDPOINT, SHEET_DB_AUTH_TOKEN)
sheet_data = sheet.sheet_data
searches = FlightSearch(sheet_data= sheet_data, auth_token=amadeus_auth_token)

#city_code_map = searches.get_iata_code(url= AMADEUS_CITIES_URL)

flight_prices = searches.get_price(cheapest_flight_url=AMADEUS_FLIGHT_PRICES)
print(flight_prices)