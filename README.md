## Objective
Create e2e test scenarios for the CRUD user operations with API Version 2 and HTTP Bearer Token authentication from 
https://gorest.co.in/ service.


## Execution
Tests can be run with one of following ways:

### GitHub page
- API token is already stored as GitHub secret.
- Go to actions page
- Select `Test Go-Rest API` workflow
- Hit `Run workflow` button

### Locally
- First create an `.env` file and paste `GO_REST_TEST_KEY=YOUR_TOKEN`. YOUR_TOKEN must be retrieved from [here][token].
- Then use one of the options below

#### Docker Container:
Build and run from included Dockerfile

#### Local venv
- Create venv
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `pytest -v`


## Design


## Limitations
`PUT` operations are not covered. This is because testing them would have been very similar to `PATCH`.

## Bugs Discovered
All test cases marked with `@pytest.mark.xfail` are one of:
- Certain bugs
- Potential bugs
- Possible improvements

Please read the `reason` comments for explanations.


[token]: https://gorest.co.in/my-account/access-tokens