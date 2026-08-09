# Technical Decisions — TranscriBITE

## Présentation

Ce document regroupe les décisions techniques prises pendant la conception et le développement du projet TranscriBITE.

Chaque décision est accompagnée de sa justification afin de garder une trace claire des choix effectués.

---

# 1. Architecture générale de l'application

## Décision

Adoption d'une architecture séparée en trois grandes parties :

```text
Frontend

↓

Backend API

↓

Services de traitement
```

## Justification

Cette architecture permet :

* séparation claire des responsabilités
* maintenance plus facile
* développement parallèle entre les membres
* évolution future de l'application

---

# 2. Séparation Frontend et Backend

## Décision

Utilisation d'un frontend indépendant basé sur React et d'un backend basé sur FastAPI.

## Justification

Le découpage permet :

* une meilleure organisation du code
* une communication via API
* une évolution indépendante des deux parties

---

# 3. Choix de FastAPI pour le Backend

## Décision

Utilisation de FastAPI comme framework Backend.

## Justification

FastAPI a été choisi pour :

* création rapide d'API REST
* performances élevées
* support des opérations asynchrones
* validation automatique avec Pydantic
* bonne intégration avec Python

---

# 4. Choix de React pour le Frontend

## Décision

Utilisation de React pour développer l'interface utilisateur.

## Justification

React permet :

* création de composants réutilisables
* gestion dynamique des états
* organisation claire de l'interface
* communication simple avec les API Backend

---

# 5. Fonctionnement local Offline

## Décision

L'application doit fonctionner localement sans dépendance cloud.

## Justification

Cette décision répond aux contraintes du projet :

* protection des fichiers utilisateurs
* confidentialité des données
* fonctionnement sans connexion Internet
* contrôle complet du traitement

---

# 6. Choix de Faster-Whisper pour la transcription

## Décision

Utilisation de Faster-Whisper pour la conversion audio vers texte.

## Justification

Faster-Whisper a été choisi pour :

* fonctionnement local
* bonne précision
* optimisation des performances
* compatibilité CPU

---

# 7. Choix de FFmpeg pour le traitement multimédia

## Décision

Utilisation de FFmpeg pour l'extraction audio depuis les fichiers vidéo.

## Justification

FFmpeg permet :

* support de nombreux formats audio et vidéo
* extraction fiable du son
* conversion des fichiers avant transcription

Pipeline :

```text
Vidéo

↓

FFmpeg

↓

Audio

↓

Faster-Whisper
```

---

# 8. Choix d'Ollama pour la génération de résumé

## Décision

Utilisation d'Ollama pour la génération locale des résumés.

## Justification

Ollama permet :

* utilisation de modèles IA locaux
* absence d'API externe
* respect de la contrainte Offline

Cette fonctionnalité reste optionnelle selon les performances disponibles.

---

# 9. Organisation modulaire du Backend

## Décision

Organisation du Backend selon une architecture modulaire :

```text
routers

services

schemas

models

utils
```

## Justification

Cette organisation permet :

* séparation des responsabilités
* code plus maintenable
* tests plus faciles
* évolution simplifiée

---

# 10. Séparation des responsabilités entre les membres

## Décision

Définition claire des modules attribués à chaque membre.

## Membre 1

Responsable de :

* gestion fichiers
* upload
* validation
* qualité audio
* FFmpeg
* progression
* téléchargement
* frontend

## Membre 2

Responsable de :

* transcription Faster-Whisper
* résumé Ollama
* traitement IA
* résultats

## Justification

Cette séparation réduit les conflits de développement et facilite l'intégration.

---

# 11. Gestion du pipeline avec des Enum

## Décision

Utilisation d'Enum pour représenter les étapes et états du traitement.

Fichiers créés :

```text
backend/app/enums/

pipeline_step.py

step_status.py

pipeline_order.py
```

## Justification

Les Enum permettent :

* éviter les erreurs de chaînes de caractères
* standardiser les valeurs
* faciliter la maintenance
* préparer le suivi de progression

---

# 12. Pipeline officiel de traitement

## Décision

Le traitement suit un pipeline composé des étapes suivantes :

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

## Justification

Cette organisation permet :

* suivi précis du traitement
* gestion des erreurs
* communication avec le frontend
* intégration progressive des modules

---

# 13. Documentation continue

## Décision

La documentation sera mise à jour pendant le développement.

## Règle appliquée

Après chaque grande étape :

* mise à jour architecture
* mise à jour workflow
* mise à jour décisions techniques
* mise à jour notes quotidiennes
* ajout des problèmes rencontrés

## Justification

Cela garantit une documentation toujours synchronisée avec le projet.

---

# Décision : Architecture modulaire Backend

## Décision

Séparer le Backend selon les responsabilités :

* routers pour les API
* services pour la logique métier
* schemas pour les échanges API
* models pour les structures internes
* utils pour les fonctions communes

## Justification

Cette organisation facilite :

* le développement parallèle
* les tests
* la maintenance
* l'intégration avec le membre 2

---

# Décision : Utilisation des Enums pour le pipeline

## Contexte

Plusieurs modules doivent communiquer autour de l'état du traitement.

L'utilisation de simples chaînes de caractères pourrait provoquer des incohérences.

## Décision

Créer un système centralisé basé sur des enums :

```text
backend/app/enums/

pipeline_step.py
step_status.py
pipeline_order.py
```

---

# Décision : Centralisation de l'état du traitement

## Contexte

Plusieurs modules doivent connaître l'état d'avancement d'un fichier pendant son traitement.

## Décision

Créer un modèle centralisé `ProcessingStatus` utilisant les enums :

* PipelineStep
* StepStatus

## Informations conservées

Le modèle contient :

* étape actuelle
* statut
* progression
* historique des étapes
* dates de traitement

## Justification

Cette approche permet :

* un suivi précis du pipeline
* une communication claire avec le Frontend
* une future intégration SSE/WebSocket
* une meilleure gestion des erreurs

---

# Décisions futures à ajouter

Les prochaines décisions seront ajoutées concernant :

* communication temps réel SSE ou WebSocket
* choix du modèle Faster-Whisper
* optimisation CPU
* gestion des gros fichiers
* stratégie de tests
* déploiement final

---

### 14. Architecture du module Process

Le module Process est conçu comme l'orchestrateur principal du backend.

Le routeur `process.py` contient uniquement les endpoints HTTP.

Toute la logique métier est déléguée à `ProcessService`.

Le pipeline est construit selon une architecture modulaire où chaque responsabilité est confiée à un service spécialisé :

- FileService
- AudioService
- QualityService
- TranscriptionService
- SummaryService
- DownloadService
- ProgressService

Le ProcessService ne réalise aucun traitement métier directement, il orchestre uniquement les différents services.

Chaque traitement est délégué à un service spécialisé afin de garantir une séparation stricte des responsabilités.

Toutes les méthodes du pipeline sont déclarées dès cette phase afin de garantir une architecture stable avant l'implémentation complète.

Les méthodes asynchrones (`async`) sont utilisées dans ProcessService afin d'assurer une cohérence avec FastAPI et de faciliter l'intégration future des traitements I/O.

---

## Uniformisation de l'architecture Backend

Décision :

Créer un `HealthService`.

Motivation :

Tous les modules Backend utilisent désormais exactement la même architecture.

Router

↓

Service

↓

Schema

Cette homogénéité facilite la maintenance, les tests et les futures évolutions.

---

## Ajout du HealthService

### Décision

Créer un service dédié aux vérifications de l'environnement.

### Justification

Séparer les contrôles système du routeur améliore la maintenabilité et respecte l'architecture en couches du projet.

---

## Analyse audio basée sur le chemin du fichier

### Décision

Le QualityService reçoit directement un objet `Path` plutôt qu'un identifiant UUID.

### Justification

Le service travaille sur un fichier physique. La conversion éventuelle UUID → Path sera réalisée par le ProcessService, ce qui permet au QualityService de rester spécialisé dans l'analyse audio.

---

## Centralisation de la vérification des fichiers

### Décision

La méthode `check_file_exists()` est centralisée dans FileService.

### Justification

Toutes les vérifications liées aux fichiers sont regroupées dans un seul service afin d'éviter la duplication de code et de conserver une responsabilité unique.


# 14. Environnement Python 3.12 dédié au projet

## Décision

TranscriBITE utilise Python 3.12 dans un environnement virtuel situé dans `backend/.venv`.

## Justification

Le projet nécessite un environnement stable et isolé pour ses dépendances Backend et IA. Le Python système peut conserver une autre version sans affecter TranscriBITE.

# 15. Dépendances verrouillées dans requirements.txt

## Décision

Le fichier `backend/requirements.txt` est généré à partir de l'environnement virtuel validé.

## Justification

Le fichier constitue une référence commune pour reproduire l'environnement du projet et préparer l'intégration entre les deux membres.

# 16. FFmpeg accessible par le PATH

## Décision

Le Backend utilise `FFMPEG_PATH=ffmpeg` et s'appuie sur le PATH pour localiser FFmpeg.

## Justification

Cette configuration évite de dépendre d'un chemin absolu propre à une seule machine.

# 17. Ollama comme service local

## Décision

Ollama est utilisé comme composant local destiné à la future génération de résumé.

## Justification

Cette décision respecte la contrainte offline du projet. Le serveur local et la commande CLI ont été vérifiés pendant le Jour 10.

# 18. Préparation de l'intégration IA

## Décision

Le Jour 10 prépare l'environnement nécessaire, mais l'intégration réelle des services IA avec le pipeline du Membre 1 reste planifiée pour la phase d'intégration du Jour 14.

## Justification

Cette séparation permet de valider d'abord l'environnement puis de connecter les services du Membre 2 dans une phase dédiée.

---

# 19. Stratégie de gestion des versions

### Objectif

TranscriBITE utilise Git et GitHub afin d'assurer le suivi des modifications, la collaboration entre les deux membres et la conservation d'une version stable du projet.

Le projet étant développé par deux membres avec des responsabilités distinctes, une organisation simple basée sur une branche principale et une branche de développement par membre a été retenue.

### Organisation des branches

La structure retenue est la suivante :

```text
main
│
├── member1
│
└── member2
```

#### Branche `main`

La branche `main` représente la version stable et validée du projet.

Les développements ne sont pas réalisés directement sur cette branche.

Les modifications y sont intégrées après validation du travail effectué sur les branches des membres.

#### Branche `member1`

La branche `member1` est la branche principale de développement du Membre 1.

Elle contient notamment les travaux liés à :

* Backend fichiers
* Upload
* Validation
* Process
* Progress
* Download
* Health
* Quality Check
* Frontend
* Documentation

#### Branche `member2`

La branche `member2` est la branche principale de développement du Membre 2.

Elle contient notamment les travaux liés à :

* Faster-Whisper
* Transcription
* Ollama
* Résumé
* Fonctionnalités IA

### Règle de développement

Chaque membre développe principalement sur sa propre branche.

Le développement direct sur `main` est évité afin de conserver une version stable du projet.

Le cycle de travail est :

```text
Développement
↓
Test local
↓
Vérification des modifications
↓
Commit
↓
Push vers la branche du membre
↓
Pull Request
↓
Validation
↓
Merge vers main
```

### Convention des commits

Chaque commit doit représenter une étape logique et identifiable du développement.

Exemples :

```text
Initialize TranscriBITE project

Fix documentation directory structure

Implement QualityService file validation

Update technical documentation

Prepare UML diagrams

Integrate frontend upload module
```

Les messages vagues tels que `Update`, `Fix`, `Changes` ou `Final` sont évités.

### Synchronisation avec `main`

Lorsqu'une mise à jour de `main` doit être récupérée, le membre peut utiliser :

```bash
git fetch origin
git merge origin/main
```

Cette méthode permet de récupérer les dernières modifications du dépôt distant puis de les intégrer explicitement dans la branche de travail.

### Pull Requests

Une Pull Request est utilisée lorsqu'une branche contient un ensemble de modifications terminé, testé et prêt à être intégré.

Le processus recommandé est :

```text
member1 / member2
↓
Travail terminé
↓
Tests
↓
Push
↓
Pull Request
↓
Vérification
↓
Merge vers main
```

### Gestion des conflits

En cas de conflit entre deux branches, le conflit doit être analysé et résolu avant la fusion.

La procédure générale est :

```text
Détection du conflit
↓
Identification des fichiers concernés
↓
Analyse des modifications
↓
Résolution du conflit
↓
Tests
↓
Commit
↓
Fusion
```

L'utilisation de `git push --force` n'est pas utilisée comme méthode de résolution normale des conflits.

### Initialisation du dépôt

Le dépôt Git local de TranscriBITE a été initialisé après la préparation de l'environnement Python 3.12 du Jour 10.

Cette décision permet de commencer le suivi Git avec un environnement de développement cohérent et validé.

Le dépôt GitHub est utilisé comme dépôt distant officiel du projet.

### État actuel

Le dépôt contient actuellement les branches principales suivantes :

main
member1

La branche `main` est synchronisée avec le dépôt GitHub et la branche `member1` est également publiée sur le dépôt distant.

Le Membre 1 poursuit son développement sur `member1`.
