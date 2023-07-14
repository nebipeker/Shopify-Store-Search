import re
import pika
from googlesearch import search
import time

def search_shopify_stores(query, num_results=10):
    search_query = f"{query} site:.store"
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='shopify')
    try:
        count = 0  # Initialize count
        print(f"Search results for '{query}':")
        for result in search(search_query, num_results=num_results,  sleep_interval=45):
            store_url = extract_shopify_store_url(result)
            store_url = store_url.split(".store", 1)[0] + ".store"
            if store_url:
                count += 1
                print(f"Result {count}:")
                print(f"Store URL: {store_url}")
                channel.basic_publish(exchange='',
                                      routing_key='shopify',
                                      body=store_url)
                print("-" * 20)
                if count >= num_results:
                    break  # Break the loop when reaching desired results
        connection.close()  # Close the connection after the loop
    except Exception as e:
        print(f"Error occurred while searching Shopify stores: {e}")


def extract_shopify_store_url(url):
    match = re.search(r"https?://[^&]+", url)
    if match:
        return match.group(0)
    return None


# Example usage
#time.sleep(1000)
search_query = "tech"  # The query to search Shopify stores
num_results = 15000  # Number of results to retrieve (adjust as needed)
search_shopify_stores(search_query, num_results)
