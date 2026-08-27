# TranscriBITE

## Présentation

TranscriBITE est une application locale de transcription audio et vidéo développée dans le cadre d'un projet de stage.

L'objectif du projet est de proposer une plateforme capable de transformer automatiquement des fichiers audio ou vidéo en texte, puis de générer un résumé du contenu grâce à l'intelligence artificielle, tout en fonctionnant entièrement en local.

Aucune donnée n'est envoyée vers un service Cloud.

---

# Objectifs

Les principaux objectifs de TranscriBITE sont :

- importer des fichiers audio ou vidéo
- détecter automatiquement le type de média
- extraire l'audio des vidéos
- analyser les caractéristiques du média
- produire une transcription
- générer un résumé (optionnel)
- permettre le téléchargement des résultats

---

# Fonctionnalités

## Upload

- Import de fichiers audio
- Import de fichiers vidéo
- Validation des extensions
- Validation des types MIME
- Validation de la taille
- Génération d'un identifiant UUID
- Sauvegarde des fichiers

---

## Pipeline

Le traitement est entièrement automatisé.

Étapes principales :

1. Upload
2. Validation
3. Détection Audio/Vidéo
4. Analyse qualité
5. Extraction audio (si nécessaire)
6. Transcription
7. Génération du résumé
8. Préparation des résultats
9. Téléchargement

---

## Progression

Le suivi du traitement permet d'afficher :

- l'étape actuelle
- le statut
- le pourcentage
- les messages de progression

---

## Téléchargement

Formats disponibles :

- TXT
- JSON
- PDF

---

# Architecture

Le projet est organisé autour d'une architecture modulaire.

```text
Frontend React

↓

API FastAPI

↓

ProcessService

↓

Services spécialisés

↓

Résultats
```

Les principaux services sont :

- FileService
- ProcessService
- ProgressService
- AudioService
- QualityService
- TranscriptionService
- SummaryService
- DownloadService
- HealthService

---

# Technologies

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

---

## Intelligence Artificielle

- Faster-Whisper
- Ollama

---

## Traitement multimédia

- FFmpeg

---

## Frontend

- React
- JavaScript

---

# Structure du projet

```text
backend/
frontend/
storage/
docs/
logs/
scripts/
tests/
```

La structure détaillée est décrite dans :

```
docs/architecture/Folder_Structure.md
```

---

# Documentation

La documentation du projet est disponible dans :

```
docs/
```

Elle comprend notamment :

- Architecture
- Workflow
- API Contract
- Documentation technique
- Documentation des tests
- Changelog

---

# Tests

Les tests sont organisés dans :

```text
tests/

backend/

frontend/
```

Les campagnes de tests sont documentées dans :

- Test_Plan.md
- Test_Cases.md
- Test_Results.md

---

# Équipe

## Membre 1

Responsabilités :

- Upload
- Validation
- Process
- Progress
- Download
- Health
- Quality
- Frontend
- Documentation
- Architecture

---

## Membre 2

Responsabilités :

- Faster-Whisper
- Transcription
- Ollama
- Résumé
- Modules IA

---

# État du projet

Le projet est développé progressivement selon un planning de réalisation en plusieurs phases :

- Conception
- Développement Backend
- Documentation
- Git & GitHub
- UML
- Intégration
- Frontend
- Tests
- Optimisation
- Finalisation

---

# Licence

Ce projet est distribué sous la licence définie dans le fichier `LICENSE`.
