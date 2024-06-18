FROM ubuntu:22.04

# Définir le répertoire de travail
WORKDIR ${HOME}/ensaie-reproductibilite-application-correction

# Installer Python et les dépendances
RUN apt-get -y update && \
    apt-get install -y python3-pip curl

# Copier et installer les dépendances du projet
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier les scripts et le code source
COPY . .

# Exécuter train.py pendant la construction de l'image
# RUN python3 train.py

# Rendre le script exécutable
RUN chmod +x run.sh

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]


