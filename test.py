import json

transaction = {
    "id": "2353",
    "asin": "asin",
    "mercariId": "mercariId",
    "changeDetails":{}
}

transaction["changeDetails"]["add"] = {
    "a": 0,
    "b": 0
}

print(transaction)