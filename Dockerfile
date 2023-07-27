FROM python:3.11-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y libpq-dev gcc
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY run.sh .
COPY backend/requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt --no-cache-dir && pip install gunicorn
COPY ./backend/ .
RUN chmod +x run.sh
ENTRYPOINT ["/app/run.sh"]
