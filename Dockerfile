FROM python:3.9-alpine3.15

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app .

# Commande pour initialiser la base de données
RUN python -c "from app import app, db; app.app_context().push(); db.create_all()"

EXPOSE 5010

CMD ["gunicorn", "-b", ":5010", "wsgi:app", "--timeout", "30000", "--workers", "1"]
