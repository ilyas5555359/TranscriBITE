# API Contract — TranscriBITE

## Présentation

Ce document décrit les endpoints REST exposés par le backend de TranscriBITE.

Chaque endpoint précise :

* sa responsabilité
* la méthode HTTP utilisée
* les paramètres attendus
* les modèles de données utilisés
* les réponses retournées
* son état d'avancement

Le contrat est maintenu en fonction de l'implémentation réelle du backend.

---

# 1. Upload API

## POST /upload/

### Responsabilité

Recevoir un fichier audio ou vidéo envoyé par l'utilisateur, effectuer les validations nécessaires puis enregistrer le fichier dans le stockage.

### Entrée

Requête `multipart/form-data`.

Paramètre :

* `file` : fichier audio ou vidéo

### Vérifications

* extension autorisée
* type MIME
* taille maximale
* nom du fichier
* génération d'un identifiant de fichier

### État

**Développé — Jour 5**

---

# 2. Process API

## POST /process/start

### Responsabilité

Initialiser le traitement d'un fichier à travers le pipeline principal.

### Paramètre

* `file_id` : UUID du fichier

### Réponse

`ProcessResponse`

La réponse contient notamment :

* `success`
* `message`
* `processing`
* `file_id`
* `current_step`
* `current_status`
* `progress_percentage`
* `steps`
* `started_at`
* `finished_at`

### Gestion des erreurs

* `404` : fichier introuvable
* `400` : erreur de validation métier
* `500` : erreur interne

### État

**Développé — architecture du ProcessService**

---

# 3. Progress API

## GET /progress/{file_id}

### Responsabilité

Retourner l'état actuel du traitement d'un fichier.

### Paramètre

* `file_id` : UUID

### Réponse

`ProgressResponse`

Informations retournées :

* `success`
* `message`
* `processing`
* `current_step`
* `current_status`
* `progress_percentage`
* `steps`
* `started_at`
* `finished_at`

### Gestion des erreurs

* `404` : traitement ou fichier introuvable
* `500` : erreur interne

### État

**Développé — Jour 7**

---

# 4. Download API

## GET /download/{file_id}/{download_format}

### Responsabilité

Préparer le téléchargement d'un résultat généré par le pipeline.

### Paramètres

* `file_id` : UUID
* `download_format` : format demandé

### Réponse

`DownloadResponse`

Informations retournées :

* `success`
* `message`
* `file_id`
* `filename`
* `download_format`

### État

**Développé — Jour 8**

---

# 5. Health API

## GET /health

### Responsabilité

Vérifier l'état général de l'environnement Backend.

### Réponse

`HealthResponse`

Informations retournées :

* `success`
* `message`
* `checks`

Chaque contrôle contient :

* `component`
* `status`
* `message`

### État

**Développé — Jour 9**

---

# 6. Quality Module

## Route dédiée

Aucune route REST dédiée n'est prévue pour le module Quality.

Le `QualityService` est utilisé par le `ProcessService` pendant le pipeline principal.

### Responsabilité

Analyser les caractéristiques du fichier audio, notamment les informations nécessaires au contrôle de qualité.

### État

**Architecture développée — Jour 9**

---

# 7. Extract API

## POST /extract

### Responsabilité

Extraire la piste audio d'un fichier uploadé et produire un fichier WAV compatible avec Faster-Whisper.

Le fichier produit est :

* mono
* 16 kHz
* PCM 16-bit
* au format WAV

### Entrée

Requête JSON :

```json
{
  "file_id": "identifiant_du_fichier",
  "output_format": "wav"
}
```

### Paramètres

#### file_id

Identifiant du fichier uploadé.

Type :

```text
string
```

#### output_format

Format audio demandé.

Valeur actuellement supportée :

```text
wav
```

### Réponse

`ExtractResponse`

Exemple de structure :

```json
{
  "success": true,
  "message": "Audio extracted successfully",
  "file_id": "test_file",
  "audio_filename": "test_file.wav",
  "audio_path": "chemin/vers/test_file.wav"
}
```

### Erreurs

`404` :

Fichier uploadé introuvable.

`500` :

* FFmpeg indisponible
* échec de l'extraction audio

### État

**Développé — intégration validée avant Transcription**

---

# 8. Transcription API

## POST /transcribe

### Responsabilité

Transcrire un fichier audio déjà préparé à l'aide de Faster-Whisper.

Cette route appartient au module IA du **Membre 2**.

Le fichier audio fourni doit être un fichier audio prêt pour la transcription.

### Entrée

Requête JSON :

```json
{
  "job_id": "test-job-001",
  "audio_path": "chemin/vers/audio.wav",
  "original_filename": "video.mp4",
  "media_type": "audio"
}
```

### Paramètres

#### job_id

Identifiant partagé du traitement.

Type :

```text
string
```

#### audio_path

Chemin vers le fichier audio préparé.

Type :

```text
string
```

#### original_filename

Nom original du fichier envoyé par l'utilisateur.

Type :

```text
string
```

#### media_type

Type de média attendu par l'endpoint.

Valeur actuellement supportée :

```text
audio
```

### Traitement

Le endpoint transmet `audio_path` au `TranscriptionService`.

Le `TranscriptionService` utilise Faster-Whisper avec le modèle configuré dans l'environnement.

Configuration actuelle :

```text
WHISPER_MODEL=base
device=cpu
compute_type=int8
```

### Réponse

`TranscribeResponse`

Structure :

```json
{
  "success": true,
  "message": "Transcription completed successfully",
  "data": {
    "text": "Texte transcrit...",
    "language": "fr",
    "segments": []
  },
  "job_id": "test-job-001"
}
```

### Données de transcription

`TranscriptionData` contient :

* `text` : texte transcrit
* `language` : langue détectée
* `segments` : segments avec informations temporelles

### Gestion des erreurs

`404` :

Le fichier audio demandé n'existe pas.

`500` :

Une erreur de transcription interne est survenue.

### État

**Développé et intégré — Membre 2**

---

# 9. Pipeline IA

Le flux IA actuellement préparé est :

```text
Fichier uploadé
       ↓
   /extract
       ↓
Audio WAV
       ↓
 /transcribe
       ↓
TranscriptionService
       ↓
Faster-Whisper
       ↓
Texte + langue + segments
```

Le pipeline complet prévu du projet est :

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
Préparation des résultats
   ↓
Nettoyage
   ↓
Terminé
```

---

# 10. Modèles IA

## Faster-Whisper

Faster-Whisper est utilisé pour la transcription locale des fichiers audio.

### Configuration actuelle

```text
Modèle : base
Device : CPU
Compute type : int8
```

Le choix du modèle `base` résulte des tests comparatifs effectués sur la machine cible.

### Résultat

Le modèle `base` constitue actuellement le compromis retenu entre :

* temps de transcription
* consommation mémoire
* qualité de transcription

---

# 11. Summary API

## État actuel

Le module Summary fait partie des responsabilités du Membre 2.

L'architecture du projet prévoit l'utilisation optionnelle d'Ollama pour générer un résumé local de la transcription.

Cependant, aucun endpoint Summary final n'est actuellement exposé dans l'OpenAPI du backend.

### État

**À finaliser lors de l'implémentation Summary.**

---

# 12. OpenAPI

Le backend FastAPI expose automatiquement sa documentation OpenAPI.

Documentation interactive :

```text
GET /docs
```

Spécification OpenAPI :

```text
GET /openapi.json
```

Les routes actuellement visibles dans OpenAPI comprennent notamment :

```text
POST /upload/
POST /process/start
GET  /progress/{file_id}
GET  /download/{file_id}/{download_format}
GET  /health
POST /extract
POST /transcribe
```

---

# 13. Synchronisation Frontend / Backend

Les contrats définis dans ce document servent de référence pour l'intégration avec le Frontend.

Pour la partie IA, le Frontend doit respecter notamment les contrats :

```text
POST /extract
POST /transcribe
```

La réponse de transcription doit être interprétée à partir de :

```text
success
message
data.text
data.language
data.segments
job_id
```

Toute modification du contrat d'API doit être communiquée aux deux membres avant l'intégration.

---

# 14. État global

| Module        | Endpoint                                  | État                 |
| ------------- | ----------------------------------------- | -------------------- |
| Upload        | POST /upload/                             | Développé            |
| Process       | POST /process/start                       | Développé            |
| Progress      | GET /progress/{file_id}                   | Développé            |
| Download      | GET /download/{file_id}/{download_format} | Développé            |
| Health        | GET /health                               | Développé            |
| Quality       | Utilisé par ProcessService                | Développé            |
| Extract       | POST /extract                             | Développé            |
| Transcription | POST /transcribe                          | Développé — Membre 2 |
| Summary       | À définir                                 | À finaliser          |

---

## Validation de l'étape 1

Enregistre le fichier puis exécute :

```powershell
Get-Content .\docs\api\API_Contract.md -Raw
```

Puis vérifie que tu vois bien :

```text
# 7. Extract API
```

et :

```text
# 8. Transcription API
```

et surtout :

```text
POST /extract
POST /transcribe
```

---

# 🟡 Étape 2 — Performance Comparison

Ton fichier :

```text
docs/report_notes/Performance_Comparison.md
```

est actuellement **vide**.

C'est important de le corriger parce que les benchmarks Faster-Whisper ont déjà été réalisés pendant le travail de Membre 2.

Nous avons les résultats validés :

| Modèle | Chargement | Transcription | RAM après | Langue | Segments |
| ------ | ---------: | ------------: | --------: | ------ | -------: |
| tiny   |     1.50 s |        8.16 s | 139.14 MB | fr     |       12 |
| base   |     0.87 s |       11.98 s | 191.15 MB | fr     |       14 |
| small  |     2.00 s |       34.61 s | 366.35 MB | fr     |       18 |

Le choix retenu est :

> **`base` comme modèle principal**, car il offre un meilleur compromis que `tiny` et `small` pour la machine CPU-only.

### Fais maintenant cette commande :

```powershell
code .\docs\report_notes\Performance_Comparison.md
```

Puis remplace son contenu par le document suivant :

# Performance Comparison — Faster-Whisper

## Objectif

Cette étude compare plusieurs modèles Faster-Whisper afin de sélectionner le modèle le plus adapté à l'environnement matériel de TranscriBITE.

Le projet doit fonctionner localement sur une machine Windows sans GPU dédié.

Les critères étudiés sont :

* temps de chargement du modèle
* temps de transcription
* consommation mémoire
* détection de la langue
* nombre de segments générés
* stabilité de l'exécution

---

## Environnement de test

### Système

* Système : Windows
* CPU : Intel Core i5 8ème génération
* RAM : 16 GB
* GPU dédié : aucun
* Exécution : CPU

### Environnement Python

* Python : 3.12
* Faster-Whisper : 1.1.1 lors du benchmark
* Compute type : `int8`

### Fichier de test

Le benchmark a été réalisé avec un fichier audio de test identique pour les différents modèles afin de garantir une comparaison cohérente.

---

## Résultats

| Modèle | Temps chargement | Temps transcription | RAM avant | RAM après | Langue | Segments | Résultat |
| ------ | ---------------: | ------------------: | --------: | --------: | ------ | -------: | -------- |
| tiny   |           1.50 s |              8.16 s |  17.80 MB | 139.14 MB | fr     |       12 | Succès   |
| base   |           0.87 s |             11.98 s |  98.35 MB | 191.15 MB | fr     |       14 | Succès   |
| small  |           2.00 s |             34.61 s | 106.05 MB | 366.35 MB | fr     |       18 | Succès   |

---

## Analyse

### Modèle tiny

Le modèle `tiny` est le plus rapide.

Il présente également la plus faible consommation mémoire.

Cependant, sa capacité de transcription est inférieure aux modèles plus grands.

Il est intéressant lorsque la rapidité et la faible consommation de ressources sont prioritaires.

---

### Modèle base

Le modèle `base` présente un temps de transcription raisonnable tout en consommant beaucoup moins de mémoire que `small`.

La détection de la langue française fonctionne correctement.

Le modèle produit davantage de segments que `tiny`, ce qui fournit une structure temporelle plus détaillée.

Il constitue donc un bon compromis entre performance et qualité.

---

### Modèle small

Le modèle `small` fournit une transcription plus détaillée mais son temps d'exécution est nettement supérieur.

Sa consommation mémoire est également beaucoup plus importante.

Sur une machine CPU-only disposant de 16 GB de RAM, cette différence de coût doit être prise en compte.

---

## Comparaison

Le modèle `tiny` est le meilleur choix pour la rapidité.

Le modèle `small` est le plus coûteux en temps et en mémoire.

Le modèle `base` se situe entre les deux et fournit un compromis adapté aux contraintes du projet.

---

## Décision technique

Le modèle retenu pour TranscriBITE est :

```text
WHISPER_MODEL=base
```

Configuration :

```text
device=cpu
compute_type=int8
```

Cette configuration permet d'exécuter la transcription localement sans GPU dédié.

---

## Justification du choix

Le modèle `base` a été retenu pour les raisons suivantes :

1. temps de transcription acceptable
2. consommation mémoire raisonnable
3. détection correcte de la langue
4. fonctionnement stable sur CPU
5. meilleur compromis entre rapidité et qualité
6. compatibilité avec les contraintes matérielles du projet

---

## Conclusion

Les trois modèles testés fonctionnent correctement sur l'environnement CPU.

Le modèle `tiny` est le plus rapide mais privilégie les performances.

Le modèle `small` consomme davantage de ressources et augmente fortement le temps de transcription.

Le modèle `base` constitue le compromis retenu pour la version actuelle de TranscriBITE.

La configuration officielle utilisée par le backend est donc :

```text
WHISPER_MODEL=base
device=cpu
compute_type=int8
```
