# Basic setup
FROM python:3.11.7-slim-bullseye
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Run on port 8000
EXPOSE 8000

# Run using uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]