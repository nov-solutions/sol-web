FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/django

COPY ./django /app/django

RUN pip install -r requirements.txt --no-cache-dir

CMD python manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
