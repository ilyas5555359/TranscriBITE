# CHANGELOG

## Présentation

Ce document recense l'ensemble des évolutions apportées au projet TranscriBITE au cours du développement.

Chaque journée de travail présente les principaux modules développés, les nouvelles fonctionnalités ajoutées ainsi que les améliorations apportées à l'architecture du projet.

Il permet de suivre l'évolution du projet depuis le début du développement jusqu'à la version finale.

---

## Jour 5

### Structure Backend

- Création de l'architecture Backend
- Création de tous les dossiers
- Création des fichiers principaux
- Initialisation de FastAPI
- Développement du module Upload
- Validation des extensions
- Validation MIME
- Validation de la taille
- Génération des UUID
- Nettoyage des noms de fichiers
- Sauvegarde des fichiers
- Architecture du Logger
- Architecture des tests

---

## Jour 6

### Module Process

- Création de process.py
- Création de process_service.py
- Création de process_schema.py
- Création de l'architecture Process
- Initialisation des états de traitement
- Mise en place de la détection Audio/Vidéo
- Sélection automatique du pipeline
- Communication avec les autres services
- Préparation de la gestion centralisée des erreurs
- Préparation de l'architecture Logger
- Préparation de l'architecture des tests
- Enregistrement du routeur Process dans main.py

---

## Jour 7

### Module Progress

- Création de progress.py
- Création de progress_service.py
- Création de progress_schema.py
- Création de processing_state.py
- Développement de l'architecture du suivi de progression
- Mise en place de la gestion des états du traitement
- Calcul automatique du pourcentage de progression
- Préparation de l'estimation du temps de traitement
- Préparation des messages de progression
- Communication entre ProcessService et ProgressService
- Création de l'API de suivi de progression
- Préparation de l'architecture Logger
- Préparation de l'architecture des tests

---

## Jour 8

### Module Download

- Création de download.py
- Création de download_service.py
- Création de download_schema.py
- Création de l'architecture Download
- Préparation des téléchargements TXT
- Préparation des téléchargements JSON
- Préparation du futur téléchargement PDF
- Validation des formats de téléchargement
- Enregistrement du routeur Download dans main.py
- Préparation de l'architecture Logger
- Préparation de l'architecture des tests

---

## Jour 9

### Module Health

- Création de health.py
- Création de health_schema.py
- Création de health_service.py
- Développement de l'architecture Health
- Préparation des vérifications Backend
- Préparation des vérifications Configuration
- Préparation des vérifications Storage
- Préparation des vérifications FFmpeg
- Enregistrement du routeur Health dans main.py
- Préparation du Logger
- Préparation de l'architecture des tests

---

### Module Quality

- Définition de l'architecture du `QualityService`
- Création de quality_service.py
- Création de l'architecture Quality
- Analyse de la taille des fichiers
- Préparation de l'analyse de la durée
- Préparation de l'analyse du débit
- Préparation de l'analyse de la fréquence d'échantillonnage
- Préparation de l'analyse des canaux
- Construction du rapport qualité
- Centralisation de la validation des fichiers dans FileService avec `check_file_exists()`
- Préparation de l'analyse des caractéristiques audio
- Préparation de l'architecture des tests

---

## Jour 10

### Préparation de l'environnement IA

- Installation et validation de Python 3.12.10
- Création de l'environnement virtuel `backend/.venv`
- Validation de FastAPI, Pydantic et Uvicorn
- Installation et validation de Torch CPU
- Installation et validation de Faster-Whisper
- Installation et validation de FFmpeg
- Installation et validation d'Ollama
- Vérification des variables d'environnement
- Génération et validation de `requirements.txt`
- Test de lancement du Backend avec Python 3.12
- Validation des endpoints `/` et `/docs`

## Jour 11

### Documentation technique

- Vérification de la documentation d'architecture
- Mise à jour de l'architecture générale
- Mise à jour du Workflow global
- Mise à jour de la documentation API
- Mise à jour des choix techniques
- Mise à jour des problèmes et solutions
- Mise à jour des améliorations futures
- Mise à jour de `Architecture.md`
- Mise à jour de `Folder_Structure.md`
- Vérification de `Workflow_Processing.md`
- Mise à jour de `Technical_Decisions.md`
- Vérification de `API_Contract.md`
- Mise à jour de `Daily_Notes.md`
- Mise à jour de `Problems_and_Solutions.md`
- Vérification de `Technical_Choices.md`
- Vérification de la documentation des tests
- Rédaction du Test Plan
- Rédaction des Test Cases
- Préparation du Test Results
- Création du README principal
- Création du guide d'installation
- Vérification du Changelog
- Harmonisation de l'ensemble de la documentation

---
