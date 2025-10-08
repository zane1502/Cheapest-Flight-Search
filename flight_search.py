import requests
from datetime import datetime, timedelta

class FlightSearch:
    """This class is responsible for talking to the Flight Search API."""

    def __init__(self, sheet_data, auth_token):

        """
        An object must be initialized with the sheet data and auth token
        :param sheet_data:
        :param auth_token:
        """
        self.sheet_data = sheet_data
        self.auth_token = auth_token

    def get_iata_code(self, url):
        """
        The url being passed into the method is the endpoint for the Amadeus cities search API.
        The method returns a dictionary of cities with their respective IATA code.

        :param url:
        :return: city_code_map
        """
        city_code_map = {}

        # Iterating through each 'row' in sheet data, which is a dictionary of details about each city
        for row in self.sheet_data:
            # Mapping the name of each row to it's city
            city = row['city']

            params = {
                'keyword': {city},
                'max': '1'
            }
            header = {'Authorization': f'Bearer {self.auth_token}'}
            response = requests.get(url=url, params=params, headers=header)
            output = response.json()

            iata_code = output['data'][0]['iataCode']
            print(f"{city}, {iata_code}")

            city_code_map[city] = iata_code

        return city_code_map
