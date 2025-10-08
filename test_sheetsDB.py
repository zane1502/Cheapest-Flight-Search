import requests

# ------- SheetDB -------
APP_ID = "ishy23zt006uy"
ENDPOINT = "https://sheetdb.io/api/v1/ishy23zt006uy"
AUTH_TOKEN = "py8y7l9tpwxnaizap733qbha7v7efozd0ypjyvkk"
# -----------------------


# ........... AMADEUS FLIGHT SEARCH ...........
AMADEUS_CITIES_URL = 'https://test.api.amadeus.com/v1/reference-data/locations/cities'

#..............................................
response = requests.get(url= ENDPOINT)

sheet_db_header = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {AUTH_TOKEN}'
          }

get_data = requests.get(url= ENDPOINT, headers=sheet_db_header)
json_data = get_data.json()

for i in range(len(json_data)):

    code = json_data[i]['IATA Code']
    city_name = json_data[i]['City']
    lowest_price = json_data[i]['Lowest Price']

    param = {'keyword':city_name,
             'max': 1}

    city_data = requests.get(url=f'{AMADEUS_CITIES_URL}', params= param)
    print(city_data.json())
    # iata_code = city_data.json()['data'][0]['iataCode']
    # data = [{
    #     'City': city_name,
    #     'IATA Code': iata_code,
    #     'Lowest Price': lowest_price
    # }]
    #
    # put_IATA_CODE = requests.put(url=f'{ENDPOINT}/City/{city_name}', headers= sheet_db_header, json= data)
    # print(put_IATA_CODE.status_code)

# new_entry = requests.put(url= f"{ENDPOINT}/id/5", headers=header, json=data)
# print(new_entry.status_code)