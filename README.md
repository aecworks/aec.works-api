## aec.works-api
![Django CI](https://github.com/aecworks/aec.works-api/workflows/Django%20CI/badge.svg)

![logo](https://aec.works/img/logo-black.10fa9bc4.svg)


### Development Environment

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
# Get .env file

# Start db (postgres) and web (django) containers
$ make start

# Stream stdout/stderr of both containers
$ make logs

# Open Shell inside container
$ make bash
```

### Editor Setup

**Requirements**

* VSCode
* [Install Remote Container Extension](https://code.visualstudio.com/docs/remote/containers)


## Contributing

This project loosely follows patterns established by [Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide) and [Django Api Domain](https://phalt.github.io/django-api-domains/styleguide/).


The key concepts are:
* Views thin views responsible for (de)serializing only
* Serializers: avoid re-use. Don't user serializers's `create()` functionality as that coupling between view serializing and object creation is problematic.
* Models: models are _thin_ and should only be responsible defining fields and relationships.
* Services: all logic, object creation, modification, deletion happens in dedicated services. If a service function takes more than 2 arguments it should use keyword arguments.
* Selectors: all "queries" should be build as selectors. Views should not query models directly. Why? Querying logic can  increases in complexity overtime and having a central place to define and re-use those is helpful.
* Querysets: user sparingly, but can be used to define reusable model querying logic that is reusable across multiple selectors.

