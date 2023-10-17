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

EW = {
    "firefighting": {
        "Fire Extinguishers": 9,
        "Fire Hoses and Nozzles": 6,
        "Fire Hydrant Wrenches": 4,
        "Wildland Firefighting Tools": 5,
    },
    "medical": {
        "Defibrillators": 7,
        "Medical Kits and Supplies": 9,
        "Oxygen Tanks and Masks": 8,
        "Triage Kits": 6,
        "Stretchers and Backboards": 5,
        "Airway Management Equipment": 6,
    },
    "food": {
        "Non-Perishable Food Items": 9,
        "Water Bottles or Water Purification Systems": 10,
        "Food Preparation and Cooking Equipment": 6,
    },
    "shelter": {
        "Tents and Shelters": 9,
        "Sleeping Bags and Blankets": 8,
        "Tarps and Plastic Sheeting": 7,
        "Portable Toilets and Sanitation Kits": 8,
    },
    "search": {
        "First Aid Kits": 9,
        "Stretchers": 7,
        "Shovels and Picks": 6,
        "Flashlights and Headlamps": 8,
        "Life Vests and Personal Flotation Devices": 7,
        "Rope and Harnesses": 7,
        "Hydraulic Rescue Tools": 5,
    },
    "ppe": {
        "Helmets": 8,
        "Gloves": 9,
        "Respirators and Masks": 9,
        "Hazmat Suits": 6,
        "Safety Goggles": 7,
    },
    "transport": {
        "Emergency Vehicles": 9,
        "Boats and Watercraft": 8,
        "Helicopters and Aircraft": 7,
    },
    "communication": {
        "GPS Devices": 8,
        "Topographic Maps": 7,
        "Compasses": 6,
        "Two-Way Radios": 9,
        "Satellite Phones": 9,
        "Cell Phone Signal Boosters": 7,
    },
}


def hash_type(type):
    return TYPE.index(type)


def hash_equipment(equipment):
    return EQUIPMENT.index(equipment)


def get_weight(type, equipment):
    return WEIGHT[hash_type(type)][hash_equipment(equipment)]


def sigmoid(x):
    return x


def score(type, agency, proximity):
    s = 0
    for equipment in EQUIPMENT:
        if equipment in agency:
            s += agency[equipment] * (get_weight(type, equipment) / 2)
    s += proximity * PROXIMITY

    # Apply the sigmoid function to the final score
    final_score = sigmoid(s)
    return final_score


def calc_score(type, agencies):
    for agency in agencies:
        agency["score"] = score(type, agency["equipment"], agency["proximity"])
    agencies.sort(key=lambda x: x["score"], reverse=True)
    return agencies


def calc(agency, type):
    
