#!/bin/sh

until cd /code
do
    echo "Waiting for web volume..."
done

celery -A test_uchet_kz worker --loglevel=info
