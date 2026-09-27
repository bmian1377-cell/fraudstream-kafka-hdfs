from kafka import KafkaConsumer
from hdfs import InsecureClient
import json

TOPIC_NAME = 'transactions'
HDFS_URL = 'http://localhost:9870'
HDFS_USER = 'bilawal'
HDFS_DIR = '/fraudstream/transactions'
BATCH_SIZE = 100  # itni rows ikatthi kar ke ek file mein likhenge

# Kafka consumer setup
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # topic ke shuru se sab messages padho
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    consumer_timeout_ms=10000  # 10 sec tak koi naya message na aaye to consumer ruk jaye
)

# HDFS client setup
hdfs_client = InsecureClient(HDFS_URL, user=HDFS_USER)

batch = []
file_counter = 0

print(f"Listening to topic '{TOPIC_NAME}'...")

for message in consumer:
    batch.append(message.value)
    
    if len(batch) >= BATCH_SIZE:
        file_counter += 1
        filename = f'{HDFS_DIR}/batch_{file_counter}.json'
        
        with hdfs_client.write(filename, encoding='utf-8') as writer:
            for record in batch:
                writer.write(json.dumps(record) + '\n')
        
        print(f"Wrote {len(batch)} records to {filename}")
        batch = []

# Agar loop khatam hone ke baad kuch records bache ho (batch incomplete)
if batch:
    file_counter += 1
    filename = f'{HDFS_DIR}/batch_{file_counter}.json'
    with hdfs_client.write(filename, encoding='utf-8') as writer:
        for record in batch:
            writer.write(json.dumps(record) + '\n')
    print(f"Wrote {len(batch)} records to {filename}")

print(f"Done! Total {file_counter} files written to HDFS.")