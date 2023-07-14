FROM python:3.10.0-alpine3.14

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/app"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev \
    && pip install --upgrade pip  \
    && pip install --no-cache-dir -r requirements.txt 


# Create a group and user
RUN addgroup -S stockfinch && adduser -S appuser -G stockfinch

# Tell docker that all future commands should run as the appuser user
USER appuser
COPY . .
RUN export PYTHONPATH="$PYTHONPATH:/app"
CMD ["python", "./src/app.py"]  