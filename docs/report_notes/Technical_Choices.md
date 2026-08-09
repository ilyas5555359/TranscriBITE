# Technical Choices

Ce document regroupe les principales décisions techniques prises durant le développement de TranscriBITE ainsi que leurs justifications.

---

# Jour 5

## Architecture Backend

### Choix

Séparer l'application en modules indépendants.

### Justification

Cette architecture facilite la maintenance, les tests et le travail collaboratif entre les deux membres.

---

## Utilisation de FastAPI

### Choix

Développer l'API REST avec FastAPI.

### Justification

FastAPI offre de très bonnes performances, une documentation automatique et une excellente intégration avec Pydantic.

---

## UUID

### Choix

Attribuer un identifiant UUID à chaque fichier importé.

### Justification

Garantit l'unicité des fichiers et évite les conflits de noms.

---

# Jour 6

## ProcessService comme orchestrateur

### Choix

Centraliser tout le pipeline dans ProcessService.

### Justification

Chaque service reste responsable d'une seule tâche tandis que ProcessService coordonne leur exécution.

---

## Architecture asynchrone

### Choix

Utiliser des méthodes `async`.

### Justification

Les traitements réalisés (lecture de fichiers, FFmpeg, IA, téléchargements) sont principalement des opérations d'entrée/sortie. L'utilisation de `async` prépare l'application à gérer ces opérations efficacement et reste cohérente avec FastAPI.

---

## Méthodes privées

### Choix

Découper le pipeline en méthodes privées (`_initialize_processing`, `_validate_file`, `_detect_media_type`, etc.).

### Justification

Cette organisation améliore la lisibilité, facilite les tests unitaires et simplifie les futures évolutions.

---

## Architecture préparée avant implémentation

### Choix

Définir l'ensemble des méthodes du pipeline avant de développer leur logique métier.

### Justification

Cette approche stabilise l'architecture, réduit les risques de refactoring importants et facilite l'intégration avec les modules développés par les deux membres.

---

# Jour 7

## Module Progress

### Pourquoi un ProgressService ?

Le suivi de progression a été isolé dans un service indépendant afin de respecter le principe de responsabilité unique (Single Responsibility Principle).

Cette architecture facilite :

- la maintenance
- les tests unitaires
- la communication avec le Frontend
- l'évolution vers un suivi temps réel (SSE ou WebSocket)

Le ProcessService reste uniquement responsable de l'orchestration globale du pipeline.

## Séparation du suivi de progression

### Choix

Créer un `ProgressService` indépendant du `ProcessService`.

### Justification

Le ProcessService conserve uniquement le rôle d'orchestrateur tandis que ProgressService devient responsable de la gestion complète du suivi de progression. Cette séparation améliore la modularité et facilite les évolutions futures.

---

## Centralisation de l'état du traitement

### Choix

Créer le modèle `ProcessingState` pour représenter l'état d'un traitement.

### Justification

Toutes les informations relatives à la progression sont regroupées dans une seule structure. Cette approche facilite la communication entre les différents modules ainsi que l'intégration future avec le Frontend.

---

## Calcul automatique de la progression

### Choix

Calculer le pourcentage d'avancement à partir des étapes définies dans `PipelineStep`.

### Justification

Le calcul devient indépendant du nombre d'étapes du pipeline. Toute modification future du pipeline sera automatiquement prise en compte sans modifier la logique principale.

---

## Préparation du suivi temps réel

### Choix

Construire dès maintenant une architecture compatible avec un suivi temps réel.

### Justification

Même si les Server-Sent Events (SSE) ou WebSockets seront intégrés plus tard, l'architecture actuelle évite tout refactoring important lors de cette évolution.

---

# Jour 8

## Module Download indépendant

### Choix

Créer un module Download totalement indépendant du pipeline.

### Justification

La génération des fichiers de sortie est isolée afin de simplifier la maintenance et permettre l'ajout futur de nouveaux formats sans modifier le ProcessService.

---

## Préparation des formats de téléchargement

### Choix

Prévoir dès maintenant les téléchargements TXT, JSON et PDF.

### Justification

Les formats TXT et JSON seront développés progressivement tandis que l'architecture est déjà prête pour intégrer le PDF sans refactoring.

---

# Jour 9

## Création de HealthService

### Choix

Créer un service dédié pour centraliser toutes les vérifications du système.

### Justification

Le routeur Health reste léger tandis que toute la logique métier est centralisée dans HealthService.

Cette décision conserve une architecture homogène avec les autres modules Backend.

---

## Préparation des vérifications

### Choix

Préparer les différentes vérifications sous forme de méthodes privées indépendantes.

### Justification

Chaque contrôle pourra évoluer indépendamment sans modifier l'architecture générale du module.

---

## Séparation de la validation de l'existence du fichier

### Choix

Centraliser la vérification de l'existence des fichiers dans `FileService` via la fonction `check_file_exists()`.

### Justification

La validation de l'existence d'un fichier relève de la responsabilité du module de gestion des fichiers et non du `QualityService`. Cette approche évite la duplication du code et permet à tous les services de réutiliser la même logique de validation.

---

## Architecture du QualityService

### Choix

Organiser `QualityService` comme un orchestrateur composé de plusieurs méthodes privées spécialisées.

### Justification

Chaque caractéristique audio (durée, taille, débit, fréquence d'échantillonnage et nombre de canaux) est analysée indépendamment avant la génération d'un rapport global. Cette architecture facilite les tests unitaires et les évolutions futures.

---

# Jour 9

## Analyse audio avec Path

### Choix

Utiliser directement le chemin du fichier (`Path`) dans le QualityService.

### Justification

Le service manipule un fichier physique. Cette approche évite d'introduire une logique de résolution UUID → Path qui relève du ProcessService.

---

## Vérification centralisée des fichiers

### Choix

Placer `check_file_exists()` dans FileService.

### Justification

Toutes les opérations liées aux fichiers sont regroupées dans un seul service, ce qui améliore la réutilisabilité et limite la duplication de code.


# Jour 10

## Python 3.12 dédié au projet

### Choix

Utiliser Python 3.12 dans un environnement virtuel `backend/.venv` pour TranscriBITE.

### Justification

Cette approche permet d'isoler les dépendances du projet du Python système et d'assurer un environnement reproductible pour les deux membres. Le Python système peut rester sur une autre version sans modifier l'environnement du projet.

## Génération de requirements.txt depuis le .venv

### Choix

Générer `requirements.txt` à partir des paquets réellement installés dans l'environnement virtuel.

### Justification

Le fichier reflète l'environnement effectivement validé pendant le Jour 10 et permet de reproduire les dépendances du Backend.

## FFmpeg accessible par le PATH

### Choix

Utiliser `FFMPEG_PATH=ffmpeg` plutôt qu'un chemin absolu dans `.env`.

### Justification

Le chemin absolu dépendrait de la machine. L'utilisation du PATH rend la configuration plus portable tout en permettant au Backend d'appeler FFmpeg.

## Ollama installé comme service local

### Choix

Utiliser Ollama comme composant local pour la future génération de résumé.

### Justification

Ollama respecte l'architecture offline du projet. L'installation et la communication locale ont été vérifiées, tandis que le choix et le téléchargement du modèle restent liés à l'intégration IA.

## Environnement commun pour les deux membres

### Choix

Les deux membres doivent utiliser Python 3.12 et un environnement de dépendances équivalent au `requirements.txt` validé.

### Justification

Cette règle limite les différences d'environnement et réduit les problèmes lors de l'intégration du travail IA du Membre 2.
