# Étape 1 : Image de base légère avec Python 3.12
FROM python:3.12-slim

# Étape 2 : Variables d’environnement recommandées pour Django
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Étape 3 : Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Étape 4 : Définir le répertoire de travail
WORKDIR /app

# Étape 5 : Copier le fichier requirements.txt en premier (optimise le cache Docker)
COPY requirements.txt .

# Étape 6 : Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Étape 7 : Copier le reste de l’application dans le conteneur
COPY . .

# Étape 8 : Collecter les fichiers statiques avec Django (⚠️ après COPY)
RUN python webapp/manage.py collectstatic --noinput

# Étape 9 : Exposer le port utilisé par Django
EXPOSE 8000

# Étape 10 : Démarrer l’application avec gunicorn pour la prod (meilleure pratique)
# CMD ["gunicorn", "gallery.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["gunicorn", "webapp.gallery.wsgi:application", "--bind", "0.0.0.0:8000"]


