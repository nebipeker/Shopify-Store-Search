import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
import pika

def search_shopify_stores(query, num_results=10):
    search_url = f"https://www.google.com/search?q={query}+site:.store"
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='shopify')
    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = soup.select("a")
            print(f"Search results for '{query}':")
            for result in search_results:
                link = result.get("href")
                if link and link.startswith("/url?q="):
                    store_url = extract_shopify_store_url(link)
                    if store_url:
                        count += 1
                        print(f"Result {count}:")
                        print(f"Store URL: {store_url}")
                        channel.basic_publish(exchange='',
                        routing_key='shopify',
                        body=store_url)
                        print("-" * 20)
                        if count >= num_results:
                            connection.close()
                            break
            print(f"Shopify store URLs saved to '{output_file}'.")
        else:
            print(f"Failed to search Shopify stores. Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while sending the request: {e}")

def extract_shopify_store_url(link):
    match = re.search(r"/url\?q=(https?://[^&]+)", link)
    if match:
        url = match.group(1)
        return unquote(url)
    return None

# Example usage
search_query = "fashion"  # The query to search Shopify stores
num_results = 5000  # Number of results to retrieve (adjust as needed)
search_shopify_stores(search_query, num_results)
