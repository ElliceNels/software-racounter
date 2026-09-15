import json
from datetime import datetime
import matplotlib.pyplot as plt

with open("eva-data.json", "r", encoding="utf-8") as file:
    eva_data = json.load(file)

countries = set()
records = []

for eva in eva_data:
    date_text = eva.get("date")
    duration_text = eva.get("duration")
    country = eva.get("country")

    if not date_text or not duration_text or not country:
        continue

    date = datetime.fromisoformat(date_text)
    hours, minutes = map(int, duration_text.split(":"))
    duration_hours = hours + minutes / 60

    countries.add(country)
    records.append((date, duration_hours, country))

records.sort(key=lambda record: record[0])

def aggregate_data(desired_country):
    dates = []
    cumulative_hours = []
    total_hours = 0

    for date, duration_hours, stored_country in records:
        if (desired_country == "all countries") or (stored_country == desired_country):
            total_hours += duration_hours
            dates.append(date)
            cumulative_hours.append(total_hours)

    return dates, cumulative_hours

def plot_graph(country_name, x, y):
    plt.plot(x, y)
    plt.xlabel("Year")
    plt.ylabel(f"Cumulative EVA duration (hours) {country_name}")
    plt.tight_layout()
    plt.savefig(f"cumulative_duration_{country_name}.png")
    plt.show()

country = input("Enter country (Or nothing for all countries):")
country = country.strip() if country.strip() in countries else "all countries"
x, y = aggregate_data(country)
plot_graph(country, x, y)
