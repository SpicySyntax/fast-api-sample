## FastAPI example project
This is a basic Fast-API python project with examples of proper unit test, integration tests, code coverage, CI/CD, and code scanning.

## Relevant Reading
- [Fast API docs](https://fastapi.tiangolo.com/)
- [Fast API docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)

## Prerequesites
- Python: ^3.8
- [Pipenv](https://github.com/pypa/pipenv)
- [Docker](https://docs.docker.com/) + [Docker Compose](https://docs.docker.com/compose/)
- [Terraform](https://www.terraform.io/downloads.html): ^v0.14.2 Use homebrew if on Mac `brew install terraform`

## Deployment
To build, test, scan, and deploy a new version of the docker image you just need to push a new tag.
e.g.
```bash
git tag # list tags
git tag 1.2.3 # tag my version
git push --tags # push any commits with tags
```

## Setup Python Environment
```bash
pip install pipenv # if you haven't already
pipenv install --dev # download dependencies
pipenv shell # use pipenv env in shell
pipenv run pytest . # run commands in pipenv env (like tests)
```


## Run Fast API Directly
```bash
# NOTE: source AWS creds before
pipenv run uvicorn app.main:app --reload     
```


## Build/Run with Docker 
```bash
# NOTE: source AWS sbx creds before
docker-compose up --build # use '--build' if rebuilding 
```

## Autohooks (Pre commit checks)
Auto hooks integration allows us to run pylint, black, and pytest before committing to source control.
- `pylintrc` is configured based off of the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- `black` will auto format code on commit (it just works out of the box)
- `pytest` is used to run unit and integration tests

```bash
autohooks activate --mode pipenv # activate pre-commit hooks
```

## VS Code setup
In order to get intellisense in VS Code, install the [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
First, we need the python path for our virtual pipenv environment:
```bash
pipenv run which python # Save this path to python for later, will be referenced as venv_path below
```

To configure it properly we must setup our `.vscode/settings.json` as such:
```json
{
    "python.pythonPath": "{venv_path}/bin/python/",
    "python.envFile": ".env",
    "python.testing.cwd":	".",
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestPath":	"{venv_path}/bin/pytest",
    "python.testing.pytestArgs":	[".", "-c", "pytest.ini"],
    "python.testing.autoTestDiscoverOnSaveEnabled": true,
    "python.linting.pylintEnabled": true
}
```
After doing this intellisense should work in vscode, and tests should be discoverable/runnable

## Code Coverage
We use `pytest-cov` to generate test coverage reports for the python code. We integrate this into out gitlab CI adhering to this [gitlab code coverage doc](https://docs.gitlab.com/ee/user/project/merge_requests/test_coverage_visualization.html#how-test-coverage-visualization-works)


## Code scanning
This project contains some code scanning stage examples in the `.gitlab-ci.yml`.

See these [docs](https://amfament.atlassian.net/wiki/spaces/AppSec/pages/1196163102/Application+Security+Scanning+Capabilities+-+DRAFT) for some more detials

For SAST (fortify) scanning to work we can create a `requirements.txt` in the root of the project using the following:
```bash
pipenv lock -r > requirements.txt
```
