FROM python:3.8-slim-buster

WORKDIR /integration_tests

COPY ./src/api/ ./src/api/
COPY ./test/ ./test/
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV PROJECT_ID="841506577075"
ENV PROJECT_NAME="spotifind-api"
ENV CLIENT_ID="081f994d972f46519c1c8f9f6f11102a"
ENV SECRET_ID="spotify-rest-api-secret"
ENV SECRET_VERSION_ID="latest"
ENV ENVIRONMENT="staging"

CMD [ "python3", "-m", "unittest", "discover", "-s", "./test/integration_tests/" ]
