import json
import requests
import os
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

class RouteAPI:
    """Class to handle interactions with MapmyIndia and TollGuru APIs."""

    def __init__(self):
        self.mapmyindia_api_key = os.getenv("MAPMYINDIA_API_KEY")
        self.mapmyindia_api_url = "https://apis.mapmyindia.com/advancedmaps/v1"
        self.tollguru_api_key = os.getenv("TOLLGURU_API_KEY")
        self.tollguru_api_url = "https://apis.tollguru.com/toll/v2"
        self.polyline_endpoint = "complete-polyline-from-mapping-service"

    def get_polyline_from_mapmyindia(self, source, destination):
        """Extrating Polyline from MapmyIndia"""
        url = f"{self.mapmyindia_api_url}/{{self.mapmyindia_api_key}}/route_adv/driving/{source[0]},{source[1]};{destination[0]},{destination[1]}?geometries=polyline&overview=full"
        response = requests.get(url).json()
        if 'message' in response:
            raise Exception(f"{response.get('code')}: {response.get('message')}")
        elif 'responsecode' in response and response['responsecode'] == "401":
            raise Exception(f"{response.get('error_code')} {response.get('error_description')}")
        return response["routes"][0]["geometry"]

    def get_rates_from_tollguru(self, polyline):
        """Calling TollGuru API"""
        url = f"{self.tollguru_api_url}/{self.polyline_endpoint}"
        headers = {"Content-type": "application/json", "x-api-key": self.tollguru_api_key}
        params = {
            "vehicle": {"type": "2AxlesAuto"},
            "departure_time": "2021-01-05T09:46:08Z",
            "source": "mapmyindia",
            "polyline": polyline
        }
        response = requests.post(url, json=params, headers=headers).json()
        if 'message' in response:
            raise Exception(response['message'])
        return response["route"]["costs"]

def main():
    route_api = RouteAPI()
    source = (77.18609677688849, 28.68932119156764)  # New Delhi
    destination = (72.89902799500808, 19.09258017366498)  # Mumbai
    
    try:
        # Step 1: Get polyline from MapmyIndia
        polyline = route_api.get_polyline_from_mapmyindia(source, destination)
        # Step 2: Get rates from TollGuru API
        rates = route_api.get_rates_from_tollguru(polyline)
        # Step 3: Print the rates
        if rates:
            logging.info(f"The rates are \n {rates}")
        else:
            logging.info("The route doesn't have tolls")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
