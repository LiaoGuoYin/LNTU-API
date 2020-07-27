FROM tiangolo/uvicorn-gunicorn:python3.8

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

COPY ./app /app

WORKDIR /app

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host 0.0.0.0", "--port 80", "--reload"]
