import requests

def register_site_data(url):
    api_url = "http://localhost:5000/shopify/collections"  # Replace with your API URL

    # Prepare the payload with the URL parameter
    payload = {"site": url}

    try:
        response = requests.get(api_url, params=payload)
        if response.status_code == 200:
            collections = response.json()
            print(f"Site data registered successfully for {url}. Collections: {collections}")
            for collection in collections:
                register_products(url, collection)  # Register products for each collection
        else:
            print(f"Failed to register site data for {url}. Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while sending the request: {e}")

def register_products(url, collection):
    api_url = f"http://localhost:5000/shopify/collections/{collection}/products"  # Replace with your API URL

    # Prepare the payload with the URL parameter
    payload = {"site": url}

    try:
        response = requests.get(api_url, params=payload)
        if response.status_code == 200:
            products = response.json()
            print(f"Products registered successfully for {url}, collection: {collection}. Products: {products}")
        else:
            print(f"Failed to register products for {url}, collection: {collection}. Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while sending the request: {e}")

# Read URLs from a text file
def read_urls_from_file(file_path):
    with open(file_path, "r") as file:
        urls = [line.strip() for line in file]
    return urls

# Example usage
file_path = "urls.txt"  # Path to the text file containing URLs
urls = read_urls_from_file(file_path)

for url in urls:
    register_site_data(url)
