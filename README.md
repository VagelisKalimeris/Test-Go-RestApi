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

OR

#### Local env
- Create venv (optional)
- Install dependencies with `pip install -r requirements.txt`
- Run tests with `pytest -v`


## Design
Having access to the system would have enabled pre-configuring a test environment with data. That would have offered 
resource creation and test run decoupling.  
Since this was not an option, a dynamic approach was followed:  
- A set of test data is created at setup and removed during teardown. During these phases `CREATE`/`DELETE` operations 
  are tested too.   
- Tests access these resources and create/delete extra ones, on a need basis. When this happens `CREATE`/`DELETE` 
  operations are not asserted again, since this is already part of setup/teardown.


## Limitations
`PUT` operations are not covered. This is because testing them would have been very similar to `PATCH` which is covered.

## Bugs Discovered
All test cases marked with `@pytest.mark.xfail` are one of:
- Certain bugs. Search for `This actually looks like a BUG`.
- Potential bugs. Search for `Not sure if its a BUG`.
- Possible improvements Search for `Problem here is`.

Please read the `reason` comments for explanations.


[token]: https://gorest.co.in/my-account/access-tokens