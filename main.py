#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
import os
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from twilio.rest import Client

# APIs, Keys and secrets
SHEET_DB_ENDPOINT = "https://sheetdb.io/api/v1/ishy23zt006uy"
AMADEUS_CITIES_URL = 'https://test.api.amadeus.com/v1/reference-data/locations/cities'
AMADEUS_FLIGHT_PRICES = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
AMADEUS_API_KEY = os.environ.get('amadeus_api_key')
AMADEUS_API_SECRET = os.environ.get('amadeus_api_secret')
AMADEUS_OAUTH_URL = 'https://test.api.amadeus.com/v1/security/oauth2/token'
SHEET_DB_AUTH_TOKEN = os.environ.get('sheet_db_auth_token')
TWILIO_SID = os.environ.get('twilio_sid')
TWILIO_AUTH_TOKEN = os.environ.get('twilio_auth_token')
TWILIO_PHONE = os.environ.get('twilio_phone')

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

flight_prices = searches.get_price(cheapest_flight_url=AMADEUS_FLIGHT_PRICES)

cheapest_flights = FlightData(flight_prices= flight_prices).get_cheapest_flights()
print(cheapest_flights)

#Getting the city name and codes as dictionaries
cities = searches.get_iata_code(url= AMADEUS_CITIES_URL)

twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

for city, iata_code in cities.items():
    for row in cheapest_flights:
        if row['iata'] and iata_code == row['iata']:
            city_name = city

            message = f"Flight update!\nRound trip from London to {city_name}.\n"
            message += f"Flight Departure from {row['departure_date']} by {row['departure_time']}.\n"
            message += f"Return from {row['return_date']} by {row['return_time']}.\n"
            message += f"Price: {row['currency']}{row['least_price']}.\n"

            print(message)

            send = twilio_client.messages.create(from_= f"whatsapp:{TWILIO_PHONE}",
                                                 to= f"whatsapp:+2348054754075",
                                                 body=message)