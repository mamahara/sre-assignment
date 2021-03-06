# sre-assignment
Introduction:
This repository is to create a simple Python flask api application and elasticsearch with below endpoints
- a health endpoint which returns OK
- an endpoint for inserting or updating a city and its population
- an endpoint for retrieving the population of a city
- an endpoint to get all city with population details

Prerequisite:
Below prerequistes are needed to install the chart:
- helm3 needs to be installed
- a kubernetes cluster and dynamic provisioning storageclass for elasticsearch to provision PV
- a ingress class is required, if ingress for application is to be used instead of NodePort

Installation:
Please download/clone the code repo to local folder:
git clone https://github.com/mamahara/sre-assignment/
Folder details:
- src folder has all python files with all source code
- server-conf has all supporting files for dockerize and deploy using uwsgi and nginx
- Dockerfile: application image can be built using Dockerfile and already built image is available on dockerhub : mamahara/sre-assignment:1.0
- requirement.txt file all python dependency libraries
- k8s-anifest file has some k8s manifest for application deployment
- charts folder has the helm chart for this application and a dependency chart(elasticsearch) for application
- elasticsearch cluster is minimal with one node and can be scaled in future if required

Installation steps:
1. Download the repo to local where helm is installed
2. move to the sre-assignment folder
3. Install chart using below command
   - create namespace where chart need to be deployed
     ex: kubectl create namespace g42
   - install chart. example: helm install g42-sre-assignment charts/sre-assignment/ -n namespace-name
   - elasicsearch pod may take sometime to be readily available
   - Once elasticsearch is pod is available application would be up and running, verify using : kubectl get pods -n namespace-name

4. check the nodeport service and access application using the nodeport if ingress controller is not available

Application Testing:
This Application is Flask Api based and has below endpoints.
1. GET: /api/v1/healthcheck :
Application healthheck endpoint and returns {"health": "ok"} if elastic search DB is connected

2. POST: /api/v1/addOrUpdateCityPopulation :
This endpoint is to add or update a city name and population details. City names are not case-sensitive and will not be duplicated on elasticsearch.
Api Details:
Method: POST
body example: {"city_name": "Dubai", "population_count": "686936546"}
Content-type: application/json
example curl request:
curl -d "{\"city_name\": \"Abu Dhabi\", \"population_count\": \"6866546\"}" -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1/addOrUpdateCityPopulation

3. GET:  /api/v1/getCityPopulation/city_name
4. POST: /api/v1/getCityPopulation :
This endpoint is to fetch population details for city. City names are not case-sensitive.
Api Details:
Method: POST
body example: {"city_name": "Dubai"}
Content-type: application/json
example curl request:
curl -d "{\"city_name\": \"Dubai\"}" -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1/getCityPopulation

Conclusion:
Thanks

