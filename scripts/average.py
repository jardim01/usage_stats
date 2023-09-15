import json

DATA_PATH = "./data.json"


def load_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)


data = load_data()
day_count = 0
total = 0
for day in dict(data).values():
    day_count += 1
    total += day["total"]

avg = total / day_count

print(f"Average for the last {day_count} days: {avg / 60 / 60} hours")
