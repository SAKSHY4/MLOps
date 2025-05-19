# syntax=docker/dockerfile:1.4

########################################################
# Stage 1: Build all wheels for your dependencies
########################################################
FROM python:3.9-slim-bullseye AS builder

WORKDIR /app

# Install build tools for any packages that need compilation
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements and build wheels into a cache directory
COPY app/requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

########################################################
# Stage 2: Final image with just runtime dependencies
########################################################
FROM python:3.9-slim-bullseye

WORKDIR /app

# Copy pre-built wheels and install them without accessing PyPI
COPY --from=builder /wheels /wheels
COPY app/requirements.txt .
RUN pip install --no-index --find-links=/wheels -r requirements.txt
RUN pip install pytest

# Copy your application code and model
COPY model.pkl .
COPY app/ .

EXPOSE 5000
CMD ["python", "app.py"]
