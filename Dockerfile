# syntax=docker/dockerfile:1.4

FROM python:3.10-slim-bullseye

WORKDIR /app

# Copy pre-built wheels and install them without accessing PyPI
COPY wheels /wheels
COPY app/requirements.txt .

RUN pip install --no-index --find-links=/wheels -r requirements.txt
RUN pip install pytest

# Copy your application code and model
COPY model.pkl .
COPY app/ .

EXPOSE 5000
CMD ["python", "app.py"]