## Objective
Create e2e test scenarios for the CRUD user operations with API Version 2 and HTTP Bearer Token authentication from 
https://gorest.co.in/ service.


## Execution
Tests can be run with one of following ways:

### Repository
Through GitHub actions(on push).  
API token is already stored as GitHub secret.

### Locally
First create a `.env` file and paste `GO_REST_TEST_KEY=YOUR_TOKEN`.  
YOUR_TOKEN must be retrieved from [here][token].

#### Docker Container:
Build and run from included Dockerfile

#### Local venv
- Create venv
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `pytest -v`


## Design


## Limitations


## Bugs Discovered 


[token]: https://gorest.co.in/my-account/access-tokens