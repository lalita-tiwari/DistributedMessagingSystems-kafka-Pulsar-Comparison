# DistributedMessagingSystems-kafka-Pulsar-Comparison

### This Directory contains code to comapre the two distributed messaging systems Apache Kafka and Apache Pulsar
### Testing is done on one single node kubernetes cluster on a private cloud instance by depoying the Kafka and Pulsar as pods.

### Step 0: Prepare a Kubernetes cluster befor deploying Kafka and Pulsar


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
        
        
   
## Deploying Apache Pulsar on kubernetes 
     
### Step 1: Install Pulsar Helm chart

 - Add Pulsar charts repo.

        - helm repo add apache https://pulsar.apache.org/charts

        - helm repo update

 - Clone the Pulsar Helm chart repository.

git clone https://github.com/apache/pulsar-helm-chart
cd pulsar-helm-chart


- Run the script prepare_helm_release.sh to create secrets required for installing the Apache Pulsar Helm chart. The username pulsar and password pulsar are used for logging into the Grafana dashboard and Pulsar Manager.

./scripts/pulsar/prepare_helm_release.sh \
    -n pulsar \
    -k pulsar-mini \
    -c


- Use the Pulsar Helm chart to install a Pulsar cluster to Kubernetes.

Note 
You need to specify --set initialize=true when installing Pulsar the first time. This command installs and starts Apache Pulsar.
helm install \
    --values examples/values-minikube.yaml \
    --set initialize=true \
    --namespace pulsar \
    pulsar-mini apache/pulsar


- Check the status of all pods.

        - kubectl get pods -n pulsar

- If all pods start up successfully, you can see that the STATUS is changed to Running or Completed.

        
![Screen Shot 2022-04-29 at 8 30 48 PM](https://user-images.githubusercontent.com/83514861/166085357-7d51db79-9706-4e27-903d-8c3c78fcc1d7.png)


- Check the status of all services in the namespace pulsar.

        - kubectl get services -n pulsar
       
![Screen Shot 2022-04-29 at 8 31 56 PM](https://user-images.githubusercontent.com/83514861/166085386-4fbe0c30-4b76-4e20-a13c-2ce26de837ce.png)

## steps to run pulsar client

    -  To run the pulsar producer from client install the below package
        pip install pulsar-client==2.10.0
        
    -  Run the producer-pulsar.py from the client
       python3 producer-pulsar.py

## steps to install Grafana
    - docker pull grafana/grafana-oss
    - docker run -d -p 3000:3000 --name grafana grafana/grafana-oss
 
 ## steps to install prometheus for kafka
    - check the prometheus-kafka.yaml file (update the kafka pods IP's [kubectl get pods -n kafka -o wide])
     - docker run -d --name my-prometheus2 --mount type=bind,source=/home/cc/kafka/prometheus.yml,destination=/etc/prometheus/prometheus.yml --publish    published=9195,target=9090,protocol=tcp prom/prometheus


