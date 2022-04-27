# DistributedMessagingSystems-kafka-Pulsar-Comparison

### This Directory contains code to comapre the two distributed messaging systems Apache Kafka and Apache Pulsar
### Testing is done on one single node kubernetes cluster on a private cloud instance by depoying the Kafka and Pulsar as pods

## Deploying the Apache kafka and zookeeper as pods on Kubernetes using docker images
follow the below steps :


    - Login to your docker account to build and push the kafka and zookeeper images
    docker login
    
    - Build the kafka docker image
    docker build -f kafka-dockerfile -t lalitatiwari/kafka .
    
    - push the image
     docker push lalitatiwari/kafka
     
    - Build the zookeeper docker image
    docker build -f Dockerfile -t lalitatiwari/zookeeper .
    
    - push the image
    docker push lalitatiwari/zookeeper
   
    - create kafka namespace
    kubectl apply -f  kafka-namespace.yml 
   
    - deploy zookeeper
     kubectl apply -f  zookeeper.yml
    
    - deploy kafka service
    kubectl apply -f  kafka-service.yml
   
    - deploy kafka (update the external kafka port in this yml file)
    kubectl apply -f kafka.yml
    
  ![Screen Shot 2022-04-25 at 9 05 31 PM](https://user-images.githubusercontent.com/83514861/165204936-74ee9c34-467a-4694-9a20-12f8e8db9d4b.png)

    - To create a kafka topic from inside a pod
        kubectl exec -it kafka-deployment-6ffc7d5989-8dgw4 /bin/bash -n kafka (update your kafka pod id)
        cd kafka/
        bin/kafka-topics.sh --create --topic weather --bootstrap-server localhost:9092 
    
    
    - To run the kafka install below kafka-python package
        pip3 install kafka-python
        
    - Run the producer-kafka.py from the client
        python3 producer-kafka.py 
        
    - Run the consumer-kafka.py from the remote host where you have deployed your kafka 
        python3 consumer-kafka.py 
        
    - To run the pulsar producer from client install the below package
        pip install pulsar-client==2.10.0
        
    - Run the producer-pulsar.py from the client
       python3 producer-pulsar.py
        
   
     
