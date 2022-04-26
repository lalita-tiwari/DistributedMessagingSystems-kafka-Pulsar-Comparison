import pulsar
from json import dumps

# install requests package to call open weather API
import requests
from time import sleep

# registered into the weather API to call and get weather data for the city
# upon registration below API Key was assigned which is essential to call API
# Key=API_KEY

client = pulsar.Client('pulsar://129.114.25.142:6650')

while True:
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q=dallas&appid=cd3d379097b72bb4333cd41f6d499313")
    print(response.json())


    #create topic weather
    producer = client.create_producer('weather')

    producer.send('weather', value=response.json())
    producer.flush()
    sleep(60)
