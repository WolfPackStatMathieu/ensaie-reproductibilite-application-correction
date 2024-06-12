FROM ubuntu:22.04

# Définir le répertoire de travail
WORKDIR /app

# Installer Python et les dépendances
RUN apt-get -y update && \
    apt-get install -y python3-pip curl

# Copier et installer les dépendances du projet
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier les scripts et le code source
COPY train.py .
COPY src ./src
COPY api ./api
COPY run.sh .

# Debug : Vérifier que run.sh est bien copié et afficher son contenu
RUN ls -la /app && cat /app/run.sh

# Exécuter train.py pendant la construction de l'image
RUN python3 train.py

# Rendre le script exécutable
RUN chmod +x run.sh

# Lancer le script au démarrage du conteneur
CMD ["./run.sh"]

# Garder le conteneur en vie
ENTRYPOINT exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"