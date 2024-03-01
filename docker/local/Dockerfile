FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

COPY ./requirements.txt /${APP_HOME}/requirements.txt
RUN pip install -r requirements.txt

COPY ./docker/local/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

COPY . ${APP_HOME}
