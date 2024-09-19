FROM python:3.12-alpine
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
ADD . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt