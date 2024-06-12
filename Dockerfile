FROM ubuntu:22.04

# Définir le répertoire de travail
WORKDIR /app

# Installer Python et les dépendances
RUN apt-get -y update && \
    apt-get install -y python3-pip

# Copier et installer les dépendances du projet
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier les scripts et le code source
COPY train.py .
COPY src ./src
COPY api ./api


# Exécuter train.py pendant la construction de l'image
RUN python3 train.py

# Rendre le script exécutable
RUN chmod +x run.sh

# Lancer le script au démarrage du conteneur
CMD [".api/run.sh"]
