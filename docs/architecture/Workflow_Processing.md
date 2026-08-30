# Workflow Processing : TranscriBITE

## Présentation

Ce document décrit le fonctionnement interne du pipeline de traitement de TranscriBITE.

Il détaille les différentes étapes exécutées après l'import d'un fichier ainsi que les états associés à chaque étape.

Le pipeline est conçu pour être modulaire afin de permettre l'intégration progressive des différents services.

---

# 1. Vue générale du pipeline

Le traitement complet suit l'ordre suivant :

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
```

En cas d'erreur :

```text
Une étape échoue

↓

Etat Échec

↓

Arrêt ou gestion contrôlée du pipeline
```

## Vérification préalable du système

Avant le démarrage du pipeline principal, le backend peut exécuter une vérification générale de son environnement.

Cette vérification contrôle :

1. le Backend
2. la configuration
3. le stockage
4. FFmpeg

Ces contrôles sont réalisés par le module Health afin de s'assurer que le système est prêt à lancer un traitement.

---

# 2. Gestion des étapes du pipeline

Les étapes sont définies dans :

```text
backend/app/enums/pipeline_step.py
```

Elles représentent les différentes phases du traitement.

Les valeurs officielles sont :

```text
UPLOAD

VALIDATION

MEDIA_DETECTION

QUALITY_ANALYSIS

AUDIO_EXTRACTION

TRANSCRIPTION

SUMMARY_GENERATION

RESULT_PREPARATION

CLEANUP

COMPLETED

FAILED
```

## 2.1 Source unique des états du pipeline

Les différents modules utilisent les mêmes valeurs définies dans les enums Backend.

Les références officielles sont :

```text
backend/app/enums/

├── pipeline_step.py
├── step_status.py
└── pipeline_order.py
```

---

# 3. Gestion des états

Les états d'exécution sont définis dans :

```text
backend/app/enums/step_status.py
```

Valeurs utilisées :

```text
PENDING

RUNNING

COMPLETED

FAILED
```

Signification :

## En attente

L'étape n'a pas encore commencé.

---

## En cours

Le traitement est actuellement exécuté.

---

## Terminée

L'étape a été exécutée avec succès.

---

## Échec

Une erreur est survenue pendant le traitement.

---

Le suivi d'un traitement est représenté par le modèle `ProcessingStatus`.

Ce modèle conserve :

* l'identifiant du fichier
* l'étape actuelle
* le statut actuel
* le pourcentage d'avancement
* la liste des étapes exécutées
* les dates de début et de fin du traitement

Chaque étape individuelle est représentée par `ProcessingStep`.

---

# 4. Ordre d'exécution

L'ordre officiel est défini dans :

```text
backend/app/enums/pipeline_order.py
```

Il garantit que les étapes sont exécutées dans le bon ordre.

L'ordre du pipeline sera utilisé par :

* Process Service pour l'orchestration
* Progress Service pour calculer l'avancement
* Processing State pour représenter l'état courant
* Frontend Progress Tracker pour l'affichage utilisateur

---

# 5. Description des étapes

## 5.1 Upload

La première étape consiste à recevoir le fichier envoyé par l'utilisateur. L'application vérifie la présence du média, son nom, sa taille et son type. Une fois validé, le fichier est enregistré dans le dossier de stockage correspondant.

## 5.2 Validation

Cette étape sécurise le backend en vérifiant les types acceptés, la taille, les paramètres de configuration et l'intégrité du fichier téléchargé. Elle permet de ne pas lancer de traitement inutile sur un fichier invalide.

## 5.3 Détection du type de média

Le système détermine si le fichier est audio, vidéo ou incompatible. Cette étape conditionne le comportement du pipeline, notamment l'extraction d'audio pour les fichiers vidéo.

## 5.4 Analyse de qualité audio

L'analyse de qualité permet de mesurer les caractéristiques du média avant transcription. Elle aide à détecter d'éventuels soucis de qualité, de format ou de compatibilité avec les moteurs de traitement.

## 5.5 Extraction audio

Pour les vidéos, FFmpeg est utilisé pour produire une piste audio exploitable par le moteur de transcription. Cette étape est automatique et centralisée.

## 5.6 Transcription

La transcription convertit le signal audio en texte brut. Le moteur peut être configuré selon la langue, le modèle et le mode de calcul. Cette étape représente le cœur fonctionnel de l'application.

## 5.7 Génération du résumé

Selon l'état du projet et la configuration, la transcription peut être utilisée pour générer un résumé. Cela peut être réalisé avec un modèle local et permet de produire un format plus synthétique et plus exploitable.

## 5.8 Préparation des résultats

Le système regroupe les éléments obtenus, met en forme les résultats, et prépare les fichiers utilisables par le Frontend. Cette étape peut générer plusieurs sorties (TXT, JSON, PDF, etc.).

## 5.9 Nettoyage

La phase de nettoyage supprime les fichiers temporaires et les artefacts inutiles. Cela évite le remplissage du stockage et aide à maintenir la propreté du système.

## 5.10 Terminé

Quand toutes les étapes sont validées, l'état passe en `COMPLETED` afin que l'utilisateur puisse accéder à ses résultats. À ce stade, le traitement est terminé et les fichiers sont prêts à être téléchargés.

---

# 6. Intégration avec le Frontend

Le Frontend suit le statut du pipeline en appelant régulièrement les routes de progression. Il affiche :

* le nom du fichier
* l'étape active
* le pourcentage
* le statut global
* éventuellement des messages détaillés

Cette communication garantit une expérience utilisateur cohérente et réactive.

---

# 7. Gestion des erreurs et reprise

En cas d'échec, le pipeline ne doit pas laisser le système dans un état ambigu. L'API renvoie un message explicite et met à jour les états. Cela permet d'indiquer précisément quelle étape a échoué et ce qui doit être réparé.

Les erreurs les plus fréquentes sont :

* fichier absent ou corrompu
* format non supporté
* FFmpeg non disponible
* modèle IA non chargé
* problème de mémoire ou de ressources
* timeout de transcription

---

# 8. Conclusion

Le workflow de traitement de TranscriBITE est basé sur une architecture modulaire, des enums standardisés et un orchestrateur central. Cette structure rend le système lisible, extensible et stable, tout en assurant un suivi détaillé de chaque étape pour le Frontend et les utilisateurs.


## 5.1 Upload

Responsabilité :

Recevoir le fichier envoyé par l'utilisateur.

Actions :

* réception du fichier
* création de l'identifiant unique
* sauvegarde temporaire

Module associé :

```text
routers/upload.py

services/file_service.py
```

---

# 5.2 Validation

Responsabilité :

Vérifier que le fichier respecte les règles du système.

Vérifications :

* extension
* type MIME
* taille maximale
* format supporté

Module associé :

```text
utils/validators.py
```

---

# 5.3 Détection du média

Responsabilité :

Identifier si le fichier est :

* audio
* vidéo

Cette étape permet de choisir automatiquement le pipeline adapté.

---

# 5.4 Analyse qualité audio

Le contrôle qualité est réalisé par `QualityService`.

Avant toute analyse, le QualityService vérifie l'existence du fichier via `FileService.check_file_exists()`. Le fichier est vérifié grâce à la fonction `check_file_exists()` du `FileService`.

Le service récupère ensuite les différentes caractéristiques du média avant de construire un rapport de qualité.

Responsabilité :

Analyser les caractéristiques du média.

Informations possibles :

* durée
* taille
* fréquence
* débit
* nombre de canaux

Module associé :

```text
services/quality_service.py
```

Le service est organisé selon les étapes suivantes :

analyze_audio()

↓

_get_duration()

↓

_get_file_size()

↓

_get_bitrate()

↓

_get_sample_rate()

↓

_get_channels()

↓

_build_quality_report()

↓

_handle_error()


Le ProcessService transmet directement le chemin physique (`Path`) du fichier au QualityService.

Les informations récupérées sont ensuite regroupées dans un rapport qualité utilisé par le pipeline principal.
---

# 5.5 Extraction audio

Responsabilité :

Extraire la piste audio depuis une vidéo.

Technologie utilisée :

```text
FFmpeg
```

Flux :

```text
Vidéo

↓

FFmpeg

↓

Audio
```

Module associé :

```text
services/audio_service.py
```

---

# 5.6 Transcription

Responsabilité :

Transformer l'audio en texte.

Technologie :

```text
Faster-Whisper
```

Responsable :

Membre 2

Module associé :

```text
services/transcription_service.py
```

---

# 5.7 Génération résumé

Responsabilité :

Créer un résumé à partir de la transcription.

Technologie :

```text
Ollama
```

Responsable :

Membre 2

Module associé :

```text
services/summary_service.py
```

---

# 5.8 Préparation résultats

Responsabilité :

Préparer les données finales.

Résultats possibles :

* transcription texte
* résumé
* informations fichier

---

# 5.9 Nettoyage

Responsabilité :

Supprimer les fichiers temporaires.

Exemples :

* fichiers audio intermédiaires
* fichiers temporaires FFmpeg

Objectif :

Optimiser l'utilisation du stockage.

---

# 6. Gestion des erreurs

Chaque étape doit pouvoir signaler une erreur.

Exemples :

## Upload

Erreur :

* fichier absent
* format interdit

## FFmpeg

Erreur :

* extraction impossible

## Transcription

Erreur :

* modèle indisponible
* fichier audio invalide

## Résumé

Erreur :

* modèle Ollama indisponible

En cas d'erreur :

```text
Etape actuelle

↓

Etat FAILED

↓

Enregistrement du log

↓

Retour erreur utilisateur
```

---

# 7. Communication entre les modules

Le Process Service joue le rôle d'orchestrateur.

Flux :

```text
Health Service

↓

Process Service

↓

File Service

↓

Quality Service

↓

Audio Service

↓

Transcription Service

↓

Summary Service

↓

Download Service
```

---

Une fois le pipeline terminé, le Download Service prépare les fichiers exportables.

Le téléchargement suit les étapes suivantes :

1. Validation de la demande
2. Vérification du format demandé
3. Préparation du téléchargement TXT ou JSON
4. Retour des informations de téléchargement

Le pipeline permet également la génération de fichiers PDF.

## 7.1 Workflow interne du ProcessService

Le ProcessService agit comme l'orchestrateur principal du pipeline.

À la réception d'une demande de traitement, il exécute les opérations suivantes dans l'ordre :

1. Création du `ProcessingStatus`
2. Validation du fichier
3. Détection du type de média
4. Sélection automatique du pipeline
5. Exécution des services spécialisés
6. Finalisation du traitement
7. Retour du `ProcessResponse`

Ce fonctionnement garantit une séparation claire entre la logique métier des différents services et l'orchestration générale du pipeline.

---

# 8. Préparation du suivi de progression

Le suivi de progression sera basé sur l'état réel du pipeline.

Chaque étape possède :

* une étape PipelineStep
* un statut StepStatus
* un pourcentage d'avancement
* un message utilisateur
* une date de modification

Le système permettra au Frontend de connaître précisément l'état du traitement.

---

# 9. Evolution future

Ce workflow sera complété avec :

* suivi temps réel via Progress
* événements SSE ou WebSocket
* optimisation performances
* gestion avancée des erreurs
* tests d'intégration

---

# 10. Suivi de progression

Le suivi de progression repose désormais sur un service dédié (`ProgressService`).

Ce service est responsable de :

- la mise à jour de l'étape courante du traitement
- la mise à jour du statut de chaque étape
- le calcul du pourcentage global de progression
- la mise à jour de la date de fin du traitement
- la gestion de l'état final du pipeline

Le modèle `ProcessingState` centralise les informations nécessaires au suivi en temps réel.

Le module Progress constitue la base du futur affichage temps réel dans le Frontend.

---
