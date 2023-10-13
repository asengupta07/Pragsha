from wsm import calc_score

DUMMY_AGENCIES = [
    {
        "name": "Agency 1",
        "equipment": {
            "firefighting": 5,
            "medical": 23,
            "food": 12,
            "shelter": 8,
            "search": 15,
            "ppe": 9,
            "transport": 6,
            "communication": 17,
        },
        "proximity": 4,
    },
    {
        "name": "Agency 2",
        "equipment": {
            "firefighting": 7,
            "medical": 18,
            "food": 14,
            "shelter": 6,
            "search": 10,
            "ppe": 12,
            "transport": 9,
            "communication": 11,
        },
        "proximity": 3,
    },
    {
        "name": "Agency 3",
        "equipment": {
            "firefighting": 8,
            "medical": 21,
            "food": 13,
            "shelter": 7,
            "search": 16,
            "ppe": 10,
            "transport": 5,
            "communication": 14,
        },
        "proximity": 2,
    },
    {
        "name": "Agency 4",
        "equipment": {
            "firefighting": 6,
            "medical": 20,
            "food": 15,
            "shelter": 9,
            "search": 12,
            "ppe": 8,
            "transport": 7,
            "communication": 13,
        },
        "proximity": 5,
    },
    {
        "name": "Agency 5",
        "equipment": {
            "firefighting": 10,
            "medical": 19,
            "food": 11,
            "shelter": 4,
            "search": 14,
            "ppe": 12,
            "transport": 8,
            "communication": 16,
        },
        "proximity": 6,
    },
    {
        "name": "Agency 6",
        "equipment": {
            "firefighting": 9,
            "medical": 22,
            "food": 16,
            "shelter": 5,
            "search": 11,
            "ppe": 13,
            "transport": 7,
            "communication": 15,
        },
        "proximity": 7,
    },
    {
        "name": "Agency 7",
        "equipment": {
            "firefighting": 12,
            "medical": 17,
            "food": 13,
            "shelter": 7,
            "search": 9,
            "ppe": 11,
            "transport": 6,
            "communication": 18,
        },
        "proximity": 4,
    },
    {
        "name": "Agency 8",
        "equipment": {
            "firefighting": 11,
            "medical": 23,
            "food": 12,
            "shelter": 8,
            "search": 15,
            "ppe": 10,
            "transport": 5,
            "communication": 17,
        },
        "proximity": 5,
    },
    {
        "name": "Agency 9",
        "equipment": {
            "firefighting": 5,
            "medical": 20,
            "food": 15,
            "shelter": 9,
            "search": 12,
            "ppe": 8,
            "transport": 7,
            "communication": 13,
        },
        "proximity": 3,
    },
    {
        "name": "Agency 10",
        "equipment": {
            "firefighting": 7,
            "medical": 18,
            "food": 14,
            "shelter": 6,
            "search": 10,
            "ppe": 12,
            "transport": 9,
            "communication": 11,
        },
        "proximity": 2,
    },
    {
        "name": "Agency 11",
        "equipment": {
            "firefighting": 8,
            "medical": 21,
            "food": 13,
            "shelter": 7,
            "search": 16,
            "ppe": 10,
            "transport": 5,
            "communication": 14,
        },
        "proximity": 6,
    },
]


def test():
    calc_score("avalanche", DUMMY_AGENCIES)
    for agency in DUMMY_AGENCIES:
        print(agency["name"], agency["score"])


if __name__ == "__main__":
    test()