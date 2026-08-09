# Daily Notes : TranscriBITE

## Présentation

Ce document contient le suivi quotidien de l'avancement du projet TranscriBITE.

Il permet de garder une trace des tâches réalisées, des décisions prises, des problèmes rencontrés et des prochaines étapes.

Chaque journée de développement sera ajoutée afin de maintenir une vision claire de l'évolution du projet.

---

# Jour 1 : Analyse et conception initiale

## Objectifs

* Comprendre le cahier des charges
* Définir les besoins fonctionnels et non fonctionnels
* Choisir les technologies adaptées
* Définir l'architecture générale du système

## Travaux réalisés

### Analyse fonctionnelle

Définition des fonctionnalités principales :

* Import de fichiers audio et vidéo
* Détection automatique du type de média
* Extraction audio avec FFmpeg
* Transcription locale avec Faster-Whisper
* Génération optionnelle de résumé avec Ollama
* Téléchargement des résultats

### Contraintes définies

* Fonctionnement local sans cloud
* Support audio et vidéo
* Compatibilité Windows
* Optimisation pour une machine CPU uniquement

### Choix technologiques

Backend :

* Python
* FastAPI

Frontend :

* React

Traitement multimédia :

* FFmpeg

Transcription :

* Faster-Whisper

Résumé :

* Ollama

## Décisions importantes

Définition d'une architecture séparée :

* Backend
* Frontend
* Storage
* Documentation
* Tests

---

# Jour 2 : Étude technique

## Objectifs

Comprendre les technologies utilisées avant le développement.

## Travaux réalisés

Étude de :

* FastAPI
* React
* Faster-Whisper
* FFmpeg
* Ollama
* WebSockets
* Formats audio et vidéo

## Résultats

Validation des choix techniques.

Compréhension du fonctionnement général :

Utilisateur

↓

Interface React

↓

API FastAPI

↓

Pipeline de traitement

↓

Résultat

---

# Jour 3 : Conception détaillée

## Objectifs

Finaliser l'organisation interne du projet.

## Travaux réalisés

Création de :

* Convention de nommage
* API Contract
* Organisation des dossiers
* Workflow Backend
* Workflow Frontend
* Responsabilités des modules

## Répartition des responsabilités

### Membre 1

Responsable de :

* Gestion des fichiers
* Upload
* Validation
* Analyse qualité
* FFmpeg
* Progression
* Download
* Interface Frontend

### Membre 2

Responsable de :

* Faster-Whisper
* Transcription
* Ollama
* Résumé
* Résultats IA

## Résultat

Dossier de conception terminé.

---

# Jour 4 : Validation de conception

## Objectifs

Vérifier la cohérence globale avant le développement.

## Travaux réalisés

* Vérification de l'architecture
* Vérification du workflow complet
* Ajustement des responsabilités
* Préparation du développement Backend

## Résultat

Architecture validée pour commencer l'implémentation.

---

# Jour 5 : Développement Backend : Fondations et Upload

## Objectifs

Créer la base du Backend et commencer le premier module fonctionnel.

## Travaux réalisés

* création de la structure Backend
    ```text
    backend/app/

    routers/

    services/

    schemas/

    models/

    utils/
    ```

* création des dossiers modules
* création des fichiers principaux
* préparation configuration
* création des enums pipeline
* préparation du module Upload

Création des fichiers principaux :

* main.py
* config.py
* requirements.txt
* .env
* .env.example

Création des dossiers de stockage :

* uploads
* outputs
* temp
* cache
* samples

## Module Upload

Travaux réalisés :

* Création de la route Upload
* Préparation de la validation des fichiers
* Gestion des extensions
* Gestion des types MIME
* Préparation du stockage
* Organisation du service fichier

## Résultat

Base Backend créée.

Module Upload préparé selon l'architecture prévue.

## Décisions importantes

* séparation routers/services/schemas/models/utils
* utilisation des enums pour les états du pipeline
* stockage séparé des fichiers utilisateurs

## Préparation suivante

Développement du Module Process.

---

# Jour 6 : Préparation du Module Process

## Objectifs actuels

Développement complet de l'architecture du module Process.

Construire le pipeline principal de traitement.

Création du routeur Process et du ProcessService.

Mise en place de l'orchestrateur principal du pipeline.

Construction des schémas ProcessingStatus, ProcessingStep et ProcessResponse.

Définition des états du pipeline.

Préparation de la validation des fichiers.

Préparation de la détection automatique Audio/Vidéo.

Préparation de la communication entre les différents services.

Préparation de la gestion centralisée des erreurs.

Préparation de l'architecture Logger.

Préparation de l'architecture des tests.

## Travaux réalisés

Analyse du rôle du module Process.

Définition des étapes officielles du pipeline :

```text
Upload

↓

Validation

↓

Détection du média

↓

Analyse qualité audio

↓

Extraction audio

↓

Transcription

↓

Génération résumé

↓

Préparation résultats

↓

Nettoyage

↓

Terminé

ou

Échoué
```

## Gestion des états

Définition d'une gestion centralisée avec des Enum.

Création :

```text
backend/app/enums/

pipeline_step.py

step_status.py

pipeline_order.py
```

## Objectifs suivants

* Création de process.py
* Création de process_service.py
* Gestion du pipeline
* Communication avec les services
* Gestion des erreurs
* Tests

---

# Jour 7 : Conception et développement du système de suivi de progression du pipeline

## Objectif de la journée

L'objectif principal de cette journée était de développer l'architecture du module Progress chargé du suivi de l'exécution du pipeline de traitement.

Ce module constitue un élément essentiel de TranscriBITE puisqu'il permettra au Backend de communiquer en temps réel avec le Frontend concernant l'état d'avancement d'un traitement.

L'objectif n'était pas uniquement d'afficher un pourcentage de progression, mais de construire une architecture complète capable d'être réutilisée par l'ensemble des modules du projet.

---

## Travaux réalisés

### Création du modèle ProcessingState

Le modèle `ProcessingState` a été créé afin de représenter l'état courant d'un traitement.

Il centralise notamment :

- l'identifiant du fichier traité
- l'étape actuelle du pipeline
- le statut de cette étape
- le pourcentage global de progression
- la date de début du traitement
- la date de fin
- les informations nécessaires au suivi du pipeline

Cette séparation permet de conserver une représentation unique de l'état d'un traitement.

---

### Développement du ProgressService

Le `ProgressService` a été conçu comme un service indépendant responsable exclusivement de la gestion de la progression.

Ses responsabilités sont les suivantes :

- mise à jour de l'étape courante
- modification du statut des étapes
- calcul automatique du pourcentage d'avancement
- préparation de l'état final
- centralisation de toutes les opérations liées au suivi de progression

Cette architecture respecte le principe de responsabilité unique (Single Responsibility Principle).

---

### Création du routeur Progress

Un nouveau routeur FastAPI (`progress.py`) a été ajouté.

Il permettra ultérieurement au Frontend de récupérer l'état d'avancement d'un traitement grâce à un identifiant de fichier.

L'API est volontairement indépendante afin de faciliter les futures évolutions vers un suivi en temps réel via Server-Sent Events (SSE) ou WebSocket.

---

### Intégration avec le ProcessService

Le ProcessService a été préparé afin de communiquer avec ProgressService.

L'orchestrateur principal du pipeline ne gère plus directement les calculs de progression.

Il délègue désormais ces responsabilités au module Progress, ce qui améliore fortement la modularité du projet.

---

### Calcul du pourcentage de progression

L'architecture permettant de calculer automatiquement le pourcentage d'avancement du pipeline a été préparée.

Le calcul repose sur les différentes étapes définies dans `PipelineStep`.

Cette approche garantit que toute évolution future du pipeline sera automatiquement prise en compte dans le calcul de progression.

---

### Préparation du suivi temps réel

Même si aucun mécanisme temps réel n'a encore été développé, toute l'architecture a été pensée afin de permettre ultérieurement :

- un rafraîchissement automatique du Frontend
- une communication via WebSocket
- une communication via Server-Sent Events (SSE)

Aucune modification importante de l'architecture ne sera nécessaire lors de cette évolution.

---

### Préparation des tests

Les fichiers de tests ont été créés afin de définir les futurs scénarios de validation du module.

Les implémentations seront réalisées pendant la phase officielle des tests prévue dans le planning.

---

## Difficultés rencontrées

La principale difficulté concernait la séparation des responsabilités entre ProcessService et ProgressService.

Une première approche consistait à laisser ProcessService gérer directement toutes les mises à jour de progression.

Cette solution aurait rapidement conduit à un service trop volumineux et difficile à maintenir.

Le choix a donc été fait de créer un service dédié exclusivement au suivi de progression.

---

## Décisions techniques

Les décisions suivantes ont été validées :

- séparation entre orchestration et progression
- création d'un service Progress indépendant
- utilisation du modèle ProcessingState comme représentation unique du suivi
- préparation de l'API Progress avant l'intégration du Frontend
- architecture compatible avec un fonctionnement temps réel

---

## Résultat obtenu

À la fin de cette journée, le backend possède désormais une architecture complète permettant de suivre l'avancement d'un traitement.

Cette architecture pourra être utilisée directement par les prochains modules (Download, Health, Quality Check) ainsi que par le Frontend lors de son développement.

---

# Jour 8

## Objectif

Développer le module Download responsable de la préparation des fichiers de sortie.

## Travaux réalisés

- Création de download.py
- Création de download_service.py
- Création de download_schema.py
- Développement de l'architecture Download
- Création de l'endpoint GET /download/{file_id}/{download_format}
- Mise en place de la validation des formats
- Préparation des téléchargements TXT
- Préparation des téléchargements JSON
- Préparation du téléchargement PDF
- Enregistrement du routeur dans FastAPI
- Préparation du Logger
- Préparation des tests

## Résultat

Le module Download est entièrement structuré et prêt à être connecté aux futurs modules de transcription et de résumé.

---

# Jour 9 — Partie 1

## Objectif

Développer le module Health afin de préparer la vérification de l'environnement du backend avant le lancement des traitements.

## Travaux réalisés

- Création de l'architecture du module Health
- création de health_schema.py
- création de health.py
- création de health_service.py
- création de HealthResponse
- création de HealthStatus
- création de l'endpoint GET /health
- préparation des vérifications Backend
- préparation des vérifications Configuration
- préparation des vérifications Storage
- préparation des vérifications FFmpeg
- intégration du routeur dans main.py
- préparation du Logger
- préparation des tests unitaires

## Résultat

Le module Health est entièrement structuré et prêt à recevoir l'implémentation des contrôles réels lors de la mise en place de l'environnement définitif (Python 3.12, FFmpeg, Faster-Whisper et Ollama).



## Module Quality

- Création du QualityService
- Définition de l'architecture complète du service `QualityService`
- Mise en place de l'orchestration de l'analyse audio
- Implémentation de la récupération de la taille du fichier
- Préparation des méthodes d'analyse (durée, débit, fréquence, canaux)
- Construction du rapport qualité
- Préparation des tests du module Quality

## Architecture

- Validation de l'utilisation de `Path` dans le QualityService
- Centralisation de la vérification de l'existence des fichiers dans `FileService`
- Harmonisation de l'architecture avec les autres services du projet

---

# Jour 10 : Préparation de l'environnement IA

## Objectif

Préparer et valider un environnement Python 3.12 unifié pour TranscriBITE afin de rendre le Backend prêt pour l'intégration des composants IA.

## Travaux réalisés

### Environnement Python

- Installation de Python 3.12.10
- Remplacement de l'utilisation de l'ancien environnement Python 3.10 du projet
- Conservation du Python système 3.14 indépendamment du projet
- Création de `backend/.venv` avec Python 3.12
- Activation et validation de l'environnement virtuel
- Résolution du blocage PowerShell lié à l'exécution des scripts

### Dépendances Backend et IA

- Vérification de FastAPI
- Vérification de Pydantic
- Vérification d'Uvicorn
- Installation et validation de Torch en environnement CPU
- Installation et validation de Faster-Whisper
- Génération de `requirements.txt` à partir de l'environnement virtuel
- Validation des principales dépendances présentes dans l'environnement

### FFmpeg

- Installation de FFmpeg sur le disque E
- Emplacement utilisé : `E:\FFmpeg files\bin`
- Ajout de FFmpeg au PATH système
- Validation avec `ffmpeg -version`
- Conservation de `FFMPEG_PATH=ffmpeg` dans `.env`

### Ollama

- Installation d'Ollama sur le disque E
- Emplacement utilisé : `E:\Users\Default\Ollama\ollama.exe`
- Ajout du dossier Ollama au PATH
- Validation avec `ollama --version`
- Validation avec `ollama list`
- Le serveur Ollama était déjà actif sur `127.0.0.1:11434`
- Aucun modèle Ollama n'a encore été installé à ce stade

### Variables d'environnement

Le fichier `.env` a été vérifié avec succès.

Variables principales utilisées :

- `APP_NAME=TranscriBITE`
- `APP_VERSION=1.0.0`
- `HOST=127.0.0.1`
- `PORT=8000`
- `UPLOAD_FOLDER=../storage/uploads`
- `OUTPUT_FOLDER=../storage/outputs`
- `TEMP_FOLDER=../storage/temp`
- `CACHE_FOLDER=../storage/cache`
- `LOG_FOLDER=../logs`
- `MAX_FILE_SIZE=500`
- `DEFAULT_LANGUAGE=auto`
- `FFMPEG_PATH=ffmpeg`
- `WHISPER_MODEL=base`

Le chargement des variables avec `python-dotenv` a été vérifié.

### Validation du Backend

Le Backend a été lancé avec Python 3.12 à l'aide de :

```text
python -m uvicorn app.main:app --reload
```

Les vérifications suivantes ont réussi :

- démarrage du serveur Uvicorn
- démarrage de l'application FastAPI
- requête `GET /` avec réponse `200 OK`
- accès à `GET /docs` avec réponse `200 OK`

La commande directe `uvicorn app.main:app --reload` a également été validée.

## Problèmes rencontrés

- `py` n'était pas reconnu initialement dans certains terminaux
- L'activation du `.venv` était bloquée par la politique d'exécution PowerShell
- FFmpeg n'était pas reconnu avant l'ajout de son dossier au PATH
- Ollama n'était pas reconnu avant l'ajout de son dossier au PATH
- Le téléchargement initial de Torch a rencontré une erreur SSL pendant le téléchargement
- Le serveur Ollama ne pouvait pas être démarré une deuxième fois car le port `11434` était déjà utilisé par une instance active

Ces problèmes ont été résolus sans modifier l'architecture applicative.

## Résultat

L'environnement Python 3.12 du projet est opérationnel.

Les livrables du Jour 10 sont validés :

- Environnement Python 3.12 unifié
- Environnement IA prêt pour l'intégration IA
- `requirements.txt` généré et validé
- Backend validé avec le nouvel environnement

## Préparation suivante

Le Jour 11 est consacré à la documentation technique complète et à la synchronisation des documents du projet.

# Jour 11

## Documentation technique

Cette journée a été consacrée à la consolidation de toute la documentation technique du projet TranscriBITE.

L'objectif principal était de synchroniser la documentation avec l'architecture et les développements réalisés jusqu'au Jour 9.

Les travaux effectués comprennent :

- révision de l'ensemble de la documentation existante
- harmonisation des différents documents techniques
- mise à jour du Workflow général
- mise à jour de l'architecture
- mise à jour des choix techniques
- mise à jour des décisions d'architecture
- finalisation du contrat d'API
- rédaction du plan de tests
- rédaction des cas de tests
- préparation du document des résultats de tests
- création du README principal du projet
- création du guide d'installation
- vérification de la cohérence entre le code et la documentation

Cette journée a permis d'obtenir une documentation homogène, structurée et prête à accompagner les prochaines phases de développement.

---

# Prochaines mises à jour

À chaque fin de module :

* ajouter les tâches réalisées
* ajouter les décisions prises
* ajouter les problèmes rencontrés
* ajouter les solutions appliquées

Les prochains ajouts prévus :

* Intégration Membre 2
* Interface React
