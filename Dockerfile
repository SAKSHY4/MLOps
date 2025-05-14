# Dockerfile
FROM python:3.9-slim-bullseye

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY model.pkl .
COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]