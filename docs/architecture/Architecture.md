Objectif du document

Ce document répond à une seule question : Comment est organisée l'application TranscriBITE ?

# Architecture de TranscriBITE

## 1. Présentation

TranscriBITE est une application locale (offline) destinée à la transcription automatique de fichiers audio et vidéo à l'aide de modèles d'intelligence artificielle exécutés localement.

L'objectif principal est de permettre à un utilisateur d'importer un fichier audio ou vidéo, de lancer son traitement manuellement, puis d'obtenir une transcription textuelle. Selon la configuration retenue, un résumé pourra également être généré à partir de cette transcription.

L'application est conçue selon une architecture modulaire afin de faciliter son développement, sa maintenance et son évolution. Chaque fonctionnalité est regroupée dans un module indépendant ayant une responsabilité clairement définie.

Le projet est développé en séparant le Frontend et le Backend afin de respecter une architecture moderne de type client/serveur.



## 2. Objectifs

L'architecture de TranscriBITE a été conçue afin de répondre aux objectifs suivants :

* Concevoir une application entièrement locale (offline), sans dépendance à un service Cloud.
* Séparer clairement le Frontend et le Backend afin de faciliter le développement, la maintenance et les évolutions futures.
* Organiser le Backend en modules indépendants ayant chacun une responsabilité unique.
* Permettre l'intégration de différents services d'intelligence artificielle (transcription et génération de résumé) sans modifier l'architecture globale.
* Assurer une communication claire entre les différents modules grâce à des contrats d'API et des modèles de données bien définis.
* Faciliter les tests unitaires et les tests d'intégration en limitant les dépendances entre les modules.
* Préparer une architecture évolutive permettant l'ajout de nouvelles fonctionnalités (nouveaux formats de fichiers, nouveaux modèles d'IA, nouveaux types d'export, etc.).
* Garantir une bonne lisibilité du projet grâce à une organisation rigoureuse des dossiers et des responsabilités.



## 3. Architecture générale

L'application TranscriBITE repose sur une architecture client/serveur organisée autour de deux composants principaux :

* **Frontend** : développé avec React, il constitue l'interface utilisateur. Il permet d'importer un fichier, de lancer le traitement, de suivre la progression et d'afficher les résultats.

* **Backend** : développé avec FastAPI, il centralise toute la logique métier. Il reçoit les requêtes du Frontend, orchestre les différentes étapes du traitement et communique avec les différents services.

Le Backend est lui-même découpé en plusieurs modules spécialisés afin de respecter le principe de responsabilité unique. Chaque module réalise une tâche précise (gestion des fichiers, analyse, traitement, téléchargement, suivi de progression, etc.).

Les fichiers importés, les fichiers temporaires ainsi que les résultats générés sont stockés dans une arborescence dédiée afin de séparer clairement les données de l'application du code source.

Cette architecture modulaire facilite la maintenance, les tests, les évolutions futures ainsi que le travail collaboratif entre les deux membres du projet.



## 4. Architecture Backend

Le Backend de TranscriBITE est développé avec **FastAPI** et suit une architecture modulaire. En suivons le principe de responsabilité unique (Single Responsibility Principle) chaque dossier possède une responsabilité précise afin de garantir une bonne organisation du code et de faciliter la maintenance.

### Routers

Le dossier `routers` contient les points d'entrée de l'API. Chaque route reçoit les requêtes du Frontend, valide les données reçues et délègue le traitement aux services correspondants.

### Services

Le dossier `services` regroupe la logique métier de l'application. Chaque service réalise une tâche spécifique, comme la gestion des fichiers, l'analyse de la qualité audio, l'extraction audio, la transcription, la génération du résumé, le téléchargement des résultats ou le suivi de la progression.

### Schemas

Le dossier `schemas` contient les modèles Pydantic utilisés pour valider les données échangées entre le Frontend et le Backend. Ils servent également à documenter automatiquement les API.

### Models

Le dossier `models` regroupe les structures internes utilisées par l'application pour représenter les informations manipulées pendant le traitement.

### Utils

Le dossier `utils` rassemble les fonctions utilitaires communes utilisées par plusieurs modules, notamment les validateurs, les outils de gestion des fichiers, les fonctions liées à FFmpeg, les fonctions liées à Faster-Whisper et les outils de journalisation.

### Enums

Le dossier `enums` centralise les énumérations utilisées dans le projet, notamment les étapes du pipeline (`PipelineStep`), les statuts des étapes (`StepStatus`) ainsi que l'ordre officiel d'exécution (`PIPELINE_ORDER`). Cette approche garantit une cohérence entre tous les modules du Backend et facilite leur maintenance.

L'ensemble de ces composants permet de séparer clairement les responsabilités de chaque partie du Backend tout en conservant une architecture évolutive et facilement testable.

### Module Upload

Le module Upload est responsable de la réception, de la validation et de la sauvegarde des fichiers importés par l'utilisateur.

Il constitue le point d'entrée du pipeline de traitement en s'assurant que les fichiers respectent les contraintes définies par le système avant leur prise en charge.

Les principales opérations réalisées comprennent notamment :

- la réception du fichier
- la validation des extensions autorisées
- la validation du type MIME
- la validation de la taille maximale
- la génération d'un identifiant UUID
- le nettoyage du nom du fichier
- la sauvegarde dans le dossier de stockage

Comme les autres modules Backend, le routeur `upload.py` délègue toute la logique métier au `FileService`.

### Module Process

Le module Process constitue l'orchestrateur principal du backend.

Il coordonne l'ensemble du pipeline de traitement en communiquant avec les différents services spécialisés sans contenir directement la logique métier.

Le pipeline est volontairement découpé en plusieurs méthodes privées afin de respecter le principe de responsabilité unique et de faciliter les futures évolutions.

### Module Progress

Le module Progress est responsable du suivi de l'avancement d'un traitement en cours.

Il centralise les informations liées à l'état du pipeline afin de permettre au Frontend de connaître à tout moment la progression du traitement.

Les informations suivies comprennent notamment :

- l'étape actuelle du pipeline
- le statut d'exécution
- le pourcentage d'avancement
- le message utilisateur
- les dates de début et de dernière mise à jour

Le module repose sur le modèle `ProcessingState`, qui représente l'état courant d'un traitement.

Comme les autres modules Backend, le routeur `progress.py` délègue toute la logique métier au `ProgressService`.

### Module Download

Le module Download est responsable de la préparation et de l'export des résultats générés par le pipeline de traitement.

Il permet de récupérer les fichiers produits par l'application dans différents formats tout en vérifiant leur disponibilité avant le téléchargement.

Les formats actuellement prévus sont :

- TXT
- JSON

L'architecture est également préparée pour intégrer de futurs formats d'export, notamment le PDF.

Comme les autres modules Backend, le routeur `download.py` délègue toute la logique métier au `DownloadService`.

### Module HealthService

Le module Health est chargé de vérifier que l'environnement d'exécution est opérationnel avant le lancement d'un traitement.

Il centralise les vérifications suivantes :

- disponibilité du Backend
- validité de la configuration
- disponibilité des dossiers de stockage
- disponibilité de FFmpeg

Comme les autres modules du projet, le routeur FastAPI délègue toute la logique métier au service `HealthService`.

---

## Module Health

Le module Health est responsable de vérifier l'état général du Backend.

Il contrôle notamment :

- l'état du Backend
- la configuration
- les dossiers de stockage
- la disponibilité de FFmpeg

Le routeur Health expose ces informations via une API dédiée.

---

## Module Quality

Le module Quality est responsable de l'analyse technique des fichiers audio.

Il permet notamment de récupérer :

- la durée
- la taille du fichier
- le débit audio
- la fréquence d'échantillonnage
- le nombre de canaux

Le service construit ensuite un rapport qualité destiné au pipeline de traitement.

Le module travaille directement avec le chemin physique du fichier (`Path`), fourni par le ProcessService.

---

## Environnement d'exécution

Le Backend de TranscriBITE utilise Python 3.12 comme version de référence.

L'environnement virtuel du Backend est situé dans :

```text
backend/.venv
```

### `.venv`

Environnement virtuel Python utilisé par le Backend.

Il contient les dépendances nécessaires au fonctionnement de l'application et doit rester séparé de l'installation Python globale.

Le dossier `.venv` n'est pas destiné à être versionné dans Git.



## 5. Architecture Frontend

Le Frontend de TranscriBITE est développé avec **React**. Il fournit une interface utilisateur simple, claire et modulaire permettant de piloter l'ensemble du processus de transcription.

L'organisation du Frontend repose sur plusieurs dossiers spécialisés :

### Assets

Le dossier `assets` regroupe les ressources graphiques de l'application, notamment le logo, les icônes et les images utilisées dans l'interface.

### Components

Le dossier `components` contient les composants réutilisables de l'application. Chaque composant possède une responsabilité précise, comme l'import d'un fichier, la sélection de la langue, le bouton de démarrage du traitement, l'affichage de la progression, la visualisation de la transcription, du résumé ou des messages d'erreur.

### Pages

Le dossier `pages` regroupe les pages principales de l'application. À ce stade du projet, une page principale (`Home`) centralise les différents composants de l'interface.

### Services

Le dossier `services` regroupe les fonctions de communication avec le Backend. Il est responsable de l'envoi des requêtes HTTP ainsi que de la réception des réponses provenant de l'API FastAPI.

### Styles

Le dossier `styles` contient les feuilles de style communes utilisées dans toute l'application afin d'assurer une présentation cohérente et facilement maintenable.

Cette architecture favorise la réutilisation des composants, limite les duplications de code et facilite les évolutions futures de l'interface utilisateur.



## 6. Architecture du stockage des données

Afin de garantir une organisation claire des données manipulées par l'application, TranscriBITE sépare le code source des fichiers générés pendant le traitement.

Le dossier `storage` centralise l'ensemble des fichiers utilisés par le pipeline.

### uploads

Ce dossier contient les fichiers importés par l'utilisateur. Les fichiers y sont enregistrés après validation et renommage afin de garantir leur unicité et d'éviter les conflits de noms.

### outputs

Ce dossier contient les résultats générés par l'application, notamment les transcriptions et les résumés qui pourront être téléchargés par l'utilisateur.

### temp

Ce dossier est réservé aux fichiers temporaires créés pendant le traitement, par exemple lors de l'extraction audio d'une vidéo. Son contenu est supprimé à la fin du traitement.

### cache

Ce dossier est destiné aux fichiers pouvant être réutilisés afin d'améliorer les performances de l'application. Son utilisation pourra évoluer selon les besoins du projet.

### samples

Ce dossier contient des fichiers de test utilisés pendant le développement et la validation de l'application.

### Logs

Les journaux d'exécution sont enregistrés dans un dossier dédié (`logs`). Ils permettent de suivre le fonctionnement de l'application, de faciliter le débogage et d'analyser les éventuelles erreurs.

Les principaux journaux prévus sont :

* `application.log` : événements généraux de l'application.
* `ffmpeg.log` : opérations liées à FFmpeg.
* `whisper.log` : informations relatives au moteur de transcription.
* `errors.log` : erreurs rencontrées pendant l'exécution.

Cette organisation permet d'isoler les données de travail, les résultats et les fichiers temporaires, tout en facilitant les opérations de maintenance et de nettoyage.



## 7. Communication des modules

La communication entre les différents composants de TranscriBITE suit une organisation en couches afin de séparer clairement les responsabilités.

### Communication Frontend / Backend

Le Frontend React communique avec le Backend FastAPI à travers des API HTTP.

Le Frontend est responsable de :

* l'interaction avec l'utilisateur ;
* l'import des fichiers ;
* le lancement du traitement ;
* l'affichage de la progression ;
* l'affichage des résultats.

Le Backend est responsable de :

* la validation des requêtes ;
* l'orchestration du pipeline ;
* l'exécution des traitements ;
* la gestion des erreurs ;
* la préparation des résultats.

Architecture de communication :

```text
Utilisateur
     |
     v
Frontend React
     |
     | HTTP API
     v
Backend FastAPI
     |
     v
Routers
     |
     v
Services métier
     |
     v
Stockage / Services IA
```

### Communication interne du Backend

Le Backend utilise une architecture orientée services.

Les routers ne contiennent pas la logique métier. Ils délèguent les traitements aux services correspondants.

Exemple :

```text
Upload Router
      |
      v
File Service
      |
      v
Storage
```

Pour le traitement principal :

```text
Process Router
      |
      v
Process Service
      |
      +--> Quality Service
      |
      +--> Audio Service
      |
      +--> Transcription Service
      |
      +--> Summary Service
      |
      +--> Progress Service
```

### Gestion du pipeline

Le module Process agit comme orchestrateur principal. Il contrôle l'ordre d'exécution des différentes étapes du traitement.

Le déroulement global est :

```text
Upload
  |
Validation
  |
Détection du média
  |
Analyse qualité audio
  |
Extraction audio
  |
Transcription
  |
Génération résumé
  |
Préparation résultats
  |
Nettoyage
  |
Terminé
```

En cas d'erreur durant une étape, l'état du pipeline passe à `Échec` et l'erreur est enregistrée dans les logs.

Cette organisation permet de remplacer ou modifier un service sans modifier l'ensemble du système.



## 8. Répartition des responsabilités

Le développement de TranscriBITE est organisé selon une séparation claire des responsabilités entre les deux membres de l'équipe.

Cette organisation permet de travailler en parallèle tout en conservant une architecture cohérente grâce à des points d'intégration définis.

## Membre 1 — Développement Backend, Architecture et Interface

Le membre 1 est responsable des éléments suivants :

### Backend

* Gestion des fichiers importés.
* Validation des fichiers (extension, type MIME, taille).
* Génération des identifiants uniques des fichiers.
* Organisation du stockage.
* Détection du type de média.
* Analyse de la qualité audio.
* Gestion de l'extraction audio avec FFmpeg.
* Développement du module Process responsable de l'orchestration du pipeline.
* Gestion du suivi de progression.
* Préparation du téléchargement des résultats.
* Vérification de l'état du système (Health Check).

### Frontend

* Mise en place de l'architecture React.
* Développement de l'interface utilisateur.
* Gestion de l'import des fichiers.
* Sélection de la langue.
* Affichage des informations du fichier.
* Affichage de la progression du traitement.
* Affichage des résultats de transcription et du résumé.
* Gestion des actions de téléchargement.

## Membre 2 — Services d'intelligence artificielle

Le membre 2 est responsable des composants liés à l'intelligence artificielle :

* Intégration de Faster-Whisper.
* Gestion du moteur de transcription.
* Traitement et formatage des résultats de transcription.
* Intégration d'Ollama.
* Génération automatique des résumés.
* Optimisation des modèles IA selon les contraintes matérielles.

## Points d'intégration

Les deux parties communiquent à travers des interfaces clairement définies.

Le module Process agit comme orchestrateur principal et utilise les services développés par chaque membre.

Les points d'intégration principaux sont :

* Passage du fichier audio extrait vers le service de transcription.
* Récupération du résultat de transcription.
* Envoi de la transcription vers le service de résumé.
* Retour des résultats vers le Frontend.

Cette séparation permet un développement parallèle tout en maintenant une architecture modulaire et évolutive.



## 9. Choix d'architecture

Les choix d'architecture de TranscriBITE ont été réalisés afin de respecter les contraintes du projet tout en garantissant une solution évolutive, maintenable et adaptée aux ressources disponibles.

### Architecture modulaire

L'application adopte une architecture modulaire afin de séparer les responsabilités de chaque composant.

Cette organisation permet :

* de faciliter la maintenance du code.
* de limiter les dépendances entre modules.
* de simplifier les tests.
* de permettre l'évolution indépendante des fonctionnalités.

### Séparation Frontend / Backend

Le choix d'une séparation entre React et FastAPI permet de découpler l'interface utilisateur de la logique métier.

Cette approche facilite :

* le développement parallèle entre les membres.
* les évolutions futures de l'interface.
* la réutilisation des API.

### FastAPI

FastAPI a été choisi pour le développement Backend grâce à :

* sa rapidité d'exécution.
* sa compatibilité avec Python.
* sa simplicité de création d'API REST.
* sa validation automatique des données avec Pydantic.
* sa documentation automatique des endpoints.

### React

React a été choisi pour le développement Frontend grâce à son approche basée sur les composants.

Cette approche permet :

* la création d'une interface réutilisable.
* une meilleure organisation du code.
* une gestion claire des différents éléments de l'interface.

### Traitement local Offline

Une contrainte importante du projet est l'absence de dépendance aux services Cloud.

L'application réalise donc les traitements localement afin de :

* protéger les données utilisateur.
* fonctionner sans connexion Internet.
* garantir l'indépendance vis-à-vis des services externes.

### FFmpeg

FFmpeg est utilisé pour gérer les fichiers multimédias.

Il permet notamment :

* l'extraction audio depuis les vidéos.
* la conversion des formats nécessaires.
* la préparation des fichiers avant transcription.

### Faster-Whisper

Faster-Whisper est utilisé comme moteur de transcription locale.

Ce choix permet :

* une transcription sans service externe.
* une compatibilité avec une exécution CPU.
* une intégration directe dans l'environnement Python.

### Ollama

Ollama est prévu pour la génération locale de résumés.

Son intégration permet d'ajouter une fonctionnalité d'intelligence artificielle supplémentaire tout en conservant l'approche Offline.

### Gestion des états avec des Enums

Les états du pipeline sont centralisés grâce à des Enums dédiés :

* `PipelineStep` pour représenter les étapes du traitement.
* `StepStatus` pour représenter l'état d'une étape.
* `PIPELINE_ORDER` pour garantir l'ordre d'exécution.

Cette approche évite l'utilisation de chaînes de caractères dispersées dans le code et améliore la cohérence entre les différents modules.



## 10. Évolutions futures

L'architecture actuelle de TranscriBITE a été conçue afin de permettre l'ajout de nouvelles fonctionnalités sans modification majeure de la structure existante.

Les évolutions possibles sont les suivantes :

### Optimisation des performances

Une amélioration future pourra concerner l'optimisation du temps de traitement, notamment pour les fichiers volumineux.

Cela pourra inclure :

* l'amélioration de la gestion mémoire.
* l'optimisation du traitement parallèle.
* l'amélioration de la gestion du cache.

### Support GPU

L'application fonctionne actuellement dans un environnement CPU afin de respecter les contraintes matérielles du projet.

Une évolution possible serait l'ajout d'un support GPU afin d'accélérer les traitements de transcription.

### Support de nouveaux formats

L'architecture permet l'ajout progressif de nouveaux formats audio et vidéo grâce à la séparation du module de gestion des fichiers et du pipeline de traitement.

### Amélioration des modèles IA

Les services de transcription et de résumé étant séparés du reste de l'application, il sera possible de remplacer ou améliorer les modèles IA utilisés sans modifier l'ensemble du système.

### Nouveaux formats d'export

L'application pourra évoluer vers de nouveaux formats de téléchargement comme :

* PDF.
* formats structurés supplémentaires.
* exports personnalisés.

### Amélioration du suivi en temps réel

Le système de progression pourra être amélioré avec une communication temps réel basée sur :

* WebSockets.
* Server-Sent Events (SSE).

### Renforcement de la sécurité

Des améliorations futures pourront concerner :

* la gestion des permissions.
* la validation renforcée des fichiers.
* la protection des ressources système.

Grâce à son architecture modulaire, TranscriBITE pourra intégrer ces évolutions progressivement tout en conservant une structure claire et maintenable.



# Gestion du pipeline et des états

Le traitement des fichiers est organisé sous forme d'un pipeline composé de plusieurs étapes.

Les étapes et leurs états sont centralisés dans le dossier :

backend/app/enums/

avec :

- pipeline_step.py
- step_status.py
- pipeline_order.py

Cette organisation permet :

- une meilleure lisibilité du traitement
- un suivi précis de chaque étape
- une intégration future avec le module Progress

---

## Mise à jour — Jour 5

Le backend possède désormais un module dédié à l'importation et à la validation des fichiers.

Modules ajoutés :

- upload.py
- file_service.py
- upload_schema.py

Le routeur Upload communique avec FileService afin de gérer l'importation, la validation et la sauvegarde des fichiers.

---

## Mise à jour — Jour 6

Le backend possède désormais un module dédié à l'orchestration du pipeline de traitement.

Modules ajoutés :

- process.py
- process_service.py
- process_schema.py

Le ProcessService coordonne les différents services Backend afin d'exécuter le pipeline de traitement.

---

## Mise à jour — Jour 7

Le backend possède désormais un module dédié au suivi de progression.

Modules ajoutés :

- progress.py
- progress_service.py
- processing_state.py

Le ProcessService communique avec ProgressService afin de maintenir l'état d'avancement du pipeline.

---

## Mise à jour — Jour 8

Le backend possède désormais un module dédié à la préparation des téléchargements.

Modules ajoutés :

- download.py
- download_service.py
- download_schema.py

Le ProcessService communique avec DownloadService afin de préparer les fichiers de sortie du pipeline.

---

## Mise à jour — Jour 9

Le backend possède désormais un module dédié à la vérification de l'état du système.

Modules ajoutés :

- health.py
- health_service.py
- health_schema.py

Le routeur Health communique avec HealthService afin de vérifier que l'environnement d'exécution est prêt avant le lancement d'un traitement.


# Environnement d'exécution — Mise à jour Jour 10

## Python

Le Backend TranscriBITE utilise Python 3.12.10 dans un environnement virtuel :

```text
backend/.venv
```

Le Python système peut rester sur une autre version sans modifier l'environnement du projet.

## Dépendances

Les dépendances validées sont conservées dans :

```text
backend/requirements.txt
```

## Outils externes

FFmpeg est installé localement et accessible par le PATH.

Ollama est installé localement et accessible par le PATH. Il fournit le service local de génération de résumé.

Le Health Check vérifie également la présence de Torch et Faster-Whisper ainsi
que la disponibilité du serveur Ollama.

## Intégration IA

Le Jour 10 valide l'environnement nécessaire à l'IA. Les services du Membre 2 sont maintenant connectés au pipeline du Membre 1 et validés par les tests et le smoke test réel.
