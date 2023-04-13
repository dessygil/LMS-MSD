# FROM python:3

# WORKDIR /home/app

# #If we add the requirements and install dependencies first, docker can use cache if requirements don't change
# ADD requirements.txt /home/app
# RUN pip install --no-cache-dir -r requirements.txt

# ADD . /home/app

# # Migrate the database
# RUN python manage.py migrate

# EXPOSE 8000

FROM python:3.11-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/