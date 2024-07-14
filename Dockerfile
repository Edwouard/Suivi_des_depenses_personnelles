FROM python:3.9-alpine3.15

# Creer un repertoire pour l'application dans le conteneur
WORKDIR /app

# Créer le dossier /instance et donnez-lui les bonnes permissions
RUN mkdir -p ./instance && chmod -R 777 ./instance

# Copier le fichier requirements.txt dans le conteneur
COPY ./requirements.txt .
# Installer les dependances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier le reste de l'application
COPY . .

# Initialiser la base de données
RUN python -c "from srcinit_db import init_db; init_db()"

# Exposer le port 5010 pour que l'application puisse être accessible depuis l'extérieur du conteneur
EXPOSE 5010

# Lancer l'application avec gunicorn
CMD ["gunicorn", "-b", ":5010", "wsgi:app", "--timeout", "30000", "--workers", "1"]
