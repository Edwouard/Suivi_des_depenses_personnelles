FROM python:3.9-alpine3.15

# Creer un repertoire pour l'application dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY ./requirements.txt .
# Installer les dependances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier le reste de l'application
COPY ./app .

# Exposer le port 5010 pour que l'application puisse être accessible depuis l'extérieur du conteneur
EXPOSE 5010

# Lancer l'application avec gunicorn
CMD ["gunicorn", "-b", ":5010", "wsgi:app", "--timeout", "30000", "--workers", "1"]
