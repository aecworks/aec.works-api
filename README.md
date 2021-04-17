## aec.works-api

![Django CI](https://github.com/aecworks/aec.works-api/workflows/Django%20CI/badge.svg)
[![codecov](https://codecov.io/gh/aecworks/aec.works-api/branch/master/graph/badge.svg?token=RJ7ZNWGNBQ)](undefined)

![logo](https://aec.works/img/logo-black.10fa9bc4.svg)

### Development Environment

#### Requirements

- Docker - [Get Docker Docs](https://docs.docker.com/get-docker/).
- make - [Docs For Windows Users](https://stackoverflow.com/a/32127632/4411196)
- Python 3.8

Python Install Note

> Instructions for setting up Python 3.8 varies by environment and OS.
> For Windows, I recommend using the installers from [python.org/downloads/](https://www.python.org/downloads/). For Mac or Linux, you can use the installers as well, or [pyenv](https://github.com/pyenv/pyenv) (recommended).

#### Project Setup

> Note: access to `aecworks-env` which holds env secrets must be granted first

```
$ make setup
```

This command will handle the following for you:

- Check you have the correct Python version available
- Create or rebuild a local virtual environment (`./.venv`)
- Install all dependencies
- Configure git hooks

See `scripts/setup.sh` for more details.

Now let's spin up our docker resources and test that everything works:

```
$ make start
$ make test
```

This will spin up a Postgres database and Redis instance as defined in
our `docker-compose.yml` file.

You can check the status of these containers with `docker ps`.

#### Developing

```bash

# first seed database with fixtures
$ make seed

# start our dev server
$ make serve

```

#### Admin Panel

You can inspect the models and seed data through the builtin admin panel at `localhost:8000`.
For convenience a superuser is provisioned in the dev environment `dev@dev.com` password `1`.

#### Virtual Environment

If you need to run commands using the interpreter created in the `.venv` virtual environment, just activate the virtual environment first.

```bash
$ source .venv/bin/activate
$ (.venv) python manage.py migrate
```

Note: this command my vary based on the Operating System your are using.


If you are not familiar with Python's venv module you can [checkout the docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment).

### Editor Setup

**Requirements**

- VS Code (recommended)

VS Code is not required but highly recommended - if using a different editor make sure the settings in `.vscode/settings.json` and `.editorconfig` are respected.
With correct editor setup, files should be automatically linted (flake8 + mypy) and formatted (black).

VS Code should automatically format your code, sort imports, and lint errors.
If for some reason that's not working, try to get it fixed before pushing a PR.

## Contributing

#### Project Structure

```
aecworks-api/
├── api
│   ├── aecworks   -> django project config (urls, settings, etc)
│   ├── common     -> shared resources (utils, exceptions, mixins, etc)
│   ├── community  -> Django App: Community Domain (Posts, Companies, Articles, Etc)
│   ├── images     -> Django App: Images
│   ├── users      -> Django App: Users, Profiles
│   └── webhooks   -> Django App: Wehooks (Twitter Zapier Integration)
├── ...
```

#### App Structure

While each app is unique, they will often have contain these:

```
├── views       -> DRF Views
├── selectors   -> queryset builders
├── services    -> model operations, Business Logic, etc
├── models      -> orm model definitions
├── factories   -> model factories for seeding + testing
└── admin       -> admin models
```

PS: Django apps are intended to be self contained and portable. While that's not always the case, separating models by _domain_ is still helps to make projects easier to understand and maintain.

#### API

For latest API docs, see the [postman collections docs](https://documenter.getpostman.com/view/1727228/Szt79Vv8).

#### Admin Panel

The Django admin panel is available at`/admin/`. The local development server automatically seeds a dev user you can use to explore the data right away.

- Email: `dev@dev.com`
- Password: `1`

PS: these same credentials can be use to authenticate your postman

#### Django Code Structure and Style Guide

The API relies heavily on [Django Rest Framework (DRF)](https://www.django-rest-framework.org/) so developing some familiarity with its patterns and constructs is helpful.

It also loosely follows patterns established by [Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide) and [Django Api Domain](https://phalt.github.io/django-api-domains/styleguide/).

The key concepts are:

- **Views**: are thin and responsible primarily for (de)serializing, calling a service, and returning a Response
- **Serializers**: avoid re-use. Don't user serializers's `create()` functionality as that coupling between view serializing and object creation is problematic.
- **Services**: all logic, object creation, modification, deletion happens in services.
- **Models**: models are _thin_ and only be responsible for defining fields and relationships.
- **Selectors**: all "queries" should be build as selectors. Avoid building queries directly in views as querying logic can increases in complexity overtime. Having a central place to define and re-use those selectors is helpful.
- **Querysets**: user sparingly, but can be used to define reusable model querying logic that is reusable across multiple selectors.

### Frontend

To run the frontend locally see [aecworks-web](https://github.com/aecworks/aec.works-web).

## License

GNU GPL V3
