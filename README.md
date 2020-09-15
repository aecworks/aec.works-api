## aec.works-api
![Django CI](https://github.com/aecworks/aec.works-api/workflows/Django%20CI/badge.svg)

![logo](https://aec.works/img/logo-black.10fa9bc4.svg)


### Development Environment

#### Requirements

* Docker - [Get Docker Docs](https://docs.docker.com/get-docker/).
* make - [Docs For Windows Users](https://stackoverflow.com/a/32127632/4411196)
* Python 3.8

Python Install Note

> Instructions for setting up Python 3.8 varies by environment and OS.
For Windows, I recommend using the installers from [python.org/downloads/](https://www.python.org/downloads/). For Mac or Linux, you can use the installers as well, or [pyenv](https://github.com/pyenv/pyenv) (recommended).


#### Project Setup

Configure project and install all dependencies:

```
$ make setup
```

> Note: access to `aecworks-env` which holds env secrets must be granted first

#### Dev-ing

```bash

# Start db (postgres) and web (django) containers
$ make start

# Stream stdout/stderr of both containers
$ make logs

# Open Shell inside container
$ make bash
```

### Editor Setup

**Requirements**

* VSCode Recommended

VS Code is not required but highly recommended - if using a different editor, make sure the settings in `.vscode/settings.json` and `.editorconfig` are respected.

With correct editor setup, files should be automatically linted (flake8 + mypy) and formatted (black).


## Contributing

#### Django
The Django project structure loosely follows patterns established by [Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide) and [Django Api Domain](https://phalt.github.io/django-api-domains/styleguide/).


The key concepts are:
* Views thin views responsible for (de)serializing only
* Serializers: avoid re-use. Don't user serializers's `create()` functionality as that coupling between view serializing and object creation is problematic.
* Models: models are _thin_ and should only be responsible defining fields and relationships.
* Services: all logic, object creation, modification, deletion happens in dedicated services. If a service function takes more than 2 arguments it should use keyword arguments.
* Selectors: all "queries" should be build as selectors. Views should not query models directly. Why? Querying logic can  increases in complexity overtime and having a central place to define and re-use those is helpful.
* Querysets: user sparingly, but can be used to define reusable model querying logic that is reusable across multiple selectors.


## License

TODO - Not Licensed
