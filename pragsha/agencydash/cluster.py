from geopy.distance import geodesic
import rancoord as rc
import json

poly = rc.Polygon(
    [
        (22.62368419083518, 88.41940793401186),
        (22.628560169387445, 88.41640046113686),
        (22.62832744786009, 88.42883244483792),
        (22.620504194986193, 88.42697055648333)
    ]
)

poly2 = rc.Polygon(
    [
        (22.6009269720376, 88.4147718678721),
        (22.58974725201452, 88.43193276473102),
        (22.58213354891588, 88.41350894472664),
        (22.592353648259863, 88.40147403004634)
    ]
)

lat,lon = rc.coordinates_randomizer(polygon = poly, num_locations = 40, plot = True, save = True)[:-1]

lat2,lon2 = rc.coordinates_randomizer(polygon = poly2, num_locations = 20, plot = True, save = True)[:-1]


print(json.dumps([lat2,lon2], indent=4))


emergencies = [
    {"lat": 40.7128, "lon": -70.0060},
    {"lat": 41.7130, "lon": -71.0061},
    {"lat": 42.7135, "lon": -72.0058},
    {"lat": 39.7110, "lon": -69.0055},
    {"lat": 39.7105, "lon": -72.0065},
    {"lat": 40.7120, "lon": -72.0070},
    {"lat": 40.7145, "lon": -74.0062},
]

coords = [
    (emergency['lat'], emergency['lon']) for emergency in emergencies
]

# for coord1 in coords:
#     for coord2 in coords:
#         if coord1 != coord2:
            # print(geodesic(coord1, coord2).kilometers)