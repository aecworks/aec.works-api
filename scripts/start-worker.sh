#!/bin/bash

source ./scripts/console.sh

celery -A api worker -l info
