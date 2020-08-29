# aec.works
-----

## Development Environment

**Requirements**

* Docker
* make

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

* https://github.com/HackSoftware/Django-Styleguide

