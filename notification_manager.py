from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""

    def __init__(self, twilio_sid, twilio_auth_token, cities, cheapest_flights, twilio_phone):
        """
        Initialize the NotificationManager with Twilio credentials and flight data.

        :param twilio_sid: Twilio Account SID
        :param twilio_auth_token: Twilio Auth Token
        :param cities: Dictionary mapping city names to IATA codes
        :param cheapest_flights: List of dictionaries containing flight information
        :param twilio_phone: Twilio WhatsApp phone number
        """
        self.twilio_sid = twilio_sid
        self.twilio_auth_token = twilio_auth_token
        self.cities = cities
        self.cheapest_flights = cheapest_flights
        self.twilio_phone = twilio_phone

    def send_message(self, recipient_phone):
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

    def send_single_message(self, recipient_phone, city_name, flight_info):
        """
        Send a single WhatsApp message for a specific flight.

        :param recipient_phone: Recipient's phone number
        :param city_name: Name of the destination city
        :param flight_info: Dictionary containing flight details
        :return: Tuple (success: bool, message_sid or error: str)
        """
        try:
            # Initialize Twilio client
            twilio_client = Client(self.twilio_sid, self.twilio_auth_token)

            # Validate flight info
            required_keys = ['departure_date', 'departure_time', 'return_date',
                             'return_time', 'currency', 'least_price']

            for key in required_keys:
                if key not in flight_info:
                    raise KeyError(f"Missing required field: {key}")

            # Build message
            message = f"Flight update!\nRound trip from London to {city_name}.\n"
            message += f"Flight Departure from {flight_info['departure_date']} by {flight_info['departure_time']}.\n"
            message += f"Return from {flight_info['return_date']} by {flight_info['return_time']}.\n"
            message += f"Price: {flight_info['currency']}{flight_info['least_price']}.\n"

            # Send message
            send = twilio_client.messages.create(
                from_=f"whatsapp:{self.twilio_phone}",
                to=f"whatsapp:{recipient_phone}",
                body=message
            )

            print(f"✓ Message sent successfully (SID: {send.sid})")
            return True, send.sid

        except TwilioRestException as e:
            error_msg = f"Twilio error: {e.msg} (Code: {e.code})"
            print(f"✗ {error_msg}")
            return False, error_msg

        except KeyError as e:
            error_msg = f"Missing data: {str(e)}"
            print(f"✗ {error_msg}")
            return False, error_msg

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"✗ {error_msg}")
            return False, error_msg