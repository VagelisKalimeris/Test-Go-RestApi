## Objective
Implement test automation pipeline for https://gorest.co.in/ service, with API Version 2 and HTTP Bearer Token 
authentication.

## Execution
Run tests by one of following ways:

### GitHub page
- Go to repository actions page
- Select `Test Go-Rest API` workflow
- Hit `Run workflow` button
- API token is already stored as GitHub secret.


### Locally
- Create a TOKEN [here][token].
- Create an `.env` file and paste `GO_REST_TEST_KEY=TOKEN`. 
- Then use one of the options below

#### Docker Container:
Build and run from included `Dockerfile`

or

#### Local env
- Create venv (optional)
- Install dependencies with `pip install -r requirements.txt`
- Run tests with `pytest -v`


## Design
Having access to the system, would have enabled pre-configuring a trusted test environment with data, in turn decoupling 
resource creation/destruction from test run.  
This was not an option, so instead a dynamic approach was followed, which is in no way best practice, but should leave 
the system in a consistent state:  
- A set of test data is created at setup and removed during teardown. During these phases `CREATE`/`DELETE` operations 
  are tested too(this is an anti-pattern, but saves code repetition).  
- Test cases have access to these resources and create/delete extra ones, on a need basis. When this happens 
  `CREATE`/`DELETE` operations are not asserted again, since this is already done during setup/teardown.


## Limitations
- `PUT` operations are not covered. This is because these test cases would have been very similar to `PATCH` cases.
- Testing paginated results works in unfiltered 'contains' operations, since newly added test data come up in 1st 
  page(default sorting by latest entry).  
  However, for 'does not contain' operations, we need to go through all result pages, and this is blocked by api 
  with `429, Too many requests`.  
  PRs #2 and #3 were attempts at fixing this.

## Bugs Discovered
All test cases marked with `@pytest.mark.xfail` are one of:
- Certain bugs. Search for `This actually looks like a BUG`.
- Potential bugs. Search for `Not sure if its a BUG`.
- Possible improvements Search for `Problem here is`.

Please read the `reason` comments for further explanations.


[token]: https://gorest.co.in/my-account/access-tokens