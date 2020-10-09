FROM python:3.8-slim
RUN apt-get update && apt-get install -y \
    postgresql-client \
    make
libmagic1

# Setup directories
RUN mkdir /code
# Python Config
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Python dependencies
RUN pip install --upgrade pip==20.2.3
ADD requirements.txt /code/
RUN pip install -r /code/requirements.txt

EXPOSE 8000
# Files will be Mounted
WORKDIR /code
CMD ["./scripts/serve-dev.sh"]
