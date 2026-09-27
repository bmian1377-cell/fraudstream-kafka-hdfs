import pandas as pd
from kafka import KafkaProducer
import json
import time

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'transactions'
CSV_PATH = '../data/creditcard.csv'
SAMPLE_SIZE = 2000  # shuru mein chhota sample

# CSV read karo (sirf pehli SAMPLE_SIZE rows)
df = pd.read_csv(CSV_PATH, nrows=SAMPLE_SIZE)

print(f"Streaming {len(df)} rows to topic '{TOPIC_NAME}'...")

for index, row in df.iterrows():
    record = row.to_dict()
    producer.send(TOPIC_NAME, value=record)
    
    if index % 100 == 0:
        print(f"Sent row {index}")
    
    time.sleep(0.01)  # thoda delay, real-time streaming jaisa feel dene ke liye

producer.flush()
print("Done! All rows sent.")