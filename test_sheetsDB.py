import requests, json, smtplib
from email.message import EmailMessage

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

    enter_details = requests.post(url= SHEET_DB_ENDPOINT,
                                  params= params,
                                  headers= sheet_db_header,
                                  data= json.dumps(payload))

    if enter_details.status_code == 201:
        print("You're in the club!")
    else:
        print(f"Error: {enter_details.status_code} -> {enter_details.text}")

    get_data = requests.get(url= SHEET_DB_ENDPOINT,
                            headers=sheet_db_header,
                            params= params)
    json_data = get_data.json()

    print(json_data)

    sender_email = "samuel.e.achilike@gmail.com"
    password = "my_password"

    smtp_server = "smtp.gmail.com"
    smt_port = 587

    subject = "Cheapest Flight Notifications"
