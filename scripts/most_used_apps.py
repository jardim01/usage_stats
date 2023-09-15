import json
import os


DATA_PATH = "./data.json"


def load_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)


data = load_data()
day_count = 0

usage = {}
for day in dict(data).values():
    day_count += 1
    for key, time in dict(day["apps"]).items():
        if not (key in usage):
            usage[key] = 0
        usage[key] += time

sorted_usage = dict(
    sorted(usage.items(), key=lambda item: item[1], reverse=True))

print(f"Showing stats for the last {day_count} days")

top_count = 10
for key, value in list(sorted_usage.items())[:top_count]:
    total_hours = value/60/60
    hours_per_day = total_hours/day_count
    app_name = os.path.basename(key)
    print(f"{app_name} -> {total_hours:.0f} total hours, {hours_per_day:.2f} hours per day")
