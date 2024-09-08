from kafka import KafkaConsumer
import threading
import csv
import time
import shared

def create_consumer(entity_name):
    # Open a CSV file for appending
    with open(f'{entity_name}.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        
        # Check if the file is empty to write a header row
        if file.tell() == 0:
            writer.writerow(['timestamp', 'data'])

        consumer = KafkaConsumer(
            entity_name,
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            group_id=f'group_{entity_name}'
        )

        for message in consumer:
            data = message.value.decode('utf-8')
            print(f"{entity_name} message: {data}")
            # Write the message to the CSV file
            writer.writerow([data])
            # Flush data to the CSV file
            file.flush()

entities = ['apple_fetch', 'tesla_fetch', 'alphabet_fetch', 'microsoft_fetch', 'amazon_fetch', 'meta_fetch', 'nvidia_fetch']

# Create and start a thread for each consumer
for entity in entities:
    consumer_thread = threading.Thread(target=create_consumer, args=(entity,))
    consumer_thread.start()

while True:
    shared.set_flag(True)
    time.sleep(86400)
