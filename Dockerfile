FROM ubuntu:22.04

# Définir le répertoire de travail
WORKDIR ${HOME}/titanic

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

# Donner les permissions d'exécution au script run.sh
RUN chmod +x ./api/run.sh

# Lancer le script run.sh au démarrage du conteneur
CMD ["bash", "-c", "./api/run.sh"]
