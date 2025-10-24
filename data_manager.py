import requests
import json

class DataManager:
    def __init__(self, sheet_url: str, auth_token):

        """
        An object of the data manager class must be initialized with the url to the SheetDB API and the auth token of
        the API to authorize the request being made.

        Visit https://docs.sheetdb.io/ to learn about how to use the SheetDB API to structure data into Google Spreadsheets.

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

                # Take note of the format of the data that is acceptable by the SheetDB API. It must be json format.
                put_IATA_CODE = requests.put(url=f'{self.sheet_url}/City/{city_name}', headers=self.sheet_db_header,
                                             json=data)
                print(put_IATA_CODE.status_code)

    def add_user_email(self):
        """
        This method collects basic information - name and email - from a user and puts it in a new cell under the same
        spreadsheet.
        :returns: users_data
        """

        first_name = input('What is your first name? ')
        last_name = input('What is your last name? ')
        email = input('What is your email address? ')
        email_confirm = input('Enter Your email again please: ')

        if email == email_confirm:
            payload = {
                'data':
                    {'id': 'INCREMENT',
                     'First Name': first_name,
                     'Last Name': last_name,
                     'Email': email
                     }

            }

            params = {'sheet': 'users'}

            # Once again be careful to note the that the post request requires that the data being created into the
            # Google Spreadsheet must be a json format. Took me a while to figure how to do this in python, but the
            # 'dumps' method can be used to convert the required data to a json format.

            enter_details = requests.post(url=self.sheet_url,
                                          params=params,
                                          headers=self.sheet_db_header,
                                          data=json.dumps(payload))

            if enter_details.status_code == 201:
                print("You're in the club!")
            else:
                print(f"Error: {enter_details.status_code} -> {enter_details.text}")

            get_data = requests.get(url=self.sheet_url,
                                    headers=self.sheet_db_header,
                                    params=params)
            users_data = get_data.json()

            return users_data

        else:
            print("Wrong email!")
            return None # Fix this, not ideal. Don't be lazy
