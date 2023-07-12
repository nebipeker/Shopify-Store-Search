import requests
from bs4 import BeautifulSoup
import re

def search_shopify_stores(query, num_results=10):
    search_url = f"https://www.google.com/search?q={query}+site:.store"
    output_file = "urls.txt"

    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = soup.select("div.g")
            print(f"Search results for '{query}':")
            with open(output_file, "w") as file:
                count = 0
                for result in search_results:
                    link_element = result.select_one("a")
                    if link_element:
                        link = link_element["href"]
                        store_url = extract_shopify_store_url(link)
                        if store_url:
                            count += 1
                            print(f"Result {count}:")
                            print(f"Store URL: {store_url}")
                            file.write(store_url + "\n")
                            print("-" * 20)
                            if count >= num_results:
                                break
            print(f"Shopify store URLs saved to '{output_file}'.")
        else:
            print(f"Failed to search Shopify stores. Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while sending the request: {e}")

def extract_shopify_store_url(google_link):
    match = re.search(r"https?://([^/?]+).*", google_link)
    if match:
        return match.group(0)
    return None

# Example usage
search_query = "fashion"  # The query to search Shopify stores
num_results = 5  # Number of results to retrieve (adjust as needed)
search_shopify_stores(search_query, num_results)
