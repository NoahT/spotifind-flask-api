FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
COPY src/api/ src/api/

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "--workers=1", "src.api.app:flask_app", "--bind=0.0.0.0:5000"]

