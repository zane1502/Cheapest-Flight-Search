from datetime import datetime


class FlightData:
    #This class is responsible for structuring the flight data.
    """
    This class should receive a parameter called flight_prices which is a json data containing a dictionary of flight
    offers prices to and from specified locations within a specified timeframe.

    Any object of the class should be able to give the lowest possible prices of each city, and the departure
    and return dates.
    """

    def __init__(self, flight_prices):
        self.flight_prices = flight_prices

    def get_cheapest_flights(self):

        # Total flight data
        flight_data = []
        for iata_code, offers in self.flight_prices.items():
            city_offers_map = {}
            data = offers["data"]
            city_data = []

            for i in data:
                offer_info = {}

                offer_info["price"] = i["price"]["total"]
                offer_info["currency"] = i["price"]["currency"]

                departure = i["itineraries"][0]["segments"][0]["departure"]["at"]
                offer_info["departure_date"] = str(datetime.fromisoformat(departure).date())
                offer_info["departure_time"] = str(datetime.fromisoformat(departure).time())

                returns = i["itineraries"][1]["segments"][0]["departure"]["at"]
                offer_info["return_date"] = str(datetime.fromisoformat(returns).date())
                offer_info["return_time"] = str(datetime.fromisoformat(returns).time())

                city_data.append(offer_info)

            city_offers_map[iata_code] = city_data
            flight_data.append(city_offers_map)

        cheapest_flights = []
        for i in flight_data:
            iata_code = list(i.keys())[0]  # extract the key
            offers = i[iata_code]  # list of offer dicts

            # Skip if no offers for this city
            if not offers:
                continue

            # Initialize with the first offer
            flight = {
                "iata": iata_code,
                "least_price": float(offers[0]["price"]),
                "currency": offers[0]["currency"],
                "departure_date": offers[0]["departure_date"],
                "departure_time": offers[0]["departure_time"],
                "return_date": offers[0]["return_date"],
                "return_time": offers[0]["return_time"]
            }

            # Find the minimum price among offers
            for n in offers:
                if float(n["price"]) < flight["least_price"]:
                    flight["least_price"] = float(n["price"])
                    flight["currency"] = n["currency"]
                    flight["departure_date"] = n["departure_date"]
                    flight["departure_time"] = n["departure_time"]
                    flight["return_date"] = n["return_date"]
                    flight["return_time"] = n["return_time"]

            cheapest_flights.append(flight)

        return cheapest_flights