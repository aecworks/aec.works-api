FROM python:3.8-slim
RUN apt-get update && apt-get install -y postgresql-client

# Setup directories
RUN mkdir /code
# Python Config
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Python dependencies
RUN pip install --upgrade pip==19.2.1
ADD requirements.txt /code/
ADD requirements-dev.txt /code/
RUN pip install -r /code/requirements.txt
RUN pip install -r /code/requirements-dev.txt

EXPOSE 8000
# Files will be Mounted
WORKDIR /code
CMD ["./scripts/serve-dev.sh"]
