from kafka import KafkaConsumer
from json import loads
#import couchdb

#couch = couchdb.Server('http://User_ID:User_Password@129.114.25.124:5984/')

#db = couch['weather']

consumer = KafkaConsumer(
    'weather', bootstrap_servers=['129.114.25.142:30488'],
    auto_offset_reset='earliest', enable_auto_commit=True,
    group_id='0', value_deserializer=lambda x: loads(x.decode('utf-8')))

print("Inside Consumer")
# consumer.poll(timeout_ms=6000)
for message in consumer:
    message = message.value
    print(message)
