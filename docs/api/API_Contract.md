# API Contract — TranscriBITE

## Présentation

Ce document décrit les différents endpoints REST exposés par le backend de TranscriBITE.

Chaque endpoint précise :

- sa responsabilité
- la méthode HTTP utilisée
- les paramètres attendus
- les modèles de données utilisés
- les réponses retournées
- son état d'avancement pendant le développement

Ce document est mis à jour progressivement au fur et à mesure du développement des différents modules du projet.

---

# Upload API

## POST /upload

Responsabilité :

Recevoir un fichier audio ou vidéo envoyé par l'utilisateur, effectuer les différentes validations puis enregistrer le fichier dans le stockage temporaire.

Entrée :

- Fichier (multipart/form-data)

Vérifications effectuées :

- extension autorisée
- type MIME
- taille maximale
- nom du fichier
- génération d'un identifiant UUID

Réponse :

UploadResponse

Informations retournées :

- success
- message
- file_id
- original_filename
- stored_filename
- file_size
- media_type
- upload_date

Etat :

Développé - Jour 5

---

# Process API

## POST /process

Responsabilité :

Lancer le traitement complet d'un fichier après validation.

Entrée :

Informations du fichier déjà uploadé.

Sortie :

Informations du lancement du pipeline.

Etat :

Prévu - développement Jour 6



### POST /process/start

Description :

Initialise le pipeline principal.

Paramètre :

- file_id : UUID

Réponse :

ProcessResponse

---

# Progress API

## GET /progress/{file_id}

Responsabilité :

Retourner l'état actuel du traitement.

Paramètre :

- file_id : UUID

Réponse :

ProgressResponse

Informations retournées :

- file_id
- current_step
- current_status
- progress_percentage
- message
- started_at
- finished_at

Etat :

Développé - Jour 7

---

# Download API

## GET /download/{file_id}/{download_format}

Responsabilité :

Préparer le téléchargement des résultats générés par le pipeline.

Paramètres :

- file_id : UUID
- download_format : txt | json

Réponse :

DownloadResponse

Informations retournées :

- success
- message
- file_id
- filename
- download_format

Etat :

Développé - Jour 8

---

# Health API

## GET /health

Responsabilité :

Vérifier que l'environnement du backend est prêt à exécuter un traitement.

Réponse :

HealthResponse

Informations retournées :

- success
- message
- checks

Chaque élément de `checks` contient :

- component
- status
- message

Etat :

Développé — Jour 9

---

# Quality API

Aucune route dédiée n'est prévue.

Le QualityService est utilisé uniquement par le ProcessService durant le pipeline principal.

Etat :

Développement Jour 9
