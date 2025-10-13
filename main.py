#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
import os
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

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
RECIPIENT_PHONE = os.environ.get('my_whatsapp_number')
print(AMADEUS_API_KEY, AMADEUS_API_SECRET, SHEET_DB_AUTH_TOKEN, TWILIO_AUTH_TOKEN, TWILIO_SID, TWILIO_PHONE, RECIPIENT_PHONE)
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


notification_manager = NotificationManager(twilio_sid= TWILIO_SID,
                                           twilio_phone= TWILIO_PHONE,
                                           twilio_auth_token= TWILIO_AUTH_TOKEN,
                                           cities= cities,
                                           cheapest_flights= cheapest_flights,
                                           )

send_all = notification_manager.send_message(RECIPIENT_PHONE)