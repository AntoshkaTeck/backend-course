docker run --name booking-celery-worker \
    --network=backend-course_default \
    booking-image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO


docker run --name booking-celery-beat \
    --network=backend-course_default \
    booking-image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

docker run --name booking-nginx \
    -v ./nginx.conf:/etc/nginx/nginx.conf \
    -v /etc/letsencrypt:/etc/letsencrypt \
    -v /var/lib/letsencrypt:/var/lib/letsencrypt \
    --network=project_default \
    --rm -p 80:80 -p 443:443 nginx


docker run -d \
    --name postgres \
    --restart unless-stopped \
    --network=project_default \
    -e POSTGRES_USER=booking \
    -e POSTGRES_PASSWORD=booking123 \
    -e POSTGRES_DB=booking \
    -p 5432:5432 \
    -v pg_data:/var/lib/postgresql/data \
    postgres:14

docker run -d \
    --name redis \
    --network=project_default \
    --restart always \
    -p 6379:6379 \
    -v ./data:/data \
    redis:7.2 \
    redis-server --appendonly yes