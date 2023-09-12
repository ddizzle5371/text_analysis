**Project Description**

This text analysis microservices application is written in Python using Flask. The service discovery api manages
different text analysis services via a service registry, providing endpoints to add, remove, and list the services.
The central microservice, namely main, provides an endpoint that accepts the name of the service and text, which 
queries the service by the name in the service registry and forward the text to the service. It is guaranteed only one instance 
of the service registry is created within the context of an application process, throttling the number of connections 
to the Redis client of the service registry with a locking mechanism.

The application is dockerized and can be easily set up with minimal commands. Additionally, docker-compose gives
flexibility to adjust host and port numbers from the file and reflect the change across the entire application. 
Redis was utilized to store the serivce_name to service_url mapping to accomodate a runtime environment with minimal
requirements for the application to run. (i.e Consul was a good alternative to Redis, but it was requiring extra network
configurations on the development machine on macOS). 


**How to Run**
1. Clone the project
2. Install docker:
```ex) on macOS, brew install docker```
3. Install docker-compose:
```ex) on macOS, brew install docker-compose```
4. From project root, run docker compose up:
```docker compose up --build main service_discovery sentiment_analysis word_count entity_recognition```

**How to Run test**
1. Clone the project
2. From project root, run: ```docker compose up --build test```


**Use Cases**
1. Registering a service
```HTTP
POST /services
Content-Type: application/json
{
  "name": "{service_name}",
  "url": "http://{service_name}:{port_number}/analyze"
}
```
```HTTP
POST /services
Content-Type: application/json
{
  "name": "sentiment_analysis",
  "url": "http://sentiment_analysis:8003/analyze"
}

200 OK
Content-Type: application/json
{
  "message": "sentiment_analysis is successfully registered to the registry"
}
```

2. Deleting a service
```HTTP
DELETE /services/service_name
Content-Type: application/json
```

```HTTP
DELETE /services/sentiment_analysis
Content-Type: application/json

200 OK
Content-Type: application/json
{
  "message": "sentiment_analysis is successfully removed from the registry"
}
```

3. Listing services
```HTTP
GET /services
Content-Type: application/json

200 OK
Content-Type: application/json
{
  "message": {
    "sentiment_analysis": "http://sentiment_analysis:8003/analyze",
    "entity_recognition": "http://entity_recognition:8002/analyze",
    "word_count": "http://word_count:8004/analyze"
}
```

4. Performing Text Analysis
```HTTP
POST /analyze
Content-Type: application/json

{
  "service": "{service_name}",
  "text": "text"
}
```

```HTTP
POST /analyze
Content-Type: application/json

{
  "service": "sentiment_analysis",
  "text": "The weather is great today!"
}


200 OK
Content-Type: application/json

{
  "message": "positive"
}
```

5. Error: Invalid Service
```HTTP
POST /analyze
Content-Type: application/json

{
  "service": "non_existent_service",
  "text": "The weather is great today!"
}
```

```HTTP
404 Not Found
Content-Type: application/json

{
  "error": "non_existent_service does not exist in the registry"
}
```

NOTES 
  - Ensure `service_name` and `port_number` match the values in docker-compose.yml.
  - Every endpoint can be reached from public via `http://{host}:{port}/method_name`.
  - Every dockerized app can only be communicating with one another via `http://{service_name}:{service_port}/method_name`
  - To demonstrate the main microservice forwarding request to the corresponding text anaylsis service,
    the service urls must be same as dockerized container ip addresses. In other words, 
    - make a POST request 
      to `http://{service_discovery_host}:{service_discovery_port}/services` with service of `sentiment_analysis` and 
      url of `http://sentiment_analysis:{sentiment_analysis_port}/analyze` to register sentiment_analysis
    - make a POST request to `http://{main_host}:{main_port}/analyze` with service of `sentiment_analysis` and text, which
      forwards the request to `http://sentiment_analysis:{sentiment_analysis_port}/analyze` internally.
