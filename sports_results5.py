import argparse
import requests
from datetime import datetime

# Set up command-line arguments
parser = argparse.ArgumentParser(description='Display sports results from API')
parser.add_argument('--event', '-e', help='Filter by event type')
parser.add_argument('--locale', '-l', default='en', help='Set the locale')
args = parser.parse_args()

# Send a POST request to the API endpoint
response = requests.post('https://restest.free.beeceptor.com/results')

# Parse the JSON response
results = response.json()

results_list = []

# Append each result to the results_list
for sport, sport_results in results.items():
    for result in sport_results:
        result['sport'] = sport
        if not args.event or result['sport'] == args.event:
            results_list.append(result)

# Sort the results_list by publicationDate in reverse chronological order
results_list.sort(key=lambda r: datetime.strptime(r['publicationDate'], '%b %d, %Y %I:%M:%S %p'), reverse=True)

# Display the results
for result in results_list:
    if 'publicationDate' in result and 'tournament' in result and 'winner' in result:
        print(f"{result['publicationDate']} - {result['tournament']} - {result['winner']}")
    elif 'publicationDate' in result and 'tournament' in result and 'winner1' in result and 'winner2' in result:
        print(f"{result['publicationDate']} - {result['tournament']} - {result['winner1']} vs {result['winner2']}")
    else:
        print("Incomplete result data.")
