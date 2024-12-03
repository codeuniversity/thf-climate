# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.10
FROM python:${PYTHON_VERSION}-slim-bullseye as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy requirements ahead of code to utilise docker cache
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY ./src /code/src

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
