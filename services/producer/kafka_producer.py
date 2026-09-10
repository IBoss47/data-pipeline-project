import pandas as pd
import json
import time
import argparse
from confluent_kafka import Producer

def delivery_report(err, msg):
    """
    This is a callback function. Every time kafka receives our message,
    it triggers this function to let we know if it succeeded or failed.
    """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivery to {msg.topic()} [{msg.partition()}]')

def produce_from_csv(file_path, topic, broker='localhost:9092'):
    # Set up the kafka producer connection
    conf = {'bootstrap.servers' : broker}
    producer = Producer(conf)

    # Read the CSV files
    chunk = 100
    for chunk in pd.read_csv(file_path, chunksize = chunk):

        chunk['ts'] = pd.to_datetime(chunk['ts']).dt.strftime('%Y-%m-%d %H:%M:%S')
        for index, row in chunk.iterrows():
            record = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}
            json_data = json.dumps(record)

            producer.poll(0)

            producer.produce(
                topic = topic,
                value = json_data.encode('utf-8'),
                callback = delivery_report
            )

            time.sleep(1)

    producer.flush()
    print('Finished producing messages.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Stream CSV data to Kafka')
    parser.add_argument('--file', required = True, help = 'Path to the CSV file')
    parser.add_argument('--topic', required = True, help = 'Kafka topic to publish to')
    parser.add_argument('--broker', default = 'localhost:9092', help = 'Kafka broker address')

    args = parser.parse_args()
    produce_from_csv(
        file_path = args.file,
        topic = args.topic,
        broker = args.broker
    )
