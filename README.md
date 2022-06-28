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
