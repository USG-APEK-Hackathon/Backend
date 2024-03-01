FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

COPY ./requirements.txt /${APP_HOME}/requirements.txt
RUN pip install -r requirements.txt

COPY ./docker/production/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

COPY . ${APP_HOME}

EXPOSE 8000

CMD ["/start.sh"]
