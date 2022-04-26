import pulsar
  
client = pulsar.Client('pulsar://129.114.25.142:32710')
consumer = client.subscribe('weather', 'my-subscription')

while True:
    msg = consumer.receive()
    try:
        print("Received message '{}'".format(msg.data()))
        # Acknowledge successful processing of the message
        consumer.acknowledge(msg)
    except Exception:
        # Message failed to be processed
        consumer.negative_acknowledge(msg)

client.close()
