# Utilise l’image officielle Python
FROM python:3.12-slim

# Dossier de travail
WORKDIR /app

# Copie des fichiers
COPY . .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Port exposé (Cloud Run utilisera PORT)
ENV PORT 8080
EXPOSE 8080

# Lancer le serveur Flask
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
