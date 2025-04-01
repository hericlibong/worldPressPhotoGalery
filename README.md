
---

# WorldPressPhotoGallery

<p align="center">
  <img src="media/worldpressphoto.PNG" alt="worldpressphoto" width="600" height="400">
</p>

**WorldPressPhotoGallery** is a web application designed for photojournalism enthusiasts. It allows users to view, select, and rate the most striking news images, highlighted for their photojournalistic impact.

Each week, we collect these emblematic images from major media outlets via **Scrapy** spiders. The collected data is then stored and displayed in **Django**, providing an interface where users can interact with the images, vote, and (soon) share their impressions.

## Main Features

- **Voting and Rating:** Registered users can vote for their favorite images (1 to 10 rating, or star rating).
- **Scraping with Scrapy:** Automatically gather fresh images from international publications.
- **Easy Setup:** Simple installation steps and environment configuration using `.env`.

## Technology Stack

- **Scrapy** (spiders for each media source)  
- **Django** (models, views, templates)  
- **SQLite3** database (by default)  
- **python-decouple** for environment variables  

## Supported Media (examples)

- Washington Post, CNN, Guardian, The Week, etc.  
- These often source from AP, Reuters, AFP, and other agencies.

---

## Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/hericlibong/worldPressPhotoGalery
cd worldPressPhotoGalery
```

### 2. Create & activate a virtual environment

```bash
python -m venv venv
```

- **On Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **On Unix/macOS**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

1. Copy (or rename) the sample file to `.env`:
   ```bash
   cp .env.sample .env
   ```
2. In **`.env`**, define at least:
   ```text
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ```
   *(For local development, `DEBUG=True` is fine; in production, you can set it to `False` and adjust accordingly.)*

### 5. Scrape the latest images

```bash
python runspiders.py
```
This will launch the Scrapy spiders that gather images from supported media outlets and store them in the local SQLite database.

### 6. Run the Django server

From the `webapp` directory (or wherever your `manage.py` is located):

```bash
cd webapp
python manage.py runserver
```

### 7. Access the application

Open your web browser and go to:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
You can now browse through and rate the photojournalistic images!

---

## Screenshots

<p align="center">
  <img src="media/worldpressphoto_rated.PNG" alt="worldpressphoto-rated" width="600" height="400">
</p>

---

## Roadmap & Further Development

- **Refactoring** (splitting apps, improving pipeline, etc.)  
- **Dockerization**  
- **PhotoQuiz** (a quiz feature under development)  
- **Extended Media** (more spiders)  
- **CI/CD** (tests, GitHub Actions)

---

## Contributing

1. Fork the repository  
2. Create a branch (`git checkout -b feature/my-feature`)  
3. Commit your changes (`git commit -m "Add my feature"`)  
4. Push to the branch (`git push origin feature/my-feature`)  
5. Open a Pull Request

---


Voici un schéma résumé du flux, avec les principales étapes et quelques explications :

```
        ┌─────────────────────────────┐
        │ Collecte des données via    │
        │       Scrapy (spiders)      │
        └─────────────┬───────────────┘
                      │
                      │
                      ▼
        ┌─────────────────────────────┐
        │ Export des items en fichiers│
        │       JSON (via -O option)  │
        │   dans le dossier json_datas│
        └─────────────┬───────────────┘
                      │
                      │
                      ▼
        ┌─────────────────────────────┐
        │  Management Command Django  │
        │   (import_photos)           │
        │   lit les fichiers JSON     │
        └─────────────┬───────────────┘
                      │
                      │
                      ▼
        ┌─────────────────────────────┐
        │  Insertion via ORM dans     │
        │  les modèles Django         │
        │  (PhotoGallery, etc.)       │
        └─────────────┬───────────────┘
                      │
                      │
                      ▼
        ┌─────────────────────────────┐
        │  Base de données Django     │
        │ (SQLite, ou plus tard,       │
        │  PostgreSQL, etc.)          │
        └─────────────────────────────┘
```

**Explications complémentaires :**

1. **Scrapy** récupère et collecte les données grâce à ses spiders.
2. Chaque spider exporte automatiquement ses items au format JSON dans le dossier `json_datas/` (chaque spider génère son propre fichier, par exemple `guardian_picture.json`).
3. Une commande Django (`import_photos`) parcourt le dossier (ou un fichier spécifique) pour lire les fichiers JSON.
4. Pour chaque item lu, la commande utilise la méthode `update_or_create()` pour insérer ou mettre à jour les enregistrements dans le modèle `PhotoGallery`.
5. Les données finissent dans la base de données de l’application Django, prêtes à être utilisées par l’interface ou une API REST ultérieure.

Ce schéma illustre la décomposition du flux en deux parties distinctes :  
- **Collecte et export** (Scrapy et fichiers JSON)  
- **Import et insertion** (Commande Django et ORM)


---

## Docker Setup and Deployment

This project includes Docker configuration to simplify local development and deployment. Below are the steps and details to build and run the application using Docker.

### Files

- **Dockerfile**  
  Defines the Docker image for the application. It:
  - Uses the official Python 3.12-slim base image.
  - Sets environment variables to optimize performance.
  - Installs required system packages (e.g., gcc, libpq-dev, libffi-dev).
  - Installs Python dependencies from `requirements.txt`.
  - Copies the source code into the container.
  - Exposes port 8000.
  - Sets the command to start the Django development server.

- **docker-compose.yml**  
  Orchestrates multiple services (by default, only the web service is active for SQLite usage). It:
  - Builds the Docker image using the Dockerfile.
  - Maps the container port 8000 to a port on the host (e.g., 8001 if configured).
  - Loads environment variables from the non-versioned `.env` file via `env_file`.
  - (Optionally) Includes a PostgreSQL service, which can be activated by modifying the environment variables and uncommenting the db section.

### How to Use

1. **Prepare your environment:**
   - Ensure Docker Engine and docker-compose are installed on your system.
   - Create a `.env` file at the root of the project (it should not be versioned) with your environment variables. For example:

     ```dotenv
     SECRET_KEY=django-insecure-#@f-i=h_px68s=vjtj=xo%@_0wl5uk&*kweft2531j1-a(-b^o
     DEBUG=True
     ```

2. **Build and run the containers:**
   - From the root of your project, run:
     ```bash
     docker-compose up --build
     ```
   - This command will build the Docker image and start the web service (and the database service if activated). By default, the Django development server is started with the command:
     ```bash
     python webapp/manage.py runserver 0.0.0.0:8000
     ```

3. **Access the Application:**
   - Open your web browser and go to `http://localhost:8000` (or the host port specified in your docker-compose.yml) to view the application.

4. **Notes for Developers:**
   - The default configuration uses **SQLite** for the database. If you wish to test PostgreSQL, modify the environment variables in the docker-compose file and uncomment the `db` service section.
   - All secrets (like `SECRET_KEY`) are managed via the `.env` file. This file is not versioned to ensure sensitive data is not exposed.
   - To run management commands inside the container (for example, migrations), you can use:
     ```bash
     docker-compose exec web python webapp/manage.py migrate
     ```
   - When deploying to production, consider switching from the Django development server (`runserver`) to a production-ready server (like Gunicorn) and reviewing your settings accordingly.

---




## License

This project uses the **MIT License** (or whichever you prefer).  

You’re free to modify the code, propose new features, or adapt it to your needs!

---

_Keep in mind this README can evolve as the project grows. For any questions or issues, feel free to open an Issue on GitHub._