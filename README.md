# Scraper Service

This application grab the HTTP GET code of a given url and expose Prometheus metrics collecting at the endpoint **/metrics**. 

In the project you can find:
- **Src folder**: With the code of the python app and requirements file.
- **Dockerile**: To create a docker image with the python app.
- **Tests Folder**: With functional tests
- **k8s Folder**: With the files to run the app in a kubernetes cluster, in addition to Prometheus and Grafana.
- **Prometheus and Grafana folder**: With a Docker-compose file to deploy Prometheus and Grafana locally, in addition to
some config files of both applications.
- **Request-script folder**: With a script to make regular scraping requests to the service, in addition to a file with a list of urls.

## Deploying Application for testing locally

1. Clone repository

```
git clone https://github.com/leandropremar/scraper-service.git
cd scraper-service
```

2. Install requirements

```
pip3 install -r src/requirements.txt 
```

3. Run the application (you will need to have Python 3.9 installed)

```
python3 src/scraper_service.py  
```

4. If you open your browser, you will be able to see the server running in [http://localhost:8080](http://localhost:8080).
In order to access to the metrics, they will be available in [http://localhost:9095/metrics](http://localhost:9095/metrics)

5. Close application

```
Ctrl + c
```

## Building The Container Image 


1. Build the Docker image (You will need to have Docker installed) with the Dockerfile 

```
docker build -t scraper-service .
```

2. Run the application and check if it is working properly 

```
docker run -d -p 8080:8080 -p 9095:9095 --name scraper-service scraper-service
```

Once you have executed the above command, If you open your browser, you will be able to see the server running in [http://localhost:8080](http://localhost:8080).
In order to access to the metrics, they will be available in [http://localhost:9095/metrics](http://localhost:9095/metrics)

3. If you want, you can create new repository on **DockerHub** or another docker registry and push the image

```
docker login
```
```
docker tag scraper-service:latest [USERNAME]/scraper-service:latest
docker push [USERNAME]/scraper-service:latest
```

4. If you don't want to build a new docker image, you can find a public image in my **DockerHub** account

```
docker pull leandrofreila/scraper-service
```

## Deploying Prometheus and Grafana locally

In the path **goods-to-have/prometheus-and-grafana**, you will find a docker-compose file to run Prometheus and 
Grafana applications locally.

In order to configure Prometheus application, there is a config file (**prometheus.yml**)with the following parameters:

   - **scrape_interval**: How frequently to scrape targets, with a value of 5s
   - **metrics_path**:  The HTTP resource path on which to fetch metrics from targets, with value "/metrics"
   - **targets**: The endpoint of the "metrics" url you want to scrape. If you are running the application locally, 
                  we use host.docker.internal:9095, which resolves to the internal IP address used by the host.

In the case of Grafana application, there is another config file (**grafana.yml**) to define the datasource which points to the previous Prometheus Application.

1. Run the application and check if it is working properly 

```
cd goods-to-have/prometheus-and-grafana/
docker-compose up -d
```

Once you have executed the above command, If you open your browser, you will be able to see the Prometehus running in [http://localhost:9090](http://localhost:9090) 
and Grafana will be available in [http://localhost:3000](http://localhost:3000)

If you open [http://localhost:9090](http://localhost:9090) and go to **Status** > **Configuration**, you can see the configuration added:

![Prometheus Configuration](https://github.com/leandropremar/scraper-service/blob/master/screenshots/prometheus-config.png "Prometheus Configuration")

If you open [http://localhost:3000](http://localhost:3000), you will see a login screen. In order to access, the credentials are **admin/admin**. Once you are logged,
if you go to **Configuration** > **Datasource**, you can see the datasource added:

![Grafana Datasource](https://github.com/leandropremar/scraper-service/blob/master/screenshots/grafana-datasource.png "Grafana Datasource")

## Testing Prometheus and Grafana with our Application locally

Once you have all applications running (Scraper service, Prometehus and Grafana), you can genenarte automatic request to the service with the file 
**goods-to-have/request-scraper-service.py**. In that file, a list of url is read and every X seconds a new request is executed (I recommend use the file **goods-to-have/url-list.txt**, but feel free to add the urls you wish).

1. Run Request Script 

```
cd goods-to-have/request-script/
python3 goods-to-have/request-script/request-scraper-service.py <file_with_url_list> <time_in_seconds>
```
Example:

```
cd goods-to-have/request-script/
python3 request-scraper-service.py "url-list.txt" 3
```

2. If you want to stop it

```
Ctrl + C
```

If you open Prometheus endpoint [http://localhost:9090/graph](http://localhost:9090/graph) with the query **"{job="scraper-service"}"**, you can see all the metrics created by the request script:

![Prometheus Graph](https://github.com/leandropremar/scraper-service/blob/master/screenshots/prometheus-graph.png "Prometheus Graph")

If you open Grafana endpoint [http://localhost:3000/explore](http://localhost:3000/explore) with the query **"{job="scraper-service"}"**, you can see all the metrics created by the request script:

![Grafana Board](https://github.com/leandropremar/scraper-service/blob/master/screenshots/grafana-board.png "Grafana Board")

## Functional Tests

1. Install Python packages

```
pip3 install -r tests/requirements-test.txt
```
2. Run scraper application

```
python3 src/scraper_service.py
```
3. Run application

```
nosetests -v tests --tc-file=tests/config.ini
```

## Deploy Application in Kubernetes cluster

In **goods-to-have/k8s** you can find all the files for Kubernetes deployment:
 
 1. **scraper-service.yml**: This file contains:
    - **Deployment:** This contains the k8s deployment of the application. The image used is **leandrofreila/scraper-service**, abovementioned.
    - **LoadBalancer Service:** A loadbalancer to expose port 8080 and 9095 externally using a cloud provider's load balancer.
    - **Cluster IP Service:** A Cluster IP service to expose the app internally.

### Deploy Application in cluster
1. Create a namespace

```
kubectl create ns scraper-service
```

2. Deploy application in the above namespace

```
kubectl apply -f goods-to-have/k8s/scraper-service.yml -n scraper-service
```

3. You can check the application with a port-forward in your local machine 

```
kubectl port-forward deployment/scraper-service-deployment 8080 9095 -n scraper-service
```

Once you have executed the above command, Iif you open your browser, you will be able to see the server running in [http://localhost:8080](http://localhost:8080) 
To access to the metrics, they will be available in [http://localhost:9095/metrics](http://localhost:9095/metrics)

## Deploying Prometheus and Grafana in Kubernetes cluster

**Prometheus**

1. Get Repo

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add kube-state-metrics https://kubernetes.github.io/kube-state-metrics
helm repo update
```

2. Install 

```
helm install prometheus prometheus-community/prometheus
```

3. Add scraper config file 

```
helm upgrade --install prometheus \
--set rbac.create=true \
--set server.persistentVolume.enabled=false \
--set alertmanager.persistentVolume.enabled=false \
--set alertmanager.enabled=false \
--set kubeStateMetrics.enabled=false \
--set nodeExporter.enabled=false \
--set pushgateway.enabled=false \
--set-file extraScrapeConfigs=goods-to-have/k8s/prometheus-config.yml \
stable/prometheus
```

The config file (**goods-to-have/k8s/prometheus-config.yml**) has the same structure than the config locally file (**goods-to-have/prometheus-and-grafana/prometheus.yml**). The only difference is the target we use. Locally, the target is **host.docker.internal:9095**, which docker resolves to the internal IP address used by the host. In Kubernetes cluster, the target is **scraper-service.default.svc.cluster.local:9095**, this resolves to the cluster IP of the service.

**Grafana**

1. Get Repo

```
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

2. Install 

```
helm install grafana grafana/grafana
```

3. Add datasource of Prometheus

```
helm upgrade grafana --values goods-to-have/k8s/grafana-config.yml  stable/grafana
```

Now, the config file (**goods-to-have/k8s/grafana-config.yml**) also points to the prometheus-service **http://prometheus-server.default.svc.cluster.local**, in order to reach the prometheus from Grafana server.

## Testing Prometheus and Grafana in Kubernetes cluster

You can check both applications with a port-forward in your local machine:

1. Prometheus

```
kubectl port-forward service/prometheus-server 9090:80
```

2. Grafana

```
kubectl port-forward service/grafana 3000:80
```

Once you have executed the above commands, if you open your browser, you will be able to see the Prometehus running in [http://localhost:9090](http://localhost:9090) 
and Grafana will be available in [http://localhost:3000](http://localhost:3000)

In order to access to Grafana, you will need the login username and password:

```
kubectl get secrets grafana -o jsonpath='{.data.admin-password}' | base64 --decode 
kubectl get secrets grafana -o jsonpath='{.data.admin-user}' | base64 --decode
```

Once you have executed the "port-forward" commands, you will be able to check the working of the app (Scraper service, Prometheus and Grafana) through localhost in the same way than you can do it locally.

## Example of PromQL Query

Prometheus provides PromQL, a query language that enables users to do aggregations, analysis, and arithmetic operations on metric data.
If we access to [http://localhost:9090/graph](http://localhost:9090/graph) or Grafana endpoint [http://localhost:3000/explore](http://localhost:3000/explore), we can introduce multiple querys to analyse our data.

1. With the query 1, we can see all the metrics httt_get store for our application or job **scraper-service**.

```
http_get{job="scraper-service"}
```

![PromQL Query 1](https://github.com/leandropremar/scraper-service/blob/master/screenshots/promql-1.png "PromQL Query 1")

2. With the query 2, we filter all "3XX" status code querys using the operator **=~**.

```
http_get{job="scraper-service",code=~"3.."}
```

![PromQL Query 2](https://github.com/leandropremar/scraper-service/blob/master/screenshots/promql-2.png "PromQL Query 2")

3. With the query 3, we can sum all "200" status code querys and check the total amount in a graph instead of a table.

```
sum(http_get{job="scraper-service",code=~"200"})
```

![PromQL Query 3](https://github.com/leandropremar/scraper-service/blob/master/screenshots/promql-3.png "PromQL Query 3")

