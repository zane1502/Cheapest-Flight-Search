from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import smtplib, ssl
from email.message import EmailMessage

class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""

    def __init__(self, twilio_sid, twilio_auth_token, cities, cheapest_flights, twilio_phone):
        """
        Initialize the NotificationManager with Twilio credentials and flight data.

        :param twilio_sid: Twilio Account SID
        :param twilio_auth_token: Twilio Auth Token
        :param cities: Dictionary mapping city names to IATA codes
        :param cheapest_flights: List of dictionaries containing flight information
        """
        self.twilio_sid = twilio_sid
        self.twilio_auth_token = twilio_auth_token
        self.cities = cities
        self.cheapest_flights = cheapest_flights
        self.twilio_phone = twilio_phone

    def send_whatsapp_message(self, recipient_phone):
        """
        Send WhatsApp messages for all matching flight deals.

        :param recipient_phone: Recipient's phone number (with country code, e.g., +2348054754075)
        :return: Dictionary with success count, failed count, and error details
        """
        results = {
            'successful': 0,
            'failed': 0,
            'errors': []
        }

        # Validate inputs
        if not self.cities or not self.cheapest_flights:
            error_msg = "No cities or flight data available to send notifications."
            print(f"Error: {error_msg}")
            results['errors'].append(error_msg)
            return results

        # Initialize Twilio client with error handling
        try:
            twilio_client = Client(self.twilio_sid, self.twilio_auth_token)
        except Exception as e:
            error_msg = f"Failed to initialize Twilio client: {str(e)}"
            print(f"Error: {error_msg}")
            results['errors'].append(error_msg)
            return results

        # Send messages for each matching flight
        for city, iata_code in self.cities.items():
            for row in self.cheapest_flights:
                try:
                    # Check if IATA codes match
                    if row.get('iata') and iata_code == row['iata']:
                        city_name = city

                        # Build message
                        message = f"Flight update!\nRound trip from London to {city_name}.\n"
                        message += f"Flight Departure from {row['departure_date']} by {row['departure_time']}.\n"
                        message += f"Return from {row['return_date']} by {row['return_time']}.\n"
                        message += f"Price: {row['currency']}{row['least_price']}.\n"

                        print(f"Sending message for {city_name}...")
                        print(message)

                        # Send WhatsApp message
                        send = twilio_client.messages.create(
                            from_=f"whatsapp:{self.twilio_phone}",
                            to=f"whatsapp:{recipient_phone}",
                            body=message
                        )


                        # Check message status
                        if send.status in ['queued', 'sent', 'delivered']:
                            results['successful'] += 1
                            print(f"✓ Message sent successfully to {recipient_phone} (SID: {send.sid})")
                        else:
                            results['failed'] += 1
                            error_msg = f"Message status: {send.status} for {city_name}"
                            results['errors'].append(error_msg)
                            print(f"⚠ Warning: {error_msg}")

                except TwilioRestException as e:
                    # Handle Twilio-specific errors
                    results['failed'] += 1
                    error_msg = f"Twilio error for {city}: {e.msg} (Code: {e.code})"
                    results['errors'].append(error_msg)
                    print(f"✗ {error_msg}")

                except KeyError as e:
                    # Handle missing keys in flight data
                    results['failed'] += 1
                    error_msg = f"Missing data key for {city}: {str(e)}"
                    results['errors'].append(error_msg)
                    print(f"✗ {error_msg}")

                except Exception as e:
                    # Handle any other unexpected errors
                    results['failed'] += 1
                    error_msg = f"Unexpected error for {city}: {str(e)}"
                    results['errors'].append(error_msg)
                    print(f"✗ {error_msg}")

        # Print summary
        print("\n" + "=" * 50)
        print(f"NOTIFICATION SUMMARY:")
        print(f"✓ Successful: {results['successful']}")
        print(f"✗ Failed: {results['failed']}")
        if results['errors']:
            print(f"\nErrors encountered:")
            for error in results['errors']:
                print(f"  - {error}")
        print("=" * 50)

        return results

    def send_email(self, users_emails):
        """
        Send emails for all matching flight deals.

        :return: Dictionary with success count, failed count, and error details
        """
        for user in users_emails:
            name = user['First Name']
            receiver_email = user['Email']
            sender_email = "210403053@live.unilag.edu.ng"
            app_password = "your_app_password_here"

            smtp_server = "smtp.office365.com"
            smtp_port = 587  # TLS port

            subject = "Cheapest Flights Notifications"

            for city, iata_code in self.cities.items():
                for row in self.cheapest_flights:
                    if row.get('iata') and iata_code == row['iata']:
                        city_name = city
                        message = (
                            f"Hey {name}! Here's your flight update...\n\n"
                            f"Round trip from London to {city_name}.\n"
                            f"Departure: {row['departure_date']} at {row['departure_time']}.\n"
                            f"Return: {row['return_date']} at {row['return_time']}.\n"
                            f"Price: {row['currency']}{row['least_price']}.\n"
                        )

                        print(f"Sending message for {city_name}...")

                        send_message = EmailMessage()
                        send_message["From"] = sender_email
                        send_message["To"] = receiver_email
                        send_message["Subject"] = subject
                        send_message.set_content(message)

                        # Connect and send
                        with smtplib.SMTP(smtp_server, smtp_port) as server:
                            server.starttls()  # Upgrade to secure connection
                            server.login(sender_email, app_password)
                            server.send_message(send_message)
                        print("Email sent successfully!")
