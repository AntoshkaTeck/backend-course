FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

#CMD ["python3", "src/main.py"]
CMD alembic upgrade head; python3 src/main.py