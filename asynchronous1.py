import argparse
import asyncio
import aiohttp
from datetime import datetime

# Set up command-line arguments
parser = argparse.ArgumentParser(description='Display sports results from API')
parser.add_argument('--event', '-e', help='Filter by event type')
parser.add_argument('--locale', '-l', default='en', help='Set the locale')
args = parser.parse_args()

async def fetch_results():
    async with aiohttp.ClientSession() as session:
        async with session.post('https://restest.free.beeceptor.com/results') as response:
            return await response.json()

async def display_results():
    results = await fetch_results()

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

if __name__ == '__main__':
    asyncio.run(display_results())
