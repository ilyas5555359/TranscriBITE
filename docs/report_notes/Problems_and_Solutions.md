# Problems and Solutions — TranscriBITE

## Présentation

Ce document présente les problèmes rencontrés pendant le développement du projet TranscriBITE ainsi que les solutions appliquées.

Il permet de garder une trace des difficultés techniques et organisationnelles rencontrées durant les différentes phases du projet.

Chaque nouveau problème important sera ajouté avec sa cause, son impact et sa solution.

---

# 1. Organisation initiale du projet

## Problème

Au début du projet, l'organisation des fichiers et des responsabilités n'était pas encore clairement définie.

Cela pouvait provoquer :

* mélange des responsabilités entre modules
* difficulté de maintenance
* risque de conflit entre les deux membres

## Cause

Absence d'une structure technique détaillée avant le développement.

## Solution appliquée

Création d'une architecture modulaire séparant :

```text
backend

frontend

storage

logs

scripts

docs

tests
```

Puis séparation du Backend en modules :

```text
routers

services

schemas

models

utils
```

## Résultat

Le projet possède maintenant une organisation claire permettant un développement parallèle.

---

# 2. Séparation des responsabilités entre les membres

## Problème

Le projet contient plusieurs domaines techniques différents :

* gestion des fichiers
* traitement multimédia
* transcription
* intelligence artificielle
* interface utilisateur

Sans séparation claire, il existe un risque de modifier les mêmes parties du code.

## Cause

Plusieurs fonctionnalités utilisent le même pipeline global.

## Solution appliquée

Définition des responsabilités :

## Membre 1

Responsable de :

* upload
* validation
* gestion fichiers
* FFmpeg
* qualité audio
* progression
* téléchargement
* frontend

## Membre 2

Responsable de :

* Faster-Whisper
* transcription
* Ollama
* génération résumé
* résultats IA

## Résultat

Chaque membre possède des modules dédiés avec intégration planifiée.

---

# 3. Gestion des états du pipeline

## Problème

L'utilisation de simples chaînes de caractères pour représenter les étapes du traitement pouvait provoquer des erreurs.

Exemple :

```python
status = "processing"
```

ou :

```python
status = "Processing"
```

Ces valeurs peuvent devenir incohérentes.

## Cause

Absence d'une gestion centralisée des états.

## Solution appliquée

Création d'un système basé sur des Enum :

```text
backend/app/enums/

pipeline_step.py

step_status.py

pipeline_order.py
```

Les étapes officielles sont :

```text
Upload

Validation

Détection du média

Analyse qualité audio

Extraction audio

Transcription

Génération résumé

Préparation résultats

Nettoyage

Terminé

Échoué
```

Les statuts possibles :

```text
En attente

En cours

Terminée

Échec
```

## Résultat

Le pipeline possède maintenant une gestion standardisée et évolutive.

---

# 4. Difficulté de gestion de la structure documentaire

## Problème

Plusieurs fichiers de documentation étaient prévus mais aucun suivi global n'était encore établi.

## Cause

Le développement avait commencé avant la création complète de la documentation.

## Solution appliquée

Création d'un tableau de suivi documentaire contenant :

* état de chaque document
* action actuelle
* moment de mise à jour

## Résultat

La documentation devient une partie intégrée du développement.

---

# 5. Problème d'environnement Backend

## Problème : Commandes PowerShell non reconnues

## Description

Certaines commandes Linux utilisées pour créer les fichiers ne fonctionnaient pas dans PowerShell.

Lors du lancement du serveur FastAPI, la commande :

```bash
uvicorn app.main:app --reload
```

n'était pas reconnue.

Erreur rencontrée :

```text
uvicorn n'est pas reconnu comme nom d'applet de commande
```

## Cause

Le terminal ne trouvait pas l'environnement Python contenant les dépendances.

## Solution appliquée

* Adapter les commandes à l'environnement Windows ou utiliser directement VS Code Explorer.
* Vérification de :
    * installation des dépendances
    * activation de l'environnement virtuel
    * chemin du projet
    * configuration du terminal VS Code

## Impact

Pas d'impact sur l'architecture.

## Résultat

L'environnement de développement peut être configuré correctement.

---

# 6. Gestion de l'évolution de l'architecture

## Problème

L'ajout progressif des modules pouvait modifier la structure initialement prévue.

## Cause

Le projet évolue pendant le développement.

## Solution appliquée

Adoption d'une règle :

Après chaque nouveau module :

1. Vérifier l'impact architecture
2. Modifier la documentation concernée
3. Mettre à jour les tableaux de suivi
4. Informer l'autre membre

## Résultat

La documentation reste synchronisée avec le code.

---

# 7. Construction anticipée du pipeline Process

## Problème

Le module Process dépend de plusieurs services (FileService, AudioService, QualityService, TranscriptionService, SummaryService, DownloadService et ProgressService) qui ne sont pas encore entièrement développés.

## Cause

Le ProcessService est l'orchestrateur principal du backend et nécessite l'intervention de nombreux modules développés progressivement au cours du projet.

## Solution appliquée

L'architecture complète du ProcessService a été conçue dès le Jour 6.

Toutes les méthodes du pipeline ont été définies, même lorsque leur implémentation n'était pas encore disponible, à l'aide de méthodes asynchrones et de `NotImplementedError`.

Cette approche garantit une architecture stable et évite toute modification importante lors de l'intégration des services.

## Résultat

Le pipeline principal est entièrement structuré.

Les futurs développements pourront être intégrés sans modifier l'architecture existante.

---

# 8. Préparation des formats de téléchargement

## Problème

Les fichiers de sortie (TXT, JSON et PDF) ne pouvaient pas être générés tant que les modules de transcription et de résumé n'étaient pas disponibles.

## Cause

Le développement du module Download dépend des données produites par les services développés par le membre 2.

## Solution appliquée

Création d'une architecture complète du module Download avec des méthodes dédiées à chaque format de sortie, tout en reportant la logique métier à la phase d'intégration.

## Résultat

Le module Download est totalement prêt pour recevoir les données produites par le pipeline sans nécessiter de modification de son architecture.

---

# 9. Uniformisation du module Health

## Problème

La structure initiale ne prévoyait pas de `HealthService`.

## Cause

Le module Health avait été envisagé comme un simple endpoint.

## Solution appliquée

Création d'un service dédié afin de respecter l'architecture adoptée depuis le début du projet.

## Résultat

Tous les modules Backend utilisent désormais la même organisation :

Router

↓

Service

↓

Schema

Cette cohérence simplifie les tests, la maintenance et les évolutions futures.

---

# 9.1 Répartition des responsabilités entre FileService et QualityService

## Problème

La vérification de l'existence d'un fichier pouvait être réalisée directement dans `QualityService`, ce qui entraînait une duplication des responsabilités.

## Cause

Plusieurs services du backend utilisent des fichiers stockés localement et pourraient chacun implémenter leur propre vérification.

## Solution appliquée

Création d'une fonction `check_file_exists()` dans `FileService`, réutilisable par tous les autres services.

## Résultat

La validation de l'existence des fichiers est centralisée dans un seul module, ce qui améliore la maintenabilité et limite les duplications de code.

---

# 9.2 Architecture du QualityService

## Problème

Déterminer si le QualityService devait manipuler un UUID ou directement un chemin de fichier.

## Cause

Plusieurs services utilisent des UUID alors que l'analyse audio nécessite un accès direct au fichier.

## Solution appliquée

Le ProcessService reste responsable de l'orchestration.

Le QualityService reçoit directement un objet `Path`.

La vérification de l'existence du fichier est centralisée dans FileService.

## Résultat

Les responsabilités restent clairement séparées et l'architecture est plus cohérente.

---

# Problèmes futurs prévus

Les prochains problèmes possibles seront documentés pendant :

* intégration Faster-Whisper
* optimisation CPU
* gestion des gros fichiers
* communication Frontend Backend
* tests complets
* performances

---

# 10. Préparation de l'environnement IA

## Problème : Python 3.12 non sélectionné par défaut

### Description

Le projet utilisait initialement une autre version de Python dans le terminal.

### Cause

Plusieurs versions de Python étaient présentes sur la machine.

### Solution appliquée

Python 3.12.10 a été installé puis utilisé explicitement pour créer `backend/.venv` :

```powershell
py -3.12 -m venv .venv
```

Le projet utilise ensuite le Python du `.venv`.

### Résultat

Le Backend utilise Python 3.12.10 indépendamment de la version Python système.

## Problème : activation du .venv bloquée par PowerShell

### Description

`Activate.ps1` était bloqué par la politique d'exécution PowerShell.

### Solution appliquée

La configuration PowerShell a été ajustée afin de permettre l'activation de l'environnement virtuel.

### Résultat

L'environnement est maintenant activable avec :

```powershell
.\.venv\Scripts\Activate.ps1
```

## Problème : FFmpeg non reconnu

### Description

La commande `ffmpeg` n'était pas reconnue alors que FFmpeg était installé.

### Cause

Le dossier contenant `ffmpeg.exe` n'était pas accessible depuis le PATH.

### Solution appliquée

Le dossier suivant a été ajouté au PATH :

```text
E:\FFmpeg files\bin
```

### Résultat

La commande `ffmpeg -version` fonctionne.

## Problème : Ollama non reconnu

### Description

La commande `ollama` n'était pas reconnue après l'installation.

### Cause

Le dossier de l'exécutable n'était pas accessible depuis le PATH.

### Solution appliquée

Le dossier suivant a été ajouté au PATH :

```text
E:\Users\Default\Ollama
```

### Résultat

`ollama --version` et `ollama list` fonctionnent.

## Problème : téléchargement initial de Torch interrompu

### Description

Le premier téléchargement de Torch a échoué avec une erreur SSL :

```text
DECRYPTION_FAILED_OR_BAD_RECORD_MAC
```

### Cause

Une erreur de communication SSL est apparue pendant le téléchargement du paquet.

### Solution appliquée

Le téléchargement a été relancé et l'environnement a ensuite été validé par la présence de Torch et de ses dépendances dans `requirements.txt`.

### Résultat

Torch CPU est présent dans l'environnement validé.

## Problème : Ollama déjà actif

### Description

La commande `ollama serve` a retourné une erreur indiquant que le port `127.0.0.1:11434` était déjà utilisé.

### Cause

Une instance Ollama était déjà active.

### Solution appliquée

Aucune seconde instance n'a été lancée. `ollama list` a été utilisé pour vérifier que le service répondait correctement.

### Résultat

Le service Ollama local est fonctionnel.

## Problème : validation du Backend après changement d'environnement

### Description

Le Backend devait être vérifié après migration vers Python 3.12.

### Solution appliquée

Le Backend a été lancé avec :

```powershell
python -m uvicorn app.main:app --reload
```

Puis les routes `/` et `/docs` ont été testées.

### Résultat

Le démarrage de FastAPI et les réponses HTTP `200 OK` ont été validés.

---

# Jour 11 — Documentation technique

## Synchronisation des documents

### Problème

Plusieurs documents décrivaient les mêmes composants du projet sous des angles différents.

### Solution

Une vérification croisée de la documentation a été réalisée afin d'assurer la cohérence entre :

- architecture
- workflow
- API
- choix techniques
- tests
- installation
- changelog

Les documents ont été mis à jour sans modifier les décisions déjà validées.
