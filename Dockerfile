# Etape 1 : utiliser une image de base
FROM python:3.12-slim

# Etape 2 : Définir des variables d'environnement pour éviter les warnings et optimiser les performances
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Etape 3 : installer les dépendances nécessaires (ex. gcc, libpq-dev pour PostgreSQL)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*


# Etape 4 : Créer et définir le répertoire de travail
WORKDIR /app

# Etape 5 : Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt /app/

# Etape 6 : Installer les dépendances python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Etape 7 : Copier le code source dans le répertoire de travail
COPY . /app/

# Etape 8 : Exposer le port 8000 port par défaut de Django
EXPOSE 8000

# Etape 9 : Définir la commande de démarrage du conteneur
# CMD ["python", "webapp/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python webapp/manage.py runserver 0.0.0.0:8000"]

