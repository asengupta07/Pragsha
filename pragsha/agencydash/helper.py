import requests
from userdash.models import Broadcast

def funky():
    # Replace with your Bing Maps API key
    api_key = "AoCUncNX_-l6FfT1nHyketx4jOn1zrAIiBzGfYei8zgT9CUyVqxRckBBMZYI18Zx"

    # Define the Bing Maps Reverse Geocoding API endpoint
    base_url = "http://dev.virtualearth.net/REST/v1/Locations/"

    # List of coordinates to reverse geocode
    coordinates = [(id, latitude, longitude) for (id, latitude, longitude) in Broadcast.objects.filter(is_accepted=False).values_list('id', 'latitude', 'longitude')]

    addresses = {}

    for (id, lat, lon) in coordinates:
        # Create the request URL for reverse geocoding
        request_url = f"{base_url}{lat},{lon}?key={api_key}"

        # Make the HTTP request
        response = requests.get(request_url)
        

        if response.status_code == 200:
            data = response.json()
            if data["resourceSets"][0]["estimatedTotal"] > 0:
                address = data["resourceSets"][0]["resources"][0]["address"]
                addresses[id] = address['formattedAddress']
            else:
                addresses[id] = "Address not found"
        else:
            addresses[id] = "API request failed"
    # The 'addresses' list now contains the reverse geocoded addresses
    return addresses
