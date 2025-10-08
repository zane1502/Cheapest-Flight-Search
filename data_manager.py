import requests

class DataManager:
    def __init__(self, sheet_url: str, auth_token):

        """
        An object of the data manager class must be initialized with the url to the SheetDB API and the auth token of
        the API to authorize the request being made.
        :param sheet_url:
        :param auth_token:
        """
        self.sheet_url = sheet_url
        self.sheet_db_header = {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                'Authorization': f'Bearer {auth_token}'
          }
        self.sheet_data =  requests.get(url= self.sheet_url, headers=self.sheet_db_header).json()

    def put_row(self, city_code_map):

        """
        This method is responsible for putting the row data of each city in a cell, with the city name, IATA code and
        the historical lowest price of a flight from that city to London.
        :param city_code_map:
        :return:
        """

        for row in self.sheet_data:
            city_name = self.sheet_data[row]['City']
            lowest_price = self.sheet_data[row]['Lowest Price']

            if city_name in city_code_map:

                iata_code = city_code_map.json()['data'][0]['iataCode']
                data = [{
                    'City': city_name,
                    'IATA Code': iata_code,
                    'Lowest Price': lowest_price
                }]

                put_IATA_CODE = requests.put(url=f'{self.sheet_url}/City/{city_name}', headers=self.sheet_db_header,
                                             json=data)
                print(put_IATA_CODE.status_code)