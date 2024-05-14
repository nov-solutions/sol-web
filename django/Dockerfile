FROM python:3.9

# python things
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# default is dev
ARG BUILD_ENV=dev
ENV BUILD_ENV=${BUILD_ENV}

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt --no-cache-dir

# run dev server or daphne for production
CMD if [ "$BUILD_ENV" = "dev" ]; then \
        python manage.py collectstatic --noinput && \
        python manage.py migrate && \
        python manage.py runserver 0.0.0.0:8000; \
    else \
        python manage.py collectstatic --noinput && \
        python manage.py migrate && \
        daphne -b 0.0.0.0 -p 8000 NEWSOLWEBAPP.asgi:application --application-close-timeout 120; \
    fi
