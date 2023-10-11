TYPE = [
    "landslide",
    "earthquake",
    "avalanche",
    "flood",
    "fire",
    "drought",
    "accident",
    "medical",
    "weather",
    "tsunami",
]
EQUIPMENT = [
    "firefighting",
    "medical",
    "food",
    "shelter",
    "search",
    "ppe",
    "transport",
    "communication",
]
WEIGHT = [
    [5, 8.5, 8, 7.5, 10, 7.5, 9.5, 9],
    [9.5, 8, 8, 8, 9, 10, 8.5, 8.5],
    [0, 8.5, 8, 8.5, 10, 9.5, 9, 9],
    [3, 9, 9, 9, 9.5, 2, 10, 10],
    [10, 9, 8.5, 8.5, 9, 10, 9.5, 9.5],
    [5, 9, 10, 7, 0, 0, 9.5, 9],
    [9, 10, 8, 9, 10, 9, 10, 10],
    [0, 10, 10, 10, 0, 0, 10, 10],
    [5, 9.5, 8.5, 9, 10, 8, 9.5, 9.5],
    [7, 9, 9, 9, 9.5, 0, 10, 10],
]
PROXIMITY = -25


def hash_type(type):
    return TYPE.index(type)


def hash_equipment(equipment):
    return EQUIPMENT.index(equipment)


def get_weight(type, equipment):
    return WEIGHT[hash_type(type)][hash_equipment(equipment)]


def score(type, agency, proximity):
    s = 0
    for equipment in EQUIPMENT:
        if equipment in agency:
            s += agency[equipment] * (get_weight(type, equipment) / 2)
    s += proximity * PROXIMITY
    return s


def calc_score(type, agencies):
    for agency in agencies:
        agency["score"] = score(type, agency["equipment"], agency["proximity"])
    agencies.sort(key=lambda x: x["score"], reverse=True)
    return agencies
