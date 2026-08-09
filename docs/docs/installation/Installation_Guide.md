# Installation Guide — TranscriBITE

## Présentation

Ce document décrit l'environnement de développement actuellement validé pour TranscriBITE.

Le projet utilise un Backend Python/FastAPI isolé dans un environnement virtuel Python 3.12.

## 1. Environnement Python

Version validée :

```text
Python 3.12.10
```

L'environnement virtuel du Backend est situé dans :

```text
backend/.venv
```

Depuis `E:\TranscriBITE\backend` :

```powershell
py -3.12 -m venv .venv
```

Activation PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloque l'exécution des scripts, la politique d'exécution doit être traitée selon la configuration de la machine avant l'activation.

Vérification :

```powershell
python --version
```

Résultat attendu :

```text
Python 3.12.10
```

## 2. Dépendances Python

Les dépendances validées sont enregistrées dans :

```text
backend/requirements.txt
```

Le fichier a été généré depuis l'environnement virtuel :

```powershell
python -m pip freeze > requirements.txt
```

Installation reproductible :

```powershell
python -m pip install -r requirements.txt
```

## 3. FFmpeg

FFmpeg est installé sur le disque E dans :

```text
E:\FFmpeg files\bin
```

Le dossier `bin` est ajouté au PATH afin que la commande suivante soit disponible :

```powershell
ffmpeg -version
```

La configuration du projet conserve :

```text
FFMPEG_PATH=ffmpeg
```

dans `.env`.

## 4. Ollama

Ollama est installé localement dans :

```text
E:\Users\Default\Ollama\ollama.exe
```

Le dossier est accessible depuis le PATH.

Vérification :

```powershell
ollama --version
```

Vérification des modèles installés :

```powershell
ollama list
```

Le Jour 10, aucun modèle n'était encore installé.

Le serveur local utilise le port :

```text
127.0.0.1:11434
```

Si `ollama serve` indique que le port est déjà utilisé, cela signifie généralement qu'une instance Ollama est déjà active.

## 5. Variables d'environnement

Le Backend utilise un fichier `.env` dans `backend/`.

Les variables actuellement validées sont :

```text
APP_NAME=TranscriBITE
APP_VERSION=1.0.0
HOST=127.0.0.1
PORT=8000
UPLOAD_FOLDER=../storage/uploads
OUTPUT_FOLDER=../storage/outputs
TEMP_FOLDER=../storage/temp
CACHE_FOLDER=../storage/cache
LOG_FOLDER=../logs
MAX_FILE_SIZE=500
DEFAULT_LANGUAGE=auto
FFMPEG_PATH=ffmpeg
WHISPER_MODEL=base
```

Le chargement avec `python-dotenv` a été vérifié.

## 6. Lancement du Backend

Depuis `backend/` avec `.venv` activé :

```powershell
python -m uvicorn app.main:app --reload
```

Le lancement a été validé avec :

```text
Application startup complete.
GET / HTTP/1.1 200 OK
GET /docs HTTP/1.1 200 OK
```

L'API est disponible localement sur :

```text
http://127.0.0.1:8000
```

La documentation Swagger est disponible sur :

```text
http://127.0.0.1:8000/docs
```

## 7. Environnement commun

Les deux membres doivent utiliser Python 3.12 et un environnement de dépendances correspondant au `requirements.txt` validé.

Les détails de l'intégration des services IA seront traités lors de la phase d'intégration prévue au Jour 14.

## 8. État de validation

À la fin du Jour 10 :

- Python 3.12.10 : validé
- `.venv` : validé
- FastAPI : validé
- Pydantic : validé
- Uvicorn : validé
- Torch CPU : validé
- Faster-Whisper : validé
- FFmpeg : validé
- Ollama : validé
- `.env` : validé
- `requirements.txt` : généré et validé
- démarrage du Backend : validé

