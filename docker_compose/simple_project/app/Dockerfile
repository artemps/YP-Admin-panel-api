FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 4
ENV UWSGI_THREADS 8
ENV UWSGI_HARAKIRI 60
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini
COPY entrypoint.sh entrypoint.sh

RUN apt-get update && apt-get install -y netcat-traditional

RUN  mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/opt/app/entrypoint.sh"]
