FROM python:3.12-alpine3.19

# Créer un utilisateur non-root
RUN adduser -D appuser

# Créer un répertoire pour l'application et donner les permissions
WORKDIR /app
RUN mkdir -p ./instance && chown -R appuser:appuser /app

# Copier uniquement les fichiers nécessaires pour l'installation des dépendances
COPY requirements.txt .

# Installer les dépendances et nettoyer
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copier le reste de l'application
COPY --chown=appuser:appuser . .

# Initialiser la base de données
RUN python -c "from src.init_db import init_db; init_db()"

# Changer vers l'utilisateur non-root
USER appuser

# Exposer le port 5010
EXPOSE 5010

# Lancer l'application avec gunicorn
CMD ["gunicorn", "-b", ":5010", "wsgi:app", "--timeout", "30000", "--workers", "1"]
