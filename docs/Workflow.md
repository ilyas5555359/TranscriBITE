# Workflow Global — TranscriBITE

## Présentation

Ce document décrit le fonctionnement global de l'application TranscriBITE.

Il présente le parcours complet d'un fichier depuis son import par l'utilisateur jusqu'à l'obtention des résultats de transcription et de résumé.

Le workflow respecte l'architecture définie :

* Frontend React
* Backend FastAPI
* Services spécialisés
* Traitement local Offline

---

# 1. Vue générale du fonctionnement

Le fonctionnement global de TranscriBITE suit le flux suivant :

```text
Utilisateur

↓

Interface React

↓

API FastAPI

↓

Gestion du fichier

↓

Pipeline de traitement

↓

Services spécialisés

↓

Résultats

↓

Interface utilisateur
```

---

# 2. Interaction utilisateur

L'utilisateur commence par :

* ouvrir l'application
* sélectionner un fichier audio ou vidéo
* choisir la langue ou activer la détection automatique
* lancer le traitement

L'interface React transmet ensuite les informations au Backend.

---

# 3. Partie Frontend

Le Frontend React est responsable de :

* affichage de l'interface
* import des fichiers
* affichage des informations du fichier
* sélection de la langue
* lancement du traitement
* affichage de la progression
* affichage des résultats
* téléchargement des fichiers générés

Structure principale :

```text
frontend/src/

components/

pages/

services/
```

---

# 4. Communication Frontend Backend

La communication entre React et FastAPI se fait via des API.

Flux :

```text
React

↓

HTTP Request

↓

FastAPI

↓

Traitement

↓

HTTP Response

↓

React
```

Les API permettent :

* upload des fichiers
* lancement du traitement
* récupération de la progression
* récupération des résultats
* téléchargement

---

# 5. Partie Backend

Le Backend FastAPI représente le centre de contrôle de l'application.

Il contient :

```text
routers

services

schemas

models

utils
```

---

## 5.1 Routers

Les routers exposent les fonctionnalités de l'application.

Exemples :

```text
upload.py

process.py

progress.py

download.py

health.py
```

Responsabilités :

* recevoir les requêtes
* valider les données
* appeler les services correspondants

---

## 5.2 Services

Les services contiennent la logique métier.

Exemples :

```text
file_service.py

audio_service.py

quality_service.py

progress_service.py

download_service.py
```

Ils réalisent notamment :

* gestion des fichiers
* orchestration du pipeline principal
* traitement audio
* analyse qualité
* transcription
* génération du résumé
* suivi de la progression
* préparation des fichiers de téléchargement
* vérification de l'environnement

---

# 6. Pipeline de traitement

Après l'upload, le fichier entre dans le pipeline principal.

Le pipeline complet est :

```text
Upload

↓

Validation

↓

Initialisation du pipeline

↓

Détection du média

↓

Analyse qualité

↓

Extraction audio (si nécessaire)

↓

Transcription

↓

Génération du résumé (optionnelle)

↓

Préparation des fichiers

↓

Téléchargement

↓

Nettoyage

↓

Terminé

ou

Échoué
```

Chaque étape possède un état :

```text
En attente

En cours

Terminée

Échec
```

---

# 6.1 Orchestration du pipeline

Le ProcessService constitue le cœur du Backend.

Il coordonne l'ensemble des services spécialisés afin d'exécuter le pipeline de traitement.

L'ordre d'exécution est le suivant :

ProcessService

↓

FileService

↓

QualityService

↓

AudioService

↓

TranscriptionService

↓

SummaryService

↓

DownloadService

Le ProcessService est également responsable de :

* l'initialisation du traitement
* la sélection automatique du pipeline Audio/Vidéo
* la gestion centralisée des erreurs
* la mise à jour de la progression

---

# 7. Traitement audio et vidéo

Selon le type du fichier :

## Fichier audio

Flux :

```text
Audio

↓

Analyse qualité

↓

Faster-Whisper

↓

Transcription

↓

Résumé optionnel

↓

Résultat
```

---

## Fichier vidéo

Flux :

```text
Vidéo

↓

Analyse qualité

↓

FFmpeg

↓

Extraction audio

↓

Faster-Whisper

↓

Transcription

↓

Résumé optionnel

↓

Résultat
```

---

# 8. Services Intelligence Artificielle

## Faster-Whisper

Responsabilité :

* conversion audio en texte
* génération de transcription

Responsable :

Membre 2

---

## Ollama

Responsabilité :

* génération de résumé local
* traitement du texte obtenu

Responsable :

Membre 2

---

# 9. Gestion des résultats

Après le traitement :

Les résultats sont préparés pour l'utilisateur.

Formats prévus :

* TXT
* JSON
* PDF futur

Le module Download permet :

* génération des fichiers
* récupération
* téléchargement

---

# 9.1 Vérification de l'environnement

Avant ou pendant le traitement, le module Health permet de vérifier :

* le fonctionnement du Backend
* la configuration
* les dossiers de stockage
* la disponibilité de FFmpeg

Ces vérifications facilitent le diagnostic des problèmes avant le lancement du pipeline.

---

Toutes les erreurs importantes sont enregistrées par le Logger.

Le ProcessService centralise les erreurs remontées par les différents services afin de garantir un comportement cohérent du pipeline.

---

# 10. Gestion des erreurs

Chaque étape peut produire une erreur.

Exemples :

* fichier non supporté
* problème FFmpeg
* erreur transcription
* manque d'espace stockage

En cas d'erreur :

```text
Étape en cours

↓

Erreur détectée

↓

Etat Échec

↓

Message utilisateur
```

---

# 11. Organisation entre les membres

## Membre 1

Responsable :

* Backend fichiers
* Upload
* Validation
* FFmpeg
* Qualité
* Progression
* Download
* Frontend

## Membre 2

Responsable :

* Faster-Whisper
* Transcription
* Ollama
* Résumé
* Résultats IA

L'intégration sera réalisée pendant la phase dédiée.

---

# 12. Évolution future du workflow

Le workflow sera complété avec :

* communication temps réel SSE/WebSocket
* intégration complète de Faster-Whisper
* intégration complète d'Ollama
* optimisation des performances
* tests complets
* génération PDF
* déploiement final

---

# 13. Workflow Git et collaboration

Le développement de TranscriBITE est organisé avec Git et GitHub afin de permettre aux deux membres de travailler indépendamment tout en conservant une version stable du projet.

## 13.1 Organisation

```text
main
│
├── member1
│
└── member2
```

La branche `main` représente la version stable du projet.

Chaque membre développe sur sa propre branche.

## 13.2 Workflow du Membre 1

Le Membre 1 travaille sur :

```text
member1
```

Son cycle de travail est :

```text
Développement
↓
Tests locaux
↓
git status
↓
git diff
↓
git add
↓
git commit
↓
git push
```

## 13.3 Workflow du Membre 2

Le Membre 2 travaille sur :

```text
member2
```

Il suit le même principe de développement, de test, de commit et de push.

## 13.4 Intégration

Lorsque le travail d'un membre est terminé et validé, il peut être proposé pour intégration dans `main` à travers une Pull Request.

```text
member1
   ↓
Pull Request
   ↓
main
```

ou :

```text
member2
   ↓
Pull Request
   ↓
main
```

## 13.5 Synchronisation

Lorsqu'une mise à jour de `main` doit être intégrée dans une branche de développement :

```bash
git fetch origin
git merge origin/main
```

Cette opération permet de maintenir les branches de développement synchronisées avec la version stable.

## 13.6 Gestion des conflits

En cas de modifications incompatibles entre les branches, les conflits sont résolus avant l'intégration.

Le processus est :

```text
Conflit
↓
Analyse
↓
Résolution
↓
Tests
↓
Commit
↓
Merge
```

## 13.7 Principe général

La règle principale est :

> Le développement se fait sur les branches des membres et l'intégration stable se fait dans `main`.

Cette organisation permet de limiter les conflits et de conserver une version stable du projet pendant le développement.
