import requests, json

# ------- SheetDB -------
APP_ID = "ishy23zt006uy"
SHEET_DB_ENDPOINT = "https://sheetdb.io/api/v1/ishy23zt006uy"
AUTH_TOKEN = "py8y7l9tpwxnaizap733qbha7v7efozd0ypjyvkk"
# -----------------------

sheet_db_header = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {AUTH_TOKEN}'
          }

first_name = input('What is your first name? ')
last_name = input('What is your last name? ')
email = input('What is your email address? ')
email_confirm = input('Enter Your email again please: ')


if email == email_confirm:
    payload = {
        'data' :
                    {'id': 'INCREMENT',
                     'First Name': first_name,
                      'Last Name': last_name,
                      'Email': email
                      }

    }
    params = {'sheet': 'users'}

    enter_details = requests.post(url=SHEET_DB_ENDPOINT, params= params, headers= sheet_db_header, data= json.dumps(payload))

    if enter_details.status_code == 201:
        print("You're in the club!")
    else:
        print(f"Error: {enter_details.status_code} -> {enter_details.text}")

    get_data = requests.get(url= SHEET_DB_ENDPOINT, headers=sheet_db_header, params= params)
    json_data = get_data.json()



# for i in range(len(json_data)):
#     city_name = json_data[i]['City']
#     lowest_price = json_data[i]['Lowest Price']
#
#     param = {'keyword':city_name,
#              'max': 1}
#
#     city_data = requests.get(url=f'{AMADEUS_CITIES_URL}', params= param, headers=header)
#     iata_code = city_data.json()['data'][0]['iataCode']
#     data = [{
#         'City': city_name,
#         'IATA Code': iata_code,
#         'Lowest Price': lowest_price
#     }]
#
#     put_IATA_CODE = requests.put(url=f'{SHEET_DB_ENDPOINT}/City/{city_name}', headers= sheet_db_header, json= data)
#     print(put_IATA_CODE.status_code)
#
# # new_entry = requests.put(url= f"{SHEET_DB_ENDPOINT}/id/5", headers=header, json=data)
# # print(new_entry.status_code)