# DistributedMessagingSystems-kafka-Pulsar-Comparison

### This Directory contains code to comapre the two distributed messaging systems Apache Kafka and Apache Pulsar

### To perform the comparison, the testing is done on three separate Kubernetes cluster nodes created on Google Cloud Platform (GCP) cloud.

On first Kubernetes cluster node, three replicas of kafka are deployed as docker pods along with one zookeeper, Grafana and Prometheus pods. 

On second Kubernetes cluster node, three replicas of each Pulsar bookie, Pulsar broker and zookeeper along with, Grafana and Prometheus are 
deployed as docker pods.

On third Kubernetes cluster node, to understand how these two MQs handle the high load data the clients for both kafka and pulsar deployed and running as docker pods. I’m running 5 publishers and 1 consumer pods for both kafka and pulsar. The client is using a weather APT data to send. 
Clients for both kafka and pulsar using the exact same payload and disseminating with the same frequency. 

### GitHub Link to the CLI Tool to install the Kubernetes cluster, it can save some time.
https://github.com/lalita-tiwari/faas-cli-OpenFaas-OpenWhisk-ServerlessFrameworks-viaAnsiblePlaybooks.git


### Step 0: Prepare a Kubernetes cluster befor deploying Kafka and Pulsar


## Deploying the Apache kafka and zookeeper as pods on Kubernetes using docker images
follow the below steps :


    - Login to your docker account to build and push the kafka and zookeeper images![Screen Shot 2022-05-04 at 12 47 47 AM](https://user-images.githubusercontent.com/83514861/166628624-d73c4d21-a244-47de-8df5-c0bc4d016d14.png)

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
    
   ![Screen Shot 2022-05-02 at 1 33 20 PM](https://user-images.githubusercontent.com/83514861/166304916-d26847a1-89fa-43ff-a8bb-f8cf7b91c333.png)

 
    - To create a kafka topic from inside a pod
        kubectl exec -it kafka-deployment-6ffc7d5989-8dgw4 /bin/bash -n kafka (update your kafka pod id)
        cd kafka/
        bin/kafka-topics.sh --create --topic weather --bootstrap-server localhost:9092 
        
        If you get error (java.net.BindException: Address already in use) while creating a topic from within a kafka pod,
        use below commands:
            - unset JMX_PORT
            - unset KAFKA_OPTS
    
    
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

![Screen Shot 2022-05-04 at 12 47 47 AM](https://user-images.githubusercontent.com/83514861/166628647-18bc4d4d-5221-4552-b29f-f4d4d7eaf549.png)

- Check the status of all services in the namespace pulsar.

        - kubectl get services -n pulsar
  ![Screen Shot 2022-05-04 at 12 49 21 AM](https://user-images.githubusercontent.com/83514861/166628730-29f56be6-68ee-44d1-97d4-5c22fb22a6c1.png)


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


