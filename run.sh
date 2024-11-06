#!/bin/bash

echo "Starting ..."

# Select application to run
case $APPLICATION in
    # Django backend
    django)

        # Collect and upload static files to s3
        python manage.py collectstatic --noinput

        # Run DB migrations
        python manage.py migrate

        ## Custom command
        #python manage.py  providers_handle

        # Run server
        python manage.py runserver 0.0.0.0:8000
        ;;

    celery_worker)

        # Run application
        celery -A super_app worker --loglevel=info --concurrency=1
        ;;

    celery_beat)

        # Run application
        celery -A super_app beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
        ;;

    *)
        echo "No application specified"
        ;;
esac

echo "Exiting ..."
