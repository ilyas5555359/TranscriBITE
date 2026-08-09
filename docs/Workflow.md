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

```text id="g7x0f1"
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

```text id="4yq6fw"
frontend/src/

components/

pages/

services/
```

---

# 4. Communication Frontend Backend

La communication entre React et FastAPI se fait via des API.

Flux :

```text id="7pr6pz"
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

```text id="v2m8z4"
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

```text id="8zqk91"
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

```text id="3q5p0d"
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

```text id="c3g1f9"
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

```text id="5h6n9a"
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

```text id="0j2x7k"
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

```text id="r4w6ks"
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

```text id="x8kq2m"
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

```
```
