FROM tiangolo/uvicorn-gunicorn:python3.7

RUN pip install --no-cache-dir fastapi==0.60.1

COPY ./app /app
