# aec.works
-----

## Development Environment

**Requirements**

* Docker
* make

#### Setup

Configure project and install dependencies:

```
$ make setup
```

#### Dev

```bash
# Start db (postgres) and web (django) containers
$ make start
$ open "http://localhost:8000"

# Stream stdout/stderr of both containers
$ make logs

# Open Shell inside container
$ make bash
```

### Editor Setup

**Requirements**

* VSCode
* [Install Remote Container Extension](https://code.visualstudio.com/docs/remote/containers)


### Local Python Virtual Environment

If you don't want to user VS Remote Containers or for any other reason need to setup a local Python Environment:

* Python 3.8 (pyenv recommended)
* `python -m venv .venv`
* `source ./.venv/bin/activate`
* `pip install -r requirements.txt`
* `pip install -r requirements-dev.txt`
* python manage.py runserver


## Contributing

This project loosely follows patterns established by [Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide) and [Django Api Domain](https://phalt.github.io/django-api-domains/styleguide/).


The key concepts are:
* Views thin views responsible for (de)serializing only
* Serializers: avoid re-use. Don't user serializers's `create()` functionality as that coupling between view serializing and object creation is problematic.
* Models: models are _thin_ and should only be responsible defining fields and relationships.
* Services: all logic, object creation, modification, deletion happens in dedicated services. If a service function takes more than 2 arguments it should use keyword arguments.
* Selectors: all "queries" should be build as selectors. Views should not query models directly. Why? Querying logic can  increases in complexity overtime and having a central place to define and re-use those is helpful.
* Querysets: user sparingly, but can be used to define reusable model querying logic that is reusable across multiple selectors.

