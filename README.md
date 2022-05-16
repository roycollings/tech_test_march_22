
# Technical exercise: api-test framework

# Execution
## Pre-requisites
The following environment variables need to be set:
- `API_VERSION`: (currently '0')
- `API_URL`: the api url (i.e. http://my-api.com)
- `KOTP`: one time password for the api key
- `KPUBLIC`: your public key
- `KPRIVATE`: your private key

## Running
The tests are dockerised and can be executed with
```
docker-compose up
```
If you are running without docker-compose, you need Python 3.8 (_see below_).

## Reports
Reports are created in the _output/_ folder. The _output/report.html_ gives an interactive html report of the test results.

The tests (and linting checks) are also run against pull requests (on push). In this case, the test report is zipped and is available in github as described here: https://github.com/actions/upload-artifact#where-does-the-upload-go

## Language choice
I'm very excited at the prospect of learning Rust, but given the available time I had during the week, I chose to go with Python since it was more familiar and allowed me to focus more on design etc ...

## Schema check approach
I created the json schemas based on the official Swagger file (assuming this to be the 'single source of truth') and observations (assuming, for the sake of this exercise, that the production API is currently correct).

## Frameworks considered
I avoided any 3rd party 'middleware' frameworks (i.e. with helper methods to fetch assets etc...) between myself and the api, since I wanted to test the api as directly as possible.

To prioritize my time, I only explored the following BDD frameworks (by implementing and running a few different scenario types and exploring the limitations of each).

My preference is usually to go with the most common frameworks (familiar patterns to everyone, easier to onboard, bigger community support and so on), unless the value offered by a less commmon framework is worth the difference.

I'm presuming test execution speed is very important, so I made the ability run tests in parallel to be a vital requirement (especially as this scales up to cover current and future endpoints).

| Framework  | PyPi page  | Analysis   |
|---|---|---|
| behave  |https://pypi.org/project/behave/   | Most popular Python BDD framework. However, doesn't offer parallel execution (_**deal breaker**_)|
| behave-parallel  | https://pypi.org/project/behave-parallel/  | Not updated in the last 7 years, only supports 'basic' formatter in parallel mode so no chance of html report / or json (_**deal breaker**_)|
| pytest-bdd  |https://pypi.org/project/pytest-bdd/   | Offers parallel execution and is familiar to pytest users (which is a large community). However, it has some 'quirks' that could cause problems as tests grow in number and complexity (tying steps explicitly to specific features, outlines require non standard workarounds etc...).   |
| behavex  | https://pypi.org/project/behavex/  | Only works on Python < 3.9. However, provides full html report 'out of the box' and the last update was 2 months ago.  |

### Conclusion
I chose `behavex` as it was easy to implement, intuitive and simple to use and produced a nice report out of the box, while following the same syntax etc... as _Behave_ and is, therefore, still familiar to most. The limitation to python 3.8 is a concern, but since it's being actively maintained it's reasonable to assume it'll support 3.9 soon (if not, we could fork it and make our own 3.9 version).

#### Side notes
I disabled these linters in the step definition files:
- function-redefined
- missing-function-docstring

The steps themselves describe _exactly_ what will happen in each function (no more, no less -  no 'scope creep'), so an extra message on each with the same text as the step itself would have caused a lot of 'noise' without any benefit.
Also, because of how Behave wraps the step functions they can have the same 'name' since the _actual_ function name is the step title. This makes it a lot easier and more minimal to write: instead of spending time thinking up unique names etc... for no gain, they are all just called `step_impl`.

# If I had more time ...
I would have ideally verified the response schemas _directly_ against the Swagger spec (and fetched the latest version at the start of each test run). This would remove the need for hardcoded schema files, removing the chances of human error creating the schema files, files being out of date, and the general overhead of maintaining them manually.

(I gave myself 2 hours to investigate tools that support that but didn't find a satisfactory solution in that time.)