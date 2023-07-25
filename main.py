import requests
import time

mainN = input("Please input main nation: ")
length = int(input("Please input how far in time you want to go back in days: "))
names = []
rates_of_change = []
version = 1.2
headers = {
    "User-Agent": f"Top 100 RoC/{version} (developer: https://github.com/Thorn1000 ; user:{mainN};)"
}
# Send requests and collect names
for page in range(5):
    start = 1 + (page * 20)
    url = f"https://www.nationstates.net/cgi-bin/api.cgi?q=censusranks&scale=86&start={start}"
    response = requests.get(url, headers= headers)
    data = response.text

    # Extract names from the response
    nation_tags = data.split("<NAME>")[1:]
    for tag in nation_tags:
        name = tag.split("</NAME>")[0]
        names.append(name)

    print(f"Collected names: {len(names)}/{100}")
    time.sleep(0.65)

print("Name collection completed.\n")

# Calculate rates of change
current_time = int(time.time())
from_time = current_time - length * 24 * 60 * 60
for i, name in enumerate(names, 1):
    url = f"https://www.nationstates.net/cgi-bin/api.cgi?nation={name};q=census;scale=86;mode=history;from={from_time}"
    response = requests.get(url, headers= headers)
    data = response.text

    # Extract timestamps and scores from the response
    timestamp_tags = data.split("<TIMESTAMP>")[1:]
    score_tags = data.split("<SCORE>")[1:]
    timestamps = [int(tag.split("</TIMESTAMP>")[0]) for tag in timestamp_tags]
    scores = [float(tag.split("</SCORE>")[0]) for tag in score_tags]

    # Find highest and lowest timestamps
    max_timestamp = max(timestamps)
    min_timestamp = min(timestamps)

    # Find corresponding scores
    max_score = scores[timestamps.index(max_timestamp)]
    min_score = scores[timestamps.index(min_timestamp)]

    # Calculate rate of change
    rate_of_change = round((max_score - min_score)/length,2)
    rates_of_change.append((i, name, rate_of_change))

    print(f"Processed: {i}/{len(names)}")
    time.sleep(0.65)

print("Processing completed.\n")

# Sort rates of change
rates_of_change.sort(key=lambda x: x[0])

# Print results
print("Results:")
for i, (num, name, roc) in enumerate(rates_of_change, 1):
    print(f"{i}/{len(names)} {name} | Rate of Change: {roc}")

fastest_growing = sorted(rates_of_change, key=lambda x: x[2], reverse=True)[:20]
most_lost = sorted(rates_of_change, key=lambda x: x[2], reverse=False)[:20]
# Print fastest growing players
print("\nFastest Growing Players:")
for i, (num, name, roc) in enumerate(fastest_growing, 1):
    print(f"{i}. {name} | Rate of Change: {roc}")

# Print fastest falling players
print("\nFastest falling Players:")
for i, (num, name, roc) in enumerate(most_lost, 1):
    print(f"{i}. {name} | Rate of Change: {roc}")
