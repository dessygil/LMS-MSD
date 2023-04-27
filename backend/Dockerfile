# FROM python:3.12.0a5-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# COPY . /code/

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.11-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev 
RUN pip install -r requirements.txt
RUN apk del build-deps
COPY . /code/
RUN pytest -W error
