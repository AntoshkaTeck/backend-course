docker run --name booking-celery-worker \
    --network=backend-course_default \
    booking-image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO


docker run --name booking-celery-beat \
    --network=backend-course_default \
    booking-image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

docker run --name booking-nginx \
    -v ./nginx.conf:/etc/nginx/nginx.conf
    --network=project_default \
    --rm -p 80:80 nginx
