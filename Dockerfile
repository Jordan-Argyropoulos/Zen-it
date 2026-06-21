FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Whitenoise servira les statics en prod
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Migrate au démarrage (acceptable pour un MVP, pas pour scale massif)
CMD ["sh","-c","python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --workers 2 core.wsgi:application"]
