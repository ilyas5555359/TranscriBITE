# Folder Structure — TranscriBITE

## 1. Présentation

Le projet TranscriBITE adopte une organisation modulaire permettant de séparer clairement les différentes parties de l'application.

Cette structure a été conçue pour faciliter :

* le développement parallèle entre les deux membres de l'équipe
* la maintenance du code
* l'évolution progressive des fonctionnalités
* l'intégration des différents modules
* la documentation technique du projet

L'architecture globale est divisée en plusieurs parties principales :

```text
TranscriBITE/

├── backend/

├── frontend/

├── storage/

├── logs/

├── scripts/

├── docs/

├── tests/

├── README.md

├── .gitignore

├── LICENSE

└── .editorconfig
```

## Organisation générale

### Backend

Le dossier `backend` contient toute la logique serveur développée avec FastAPI.

Il regroupe :

* les routes API
* les services métier
* les modèles de données
* les schémas de validation
* les outils utilitaires
* la gestion du pipeline de traitement

Le Backend est principalement sous la responsabilité du membre 1 pour la gestion des fichiers, du pipeline, de l'extraction audio, du suivi de progression et du téléchargement.

Le membre 2 intervient principalement dans les modules liés à l'intelligence artificielle :

* transcription avec Faster-Whisper
* génération de résumé avec Ollama

### Frontend

Le dossier `frontend` contient l'interface utilisateur développée avec React.

Il regroupe :

* les composants d'interface
* les pages
* les services de communication avec l'API
* les styles graphiques

Il permet à l'utilisateur d'importer un fichier, suivre son traitement et consulter les résultats.

### Storage

Le dossier `storage` contient les données temporaires et les fichiers générés pendant le fonctionnement de l'application.

Il est séparé du code source afin de faciliter :

* la gestion des fichiers utilisateurs
* le nettoyage des données temporaires
* la sauvegarde des résultats

### Documentation

Le dossier `docs` contient toute la documentation technique du projet.

Il regroupe :

* l'architecture
* les décisions techniques
* les contrats API
* les diagrammes UML
* les notes de développement
* les plans de test

### Tests

Le dossier `tests` contient les tests automatisés permettant de vérifier le bon fonctionnement des différents modules.

Cette organisation garantit une séparation claire entre le code de production et les tests.

Cette structure représente l'organisation officielle du projet TranscriBITE et sera maintenue à jour durant toutes les phases de développement.



## 2. Structure Backend

Le Backend de TranscriBITE est développé avec FastAPI et organisé selon une architecture modulaire.

Le dossier `backend` contient toute la logique serveur de l'application.

Sa structure principale est :

```text
backend/

├── app/

├── .env

├── .env.example

└── requirements.txt
```

---

## 2.1 Dossier app

Le dossier `app` contient le code source principal du Backend.

Il regroupe les différents modules nécessaires au fonctionnement de l'application.

Structure :

```text
app/

├── enums/

├── routers/

├── services/

├── schemas/

├── models/

├── utils/

├── config.py

└── main.py
```

---

## 2.2 Dossier enums

Le dossier `enums` centralise les valeurs constantes utilisées dans le pipeline de traitement.

Ces enums sont utilisés comme référence commune entre les différents modules Backend.

Ils permettent d'éviter l'utilisation de chaînes de caractères différentes selon les services et garantissent une communication cohérente entre :

* Process Service
* Progress Service
* Processing State
* API Progress

Il contient :

```text
enums/

├── pipeline_step.py

├── step_status.py

└── pipeline_order.py
```

Responsabilités :

* `PipelineStep` représente les différentes étapes du traitement.
* `StepStatus` représente l'état d'une étape.
* `PIPELINE_ORDER` définit l'ordre officiel d'exécution du pipeline.

Cette organisation garantit une cohérence entre les différents modules.

---

## 2.3 Dossier routers

Le dossier `routers` contient les points d'entrée API de l'application.

Chaque fichier représente un groupe de routes lié à une fonctionnalité.

Structure :

```text
routers/

├── upload.py

├── process.py

├── extract.py

├── transcription.py

├── summary.py

├── download.py

├── progress.py

└── health.py
```

Responsabilités :

* `upload.py` : réception des fichiers utilisateurs.
* `process.py` : lancement et orchestration du traitement.
* `extract.py` : gestion des opérations d'extraction audio.
* `transcription.py` : communication avec le service de transcription.
* `summary.py` : communication avec le service de résumé.
* `download.py` : téléchargement des résultats.
* `progress.py` : suivi de progression.
* `health.py` : vérification de l'état du système.

---

## 2.4 Dossier services

Le dossier `services` contient la logique métier de l'application.

Structure :

```text
services/

├── file_service.py

├── process_service.py

├── audio_service.py

├── quality_service.py

├── health_service.py

├── transcription_service.py

├── summary_service.py

├── download_service.py

└── progress_service.py
```

Responsabilités :

* `file_service.py` : gestion des fichiers importés.
* `process_service.py` : responsable de l'orchestration complète du pipeline de traitement, coordination des différents services, suivi de l'état d'exécution et lancement des étapes du processus.
Il coordonne :

- validation du fichier
- détection du média
- sélection du pipeline
- communication entre les services
- gestion centralisée des erreurs
- finalisation du traitement

* `audio_service.py` : traitement audio et extraction avec FFmpeg.
* `quality_service.py` : analyse de la qualité audio.
* `health_service.py` : service chargé des vérifications générales du système avant le lancement du pipeline.
* `transcription_service.py` : intégration Faster-Whisper.
* `summary_service.py` : génération de résumé avec Ollama.
* `download_service.py` : préparation des fichiers exportés.
* progress_service.py : gestion centralisée de l'état du pipeline, de la progression et des événements envoyés aux clients. Le Progress Service utilisera les enums définis dans le dossier enums afin de maintenir une cohérence avec le Process Service.

---

## 2.5 Dossier schemas

Le dossier `schemas` contient les modèles Pydantic utilisés pour les échanges de données.

Structure :

```text
schemas/

├── upload_schema.py

├── process_schema.py

├── extract_schema.py

├── transcription_schema.py

├── summary_schema.py

├── download_schema.py

├── progress_schema.py

├── health_schema.py

└── error_schema.py
```

Ils permettent :

* la validation des données entrantes ;
* la définition des réponses API ;
* la documentation automatique des endpoints.

---

* process_schema.py : définit les modèles utilisés par le module Process pour suivre l'exécution du pipeline.

Il contient notamment :

* `ProcessingStep` : représentation d'une étape individuelle du pipeline
* `ProcessingStatus` : état global du traitement d'un fichier
* `ProcessResponse` : réponse retournée après lancement du traitement

Il utilise les enums :

* `PipelineStep`
* `StepStatus`

afin de garantir une cohérence entre les différents modules Backend.

---

## 2.6 Dossier models

Le dossier `models` contient les structures internes utilisées pendant le traitement.

Structure :

```text
models/

├── file_metadata.py

├── processing_state.py

└── transcription_result.py
```

Responsabilités :

* `file_metadata.py` : informations sur les fichiers.
* processing_state.py : représentation interne de l'état du traitement avec utilisation des enums du pipeline.
    Ce modèle sera utilisé par le système de suivi de progression afin de conserver :
    * l'étape actuelle
    * le statut de traitement
    * le pourcentage d'avancement
    * le message associé
    * les informations temporelles

* `transcription_result.py` : structure des résultats de transcription.

---

## 2.7 Dossier utils

Le dossier `utils` contient les fonctions communes utilisées par plusieurs modules.

Structure :

```text
utils/

├── validators.py

├── logger.py

├── file_utils.py

├── ffmpeg_utils.py

└── whisper_utils.py
```

Responsabilités :

* validation des données ;
* gestion des fichiers ;
* communication avec FFmpeg ;
* fonctions liées à Whisper ;
* gestion des logs.

---

## 2.8 Fichiers principaux

### main.py

Point d'entrée principal de l'application FastAPI.

Responsabilités :

* création de l'application ;
* chargement des routes ;
* configuration globale.

### `.venv`

Le dossier `backend/.venv` contient l'environnement virtuel Python utilisé exclusivement par le Backend TranscriBITE.

Il n'est pas destiné à être versionné dans Git.

### `requirements.txt`

Le fichier `backend/requirements.txt` contient les dépendances de l'environnement Python validé.

### config.py

Centralise la configuration de l'application.

Il contient notamment :

* chemins de stockage ;
* paramètres généraux ;
* variables provenant du fichier `.env`.



## 3. Structure Frontend

Le Frontend de TranscriBITE est développé avec React afin de fournir une interface utilisateur dynamique et organisée.

La structure Frontend suit une organisation basée sur les composants afin de faciliter la réutilisation du code et la maintenance de l'application.

Structure principale :

```text
frontend/

├── public/

├── src/

│   ├── assets/

│   ├── components/

│   ├── pages/

│   ├── services/

│   ├── styles/

│   ├── App.jsx

│   ├── main.jsx

│   └── index.css

└── package.json
```

## 3.1 Dossier components

Le dossier `components` contient les composants réutilisables de l'interface.

Structure :

```text
components/

├── Header.jsx

├── LanguageSelector.jsx

├── FileUploader.jsx

├── FileInformation.jsx

├── StartProcessingButton.jsx

├── ProgressTracker.jsx

├── TranscriptViewer.jsx

├── SummaryViewer.jsx

├── TranscriptionInformation.jsx

├── DownloadButtons.jsx

├── ErrorMessage.jsx

└── Footer.jsx
```

Responsabilités :

* `Header.jsx` : affichage de l'en-tête de l'application.
* `LanguageSelector.jsx` : sélection de la langue de transcription.
* `FileUploader.jsx` : import et envoi des fichiers.
* `FileInformation.jsx` : affichage des informations du fichier.
* `StartProcessingButton.jsx` : lancement manuel du traitement.
* `ProgressTracker.jsx` : affichage de l'état du pipeline.
* `TranscriptViewer.jsx` : affichage de la transcription.
* `SummaryViewer.jsx` : affichage du résumé généré.
* `TranscriptionInformation.jsx` : affichage des informations liées au résultat.
* `DownloadButtons.jsx` : téléchargement des résultats.
* `ErrorMessage.jsx` : affichage des erreurs.
* `Footer.jsx` : pied de page.

## 3.2 Dossier pages

Le dossier `pages` contient les différentes pages principales de l'application.

Structure :

```text
pages/

└── Home.jsx
```

La page `Home.jsx` représente l'interface principale de TranscriBITE.

Elle regroupe les composants nécessaires au workflow utilisateur.

## 3.3 Dossier services

Le dossier `services` contient les fonctions de communication avec le Backend.

Structure :

```text
services/

└── api.js
```

Le fichier `api.js` centralise les appels vers l'API FastAPI.

Il permet :

* l'envoi des fichiers
* le lancement du traitement
* la récupération de la progression
* la récupération des résultats
* le téléchargement

## 3.4 Dossier styles

Le dossier `styles` contient l'organisation graphique de l'application.

Structure :

```text
styles/

├── global.css

├── variables.css

└── components.css
```

Responsabilités :

* `global.css` : styles généraux.
* `variables.css` : variables de design.
* `components.css` : styles spécifiques aux composants.

## 3.5 Dossiers assets et fichiers principaux

### assets

Contient les ressources graphiques :

* logo
* icônes
* images

### App.jsx

Point principal de composition de l'application React.

### main.jsx

Point d'entrée du rendu React.

### package.json

Contient les dépendances et les scripts du projet Frontend.



## 4. Structure Storage

Le dossier `storage` contient les fichiers manipulés par l'application pendant le cycle de traitement.

Il est séparé du code source afin de garantir une meilleure organisation des données et faciliter la gestion des fichiers temporaires.

Structure :

```text
storage/

├── uploads/

├── outputs/

├── temp/

├── cache/

└── samples/
```

---

## 4.1 Dossier uploads

Le dossier `uploads` contient les fichiers importés par l'utilisateur.

Exemples :

* fichiers audio
* fichiers vidéo

Il représente le point d'entrée du pipeline de traitement.

Workflow :

```text
Utilisateur

↓

Upload API

↓

storage/uploads
```

Les fichiers reçus passent ensuite par les étapes de validation et d'analyse.

---

## 4.2 Dossier outputs

Le dossier `outputs` contient les résultats générés par l'application.

Il peut contenir :

* fichiers texte de transcription
* fichiers JSON
* futurs exports PDF

Ce dossier est utilisé par le module Download afin de préparer les fichiers accessibles à l'utilisateur.

---

## 4.3 Dossier temp

Le dossier `temp` contient les fichiers temporaires nécessaires pendant le traitement.

Exemples :

* fichiers audio extraits depuis une vidéo
* fichiers intermédiaires générés par FFmpeg

Ces fichiers peuvent être supprimés automatiquement après la fin du traitement grâce au module de nettoyage.

---

## 4.4 Dossier cache

Le dossier `cache` contient les données temporaires permettant d'améliorer les performances.

Il pourra être utilisé pour :

* éviter certains traitements répétés
* conserver des résultats intermédiaires
* optimiser les traitements futurs

---

## 4.5 Dossier samples

Le dossier `samples` contient des fichiers d'exemple utilisés pour :

* les tests
* la validation du pipeline
* les démonstrations

Ces fichiers permettent de vérifier le fonctionnement de l'application sans utiliser des fichiers utilisateurs réels.

---

## Gestion du cycle de vie des fichiers

Le cycle général des fichiers est :

```text
Upload

↓

Validation

↓

Détection média

↓

Analyse qualité

↓

Extraction audio si nécessaire

↓

Transcription

↓

Résumé

↓

Préparation résultats

↓

Nettoyage

↓

Terminé
```

Cette organisation permet de suivre clairement l'évolution d'un fichier durant son traitement.



## 5. Structure Logs

Le dossier `logs` contient les fichiers de journalisation générés pendant l'exécution de TranscriBITE.

Les logs permettent de suivre les opérations réalisées par l'application et facilitent l'identification des problèmes rencontrés pendant le traitement.

Structure :

```text
logs/

├── application.log

├── ffmpeg.log

├── whisper.log

├── errors.log

└── .gitkeep
```

---

## 5.1 application.log

Le fichier `application.log` contient les informations générales liées au fonctionnement de l'application.

Il permet de suivre :

* le démarrage du serveur.
* les requêtes principales.
* les étapes du pipeline.
* les opérations importantes réalisées par les services.

Exemples :

* réception d'un fichier.
* lancement d'un traitement.
* changement d'état du pipeline.

---

## 5.2 ffmpeg.log

Le fichier `ffmpeg.log` contient les informations liées aux opérations multimédias réalisées avec FFmpeg.

Il permet de suivre :

* l'extraction audio depuis une vidéo.
* les conversions de formats.
* les erreurs liées au traitement média.

Ce fichier est principalement utilisé par :

* `audio_service.py`
* `ffmpeg_utils.py`

---

## 5.3 whisper.log

Le fichier `whisper.log` contient les informations liées au moteur de transcription.

Il permet de suivre :

* le lancement de la transcription.
* les informations du modèle utilisé.
* les problèmes rencontrés pendant la transcription.

Ce fichier sera principalement utilisé par :

* `transcription_service.py`
* `whisper_utils.py`

---

## 5.4 errors.log

Le fichier `errors.log` contient les erreurs importantes détectées pendant l'exécution.

Il permet de centraliser :

* les erreurs du pipeline.
* les erreurs de validation.
* les erreurs des services.
* les exceptions critiques.

Il facilite l'analyse des problèmes et leur résolution.

---

## 5.5 .gitkeep

Le fichier `.gitkeep` permet de conserver le dossier `logs` dans le dépôt Git même lorsque les fichiers de logs n'existent pas encore.

Les fichiers générés pendant l'exécution ne sont généralement pas versionnés.

---

## Gestion des logs dans l'application

La gestion des logs suit une organisation centralisée :

```text
Module Backend

      |

      v

utils/logger.py

      |

      v

Fichiers logs
```

Cette approche évite la création de systèmes de journalisation différents dans chaque module.



## 6. Structure Scripts

Le dossier `scripts` contient les scripts utilitaires permettant d'automatiser certaines opérations de configuration et de maintenance du projet.

Ces scripts ne font pas partie du fonctionnement principal de l'application mais facilitent son installation et son administration.

Structure :

```text
scripts/

├── README.md

├── create_folders.py

├── clean_temp.py

├── check_environment.py

└── install_models.py
```

---

## 6.1 README.md

Le fichier `README.md` explique l'utilisation des différents scripts disponibles.

Il contient :

* leur objectif ;
* leur utilisation ;
* les commandes nécessaires pour les exécuter.

---

## 6.2 create_folders.py

Ce script permet de créer automatiquement les dossiers nécessaires au fonctionnement de l'application.

Il peut notamment créer :

```text
storage/

├── uploads/

├── outputs/

├── temp/

├── cache/

└── samples/
```

Il permet de simplifier l'installation initiale du projet.

---

## 6.3 clean_temp.py

Ce script permet de nettoyer les fichiers temporaires générés pendant le traitement.

Il intervient principalement sur :

```text
storage/temp/
```

Il peut être utilisé :

* après un traitement terminé.
* lors de la maintenance.
* pour libérer de l'espace disque.

---

## 6.4 check_environment.py

Ce script vérifie que l'environnement d'exécution est correctement configuré.

Il peut contrôler :

* la version de Python.
* la présence de FFmpeg.
* les dépendances installées.
* l'accès aux dossiers nécessaires.
* la configuration générale.

---

## 6.5 install_models.py

Ce script prépare l'installation des modèles nécessaires aux fonctionnalités d'intelligence artificielle.

Il peut gérer :

* l'installation des modèles Faster-Whisper.
* la préparation des modèles Ollama.
* la vérification de leur disponibilité.

---

## Rôle général des scripts

Les scripts permettent d'améliorer :

* la simplicité d'installation.
* la reproductibilité de l'environnement.
* la maintenance du projet.
* la préparation des tests.



## 7. Structure Documentation

Le dossier `docs` contient l'ensemble de la documentation technique et de suivi du projet TranscriBITE.

Cette organisation permet de conserver les informations importantes concernant l'architecture, les décisions techniques, les tests et l'évolution du projet.

Structure :

```text
docs/

├── architecture/

├── uml/

├── api/

├── installation/

├── report_notes/

├── testing/

├── meeting_notes/

├── changelog/

└── Workflow.md
```

---

## 7.1 Dossier architecture

Le dossier `architecture` contient les documents décrivant la conception générale du système.

Structure :

```text
architecture/

├── Architecture.md

├── Folder_Structure.md

├── Workflow_Processing.md

└── Technical_Decisions.md
```

Responsabilités :

* `Architecture.md` : description générale de l'architecture.
* `Folder_Structure.md` : organisation des dossiers et fichiers.
* `Workflow_Processing.md` : description du pipeline de traitement.
* `Technical_Decisions.md` : justification des choix techniques.

---

## 7.2 Dossier uml

Le dossier `uml` contient les diagrammes de conception réalisés avec PlantUML.

Structure :

```text
uml/

├── use_case.puml

├── sequence.puml

├── class_diagram.puml

├── component_diagram.puml

├── deployment_diagram.puml

└── README.md
```

Ces diagrammes permettent de représenter :

* les interactions utilisateur.
* les séquences de traitement.
* les classes principales.
* les composants du système.
* le déploiement de l'application.

---

## 7.3 Dossier api

Le dossier `api` contient la documentation des interfaces de communication entre le Frontend et le Backend.

Structure :

```text
api/

└── API_Contract.md
```

Ce document décrit :

* les endpoints disponibles.
* les paramètres nécessaires.
* les formats de requêtes.
* les formats de réponses.
* les erreurs possibles.

---

## 7.4 Dossier installation

Le dossier `installation` contient les informations nécessaires pour installer et configurer le projet.

Il peut contenir :

* prérequis système.
* installation Backend.
* installation Frontend.
* configuration des modèles IA.
* configuration environnement.

---

## 7.5 Dossier report_notes

Le dossier `report_notes` contient les informations utilisées pour préparer le rapport de stage.

Structure :

```text
report_notes/

├── Daily_Notes.md

├── Technical_Choices.md

├── Problems_and_Solutions.md

├── Performance_Comparison.md

└── Future_Improvements.md
```

Responsabilités :

* `Daily_Notes.md` : suivi quotidien du développement.
* `Technical_Choices.md` : décisions techniques importantes.
* `Problems_and_Solutions.md` : problèmes rencontrés et solutions appliquées.
* `Performance_Comparison.md` : analyse des performances.
* `Future_Improvements.md` : améliorations possibles.

Les fichiers de ce dossier seront mis à jour progressivement pendant le développement afin de conserver une trace des choix réalisés, des problèmes rencontrés et des améliorations futures.
---

## 7.6 Dossier testing

Le dossier `testing` contient la documentation liée aux tests.

Structure :

```text
testing/

├── Test_Plan.md

├── Test_Cases.md

└── Test_Results.md
```

Responsabilités :

* définir la stratégie de test.
* décrire les scénarios.
* conserver les résultats obtenus.

---

## 7.7 Dossier meeting_notes

Le dossier `meeting_notes` contient les comptes rendus importants des réunions et décisions prises pendant le projet.

Il peut contenir :

* décisions d'équipe.
* changements d'organisation.
* points de coordination.

---

## 7.8 Dossier changelog

Le dossier `changelog` contient l'historique des modifications importantes du projet.

Structure :

```text
changelog/

└── CHANGELOG.md
```

Il permet de suivre :

* les nouvelles fonctionnalités.
* les corrections.
* les changements d'architecture.

---

## 7.9 Workflow.md

Le fichier `Workflow.md` décrit le fonctionnement global de l'application.

Il présente :

* le parcours utilisateur.
* le pipeline complet.
* les interactions entre les modules.

Cette documentation évoluera avec l'avancement du développement.



## 8. Structure Tests

Le dossier `tests` contient l'ensemble des tests automatisés du projet TranscriBITE.

Il est séparé du code principal afin de garantir une meilleure organisation entre les fonctionnalités de l'application et leur validation.

Les tests permettent de vérifier :

* le fonctionnement des modules Backend
* le comportement des composants Frontend
* la stabilité du pipeline de traitement
* la correction des erreurs après modification

Structure :

```text id="4v8f6b"
tests/

├── backend/

│   ├── test_upload.py

│   ├── test_validation.py

│   ├── test_download.py

│   └── test_progress.py

│

└── frontend/

    ├── test_home.jsx

    └── test_upload.jsx
```

---

## 8.1 Tests Backend

Le dossier `backend` contient les tests liés à l'API FastAPI et aux services Backend.

Structure :

```text id="3pv7yq"
backend/

├── test_upload.py

├── test_validation.py

├── test_download.py

└── test_progress.py
```

---

## 8.1.1 test_upload.py

Ce fichier vérifie le fonctionnement du module d'import des fichiers.

Il permet de tester :

* réception d'un fichier
* création de l'identifiant unique
* sauvegarde dans le dossier uploads
* retour de la réponse API

Module associé :

```text id="p5b2sf"
routers/upload.py

services/file_service.py
```

---

## 8.1.2 test_validation.py

Ce fichier vérifie les règles de validation des fichiers.

Il permet de tester :

* extensions autorisées
* types MIME
* taille maximale
* fichiers invalides

Modules associés :

```text id="r2m1xv"
utils/validators.py

upload_schema.py
```

---

## 8.1.3 test_download.py

Ce fichier vérifie la génération et la récupération des résultats.

Il permet de tester :

* création des fichiers résultats
* téléchargement TXT
* téléchargement JSON
* gestion des erreurs

Modules associés :

```text id="zn9v1w"
download.py

download_service.py
```

---

## 8.1.4 test_progress.py

Ce fichier vérifie le suivi de l'état du traitement.

Il permet de tester :

* changement des étapes du pipeline
* pourcentage de progression
* messages d'état
* erreurs pendant le traitement

Modules associés :

```text id="2hplra"
progress.py

progress_service.py

processing_state.py
```

---

## 8.2 Tests Frontend

Le dossier `frontend` contient les tests des composants React.

Structure :

```text id="x0o3fm"
frontend/

├── test_home.jsx

└── test_upload.jsx
```

---

## 8.2.1 test_home.jsx

Ce fichier vérifie l'affichage général de l'application.

Il permet de tester :

* chargement de la page principale
* présence des composants principaux
* navigation utilisateur

---

## 8.2.2 test_upload.jsx

Ce fichier vérifie le comportement du composant d'import.

Il permet de tester :

* sélection d'un fichier
* affichage des informations
* interaction avec le bouton de lancement

Module associé :

```text id="8yq2t6"
components/FileUploader.jsx
```

---

## Organisation des tests

La stratégie générale suit cette logique :

```text id="d4qj3b"
Développement module

↓

Création du test associé

↓

Exécution du test

↓

Correction des erreurs

↓

Validation du module
```

Cette organisation sera utilisée pendant les phases de développement et d'intégration.



## 9. Fichiers principaux du projet

La racine du projet TranscriBITE contient plusieurs fichiers importants permettant de gérer la documentation, la configuration du dépôt et les règles de développement.

Structure :

```text
TranscriBITE/

├── README.md

├── .gitignore

├── LICENSE

└── .editorconfig
```

---

## 9.1 README.md

Le fichier `README.md` est le document principal de présentation du projet.

Il contient :

* la description de TranscriBITE
* les objectifs de l'application
* les technologies utilisées
* les instructions d'installation
* les instructions d'utilisation
* l'organisation générale du projet

Il permet à un nouveau développeur de comprendre rapidement le fonctionnement de l'application.

---

## 9.2 .gitignore

Le fichier `.gitignore` définit les fichiers et dossiers qui ne doivent pas être envoyés dans le dépôt Git.

Il permet notamment d'exclure :

* environnements virtuels Python
* dépendances installées localement
* fichiers temporaires
* logs générés
* fichiers de configuration sensibles

Exemples :

```text
.env

__pycache__/

*.log

node_modules/
```

---

## 9.3 LICENSE

Le fichier `LICENSE` définit les règles d'utilisation et de distribution du projet.

Il précise :

* les droits d'utilisation
* les conditions de modification
* les règles de partage du code

---

## 9.4 .editorconfig

Le fichier `.editorconfig` permet d'unifier les règles de développement entre les membres de l'équipe.

Il définit notamment :

* indentation
* encodage des fichiers
* fin de ligne
* formatage général

Cette configuration garantit une meilleure cohérence du code entre les différents environnements de développement.

---

## Conclusion de la structure du projet

L'organisation complète de TranscriBITE suit une architecture modulaire séparant clairement :

* Backend
* Frontend
* Données temporaires
* Logs
* Scripts
* Documentation
* Tests

Cette séparation facilite :

* le développement parallèle entre les membres
* la maintenance du projet
* l'évolution future de l'application
* la préparation de la documentation finale

Cette structure représente l'organisation officielle validée du projet TranscriBITE.
