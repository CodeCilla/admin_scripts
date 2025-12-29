import requests
from bs4 import BeautifulSoup
import queue
import re
import time
import random
import csv

# to store the URLs discovered to visit
# in a specific order
urls = queue.PriorityQueue()
# high priority
urls.put((0.5, "https://www.mobilitix.fr/fr/"))

# to store the pages already visited
visited_urls = []
saved_urls = []

# until all pages have been visited
while not urls.empty():
    # get the page to visit from the list
    _, current_url = urls.get()

    # crawling logic
    try:
        response = requests.get(current_url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        print(f"Traitement de : {current_url}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de {current_url} : {e}")
        continue

    visited_urls.append(current_url)

    link_elements = soup.select("a[href]")
    for link_element in link_elements:
        url = link_element['href']

        # any of its subdomains
        if re.match(r"https://(?:.*\.)?mobilitix\.fr", url):
            # if the URL discovered is new
            if url not in visited_urls and url not in [item[1] for item in urls.queue] and url not in saved_urls:
                # low priority
                priority_score = 1
                urls.put((priority_score, url))
                print(url)
                saved_urls.append(url)  # Add the URL to saved_urls



    # pause the script for a random delay
    # between 1 and 3 seconds
    time.sleep(0.5)

# Write URLs to a CSV file
with open("urls.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["url"])  # En-tête du CSV
    for url in saved_urls:
        writer.writerow([url])

print("Le script a terminé. Les URLs ont été enregistrées dans urls.csv.")

print(f"Nombre d'URLs trouvées : {len(saved_urls)}")



