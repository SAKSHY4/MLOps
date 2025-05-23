# syntax=docker/dockerfile:1.4

FROM python:3.10-slim-bullseye

WORKDIR /app

COPY wheels /wheels
COPY app/requirements.txt .

RUN pip install --no-index --find-links=/wheels -r requirements.txt
RUN pip install pytest

COPY model.pkl .
COPY app/ .
COPY templates/ ./templates/
COPY static/ ./static/
COPY tests/ ./tests/

EXPOSE 5000
CMD ["python", "app.py"]