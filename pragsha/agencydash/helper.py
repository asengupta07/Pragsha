import requests
from userdash.models import Broadcast

def funky():
    api_key = "AoCUncNX_-l6FfT1nHyketx4jOn1zrAIiBzGfYei8zgT9CUyVqxRckBBMZYI18Zx"
    base_url = "http://dev.virtualearth.net/REST/v1/Locations/"
    coordinates = [(id, latitude, longitude) for (id, latitude, longitude) in Broadcast.objects.filter(is_accepted=False).values_list('id', 'latitude', 'longitude')]

    addresses = {}

    for (id, lat, lon) in coordinates:
        request_url = f"{base_url}{lat},{lon}?key={api_key}"
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
    return addresses


def get_locality(lat, lon):
    api_key = "AoCUncNX_-l6FfT1nHyketx4jOn1zrAIiBzGfYei8zgT9CUyVqxRckBBMZYI18Zx"
    base_url = "http://dev.virtualearth.net/REST/v1/Locations/"
    request_url = f"{base_url}{lat},{lon}?key={api_key}"
    response = requests.get(request_url)
    if response.status_code == 200:
        data = response.json()
        if data["resourceSets"][0]["estimatedTotal"] > 0:
            address = data["resourceSets"][0]["resources"][0]["address"]
            return address['locality']
        else:
            return "Address not found"
    else:
        return "API request failed"
