# Test Cases

## Présentation

Ce document recense les différents cas de test prévus pour le projet **TranscriBITE**.

Chaque cas de test décrit une fonctionnalité qui devra être vérifiée afin de garantir le bon fonctionnement de l'application.

Les résultats de ces tests seront consignés dans **Test_Results.md**.

---

# Module Upload

## TC-UP-01

Nom :

Import d'un fichier audio valide.

Objectif :

Vérifier qu'un fichier audio valide est correctement importé.

Résultat attendu :

Le fichier est enregistré dans le dossier Uploads et un UUID est généré.

---

## TC-UP-02

Nom :

Import d'un fichier vidéo valide.

Objectif :

Vérifier qu'un fichier vidéo valide est correctement importé.

Résultat attendu :

Le fichier est enregistré avec succès.

---

## TC-UP-03

Nom :

Extension non autorisée.

Objectif :

Vérifier le rejet des extensions interdites.

Résultat attendu :

Une erreur de validation est retournée.

---

## TC-UP-04

Nom :

Type MIME invalide.

Objectif :

Vérifier la validation du type MIME.

Résultat attendu :

Le fichier est refusé.

---

## TC-UP-05

Nom :

Fichier vide.

Objectif :

Vérifier la gestion des fichiers vides.

Résultat attendu :

Une erreur est retournée.

---

## TC-UP-06

Nom :

Fichier dépassant la taille maximale.

Objectif :

Vérifier la limitation de taille.

Résultat attendu :

Le fichier est refusé.

---

# Module Process

## TC-PR-01

Nom :

Initialisation du pipeline.

Objectif :

Vérifier le démarrage du traitement.

Résultat attendu :

Le pipeline démarre correctement.

---

## TC-PR-02

Nom :

Détection automatique du type de média.

Objectif :

Vérifier la distinction Audio / Vidéo.

Résultat attendu :

Le pipeline approprié est sélectionné.

---

## TC-PR-03

Nom :

Erreur pendant le traitement.

Objectif :

Vérifier la gestion des exceptions.

Résultat attendu :

Le traitement est interrompu et l'erreur est enregistrée.

---

# Module Progress

## TC-PG-01

Nom :

Initialisation de la progression.

Objectif :

Vérifier la création d'un nouvel état.

Résultat attendu :

La progression démarre à 0 %.

---

## TC-PG-02

Nom :

Mise à jour de la progression.

Objectif :

Vérifier la mise à jour des informations de progression.

Résultat attendu :

Les données sont correctement mises à jour.

---

## TC-PG-03

Nom :

Fin du traitement.

Objectif :

Vérifier l'état final.

Résultat attendu :

Le statut passe à COMPLETED.

---

# Module Download

## TC-DL-01

Nom :

Téléchargement TXT.

Objectif :

Vérifier le téléchargement du fichier texte.

Résultat attendu :

Le fichier TXT est généré.

---

## TC-DL-02

Nom :

Téléchargement JSON.

Objectif :

Vérifier le téléchargement JSON.

Résultat attendu :

Le fichier JSON est généré.

---

## TC-DL-03

Nom :

Format invalide.

Objectif :

Vérifier la validation du format demandé.

Résultat attendu :

Une erreur est retournée.

---

# Module Health

## TC-HL-01

Nom :

Vérification du Backend.

Objectif :

Contrôler l'état du Backend.

Résultat attendu :

Le Backend est disponible.

---

## TC-HL-02

Nom :

Vérification du stockage.

Objectif :

Contrôler les dossiers nécessaires.

Résultat attendu :

Tous les dossiers existent.

---

## TC-HL-03

Nom :

Vérification de FFmpeg.

Objectif :

Contrôler la disponibilité de FFmpeg.

Résultat attendu :

FFmpeg est détecté.

---

# Module Quality

## TC-QL-01

Nom :

Analyse de la taille du fichier.

Objectif :

Vérifier la récupération de la taille.

Résultat attendu :

La taille est correctement calculée.

---

## TC-QL-02

Nom :

Analyse de la durée.

Objectif :

Vérifier la récupération de la durée.

Résultat attendu :

La durée est correcte.

---

## TC-QL-03

Nom :

Analyse du débit audio.

Objectif :

Vérifier la récupération du bitrate.

Résultat attendu :

Le débit est correctement détecté.

---

## TC-QL-04

Nom :

Analyse de la fréquence d'échantillonnage.

Objectif :

Vérifier la récupération du sample rate.

Résultat attendu :

La fréquence est correcte.

---

## TC-QL-05

Nom :

Analyse du nombre de canaux.

Objectif :

Vérifier la récupération des canaux.

Résultat attendu :

Le nombre de canaux est correct.

---

## TC-QL-06

Nom :

Construction du rapport qualité.

Objectif :

Vérifier le rapport final.

Résultat attendu :

Toutes les informations sont présentes.

---

## Tests de l'environnement

### TC-ENV-01 — Version Python

**Objectif :**

Vérifier que le projet utilise Python 3.12.

**Résultat attendu :**

Python 3.12.x est utilisé.

---

### TC-ENV-02 — Environnement virtuel

**Objectif :**

Vérifier que le Backend utilise l'environnement virtuel du projet.

**Résultat attendu :**

`backend/.venv` est correctement utilisé.

---

### TC-ENV-03 — Dépendances

**Objectif :**

Vérifier que les dépendances nécessaires sont disponibles.

**Résultat attendu :**

Les dépendances définies dans `requirements.txt` sont installées.

---

### TC-ENV-04 — FFmpeg

**Objectif :**

Vérifier la disponibilité de FFmpeg.

**Résultat attendu :**

FFmpeg peut être exécuté correctement.

---

### TC-ENV-05 — Faster-Whisper

**Objectif :**

Vérifier l'installation de Faster-Whisper.

**Résultat attendu :**

Le package peut être importé correctement.

---

### TC-ENV-06 — Ollama

**Objectif :**

Vérifier la disponibilité d'Ollama.

**Résultat attendu :**

Ollama est accessible localement.

---

### TC-ENV-07 — Backend

**Objectif :**

Vérifier le lancement du Backend avec Python 3.12.

**Résultat attendu :**

Le Backend démarre correctement et les endpoints principaux sont accessibles.

---

# Tests d'intégration

## TC-IT-01

Nom :

Pipeline complet Audio.

Objectif :

Vérifier le traitement complet d'un fichier audio.

Résultat attendu :

La transcription est générée avec succès.

---

## TC-IT-02

Nom :

Pipeline complet Vidéo.

Objectif :

Vérifier le traitement complet d'une vidéo.

Résultat attendu :

L'audio est extrait puis transcrit.

---

## TC-IT-03

Nom :

Pipeline complet avec résumé.

Objectif :

Vérifier la génération du résumé.

Résultat attendu :

Le résumé est généré après la transcription.

---

# Tests de performance

## TC-PF-01

Nom :

Petit fichier audio.

Objectif :

Mesurer le temps de traitement.

Résultat attendu :

Le traitement reste fluide.

---

## TC-PF-02

Nom :

Grand fichier audio.

Objectif :

Mesurer les performances.

Résultat attendu :

Le traitement se termine sans erreur.

---

## TC-PF-03

Nom :

Grande vidéo.

Objectif :

Mesurer les performances du pipeline complet.

Résultat attendu :

Le pipeline s'exécute correctement.
