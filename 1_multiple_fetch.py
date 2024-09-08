import requests
import time
from kafka import KafkaProducer
import json

# Set up a Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Define a function to fetch data from an API and publish it to a Kafka topic
def fetch_and_publish(entity, api_url, topic):
    response = requests.get(api_url)
    data = response.json()
    producer.send(topic, value=data)
    producer.flush()
    print(f"Published {entity} data: {data}")

# URLs for fetching data
# URLs for fetching data
urls = {
    'apple_fetch': 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=YOUR_API_KEY',
    'tesla_fetch': 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=TSLA&apikey=YOUR_API_KEY',
    'alphabet_fetch': 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=GOOGL&apikey=YOUR_API_KEY',
    'microsoft_fetch': 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=MSFT&apikey=YOUR_API_KEY',
    'amazon_fetch': 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AMZN&apikey=YOUR_API_KEY',
    'sp500_fetch': 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=SPY&apikey=YOUR_API_KEY',
    'meta_fetch': 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=FB&apikey=YOUR_API_KEY',  # Meta
    'nvidia_fetch': 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=NVDA&apikey=YOUR_API_KEY'  # Added NVIDIA
}

# urls = {
#     'apple_fetch': 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=YOUR_API_KEY',
#     'tesla_fetch': 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=TSLA&apikey=YOUR_API_KEY',
# }

while True:
    # Fetch and publish data for each entity
    for entity, url in urls.items():
        fetch_and_publish(entity, url, entity)
        print(f"Started fetching and publishing data for {entity}")

    # Wait for 24 hours (86400 seconds) before the next round of fetching and publishing
    time.sleep(86400)
