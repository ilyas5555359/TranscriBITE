# Test Plan

## Présentation

Ce document décrit la stratégie de test du projet **TranscriBITE**.

Son objectif est de définir les différents types de tests qui seront réalisés afin de vérifier le bon fonctionnement de l'application avant sa livraison finale.

Les tests couvriront l'ensemble des composants développés durant le projet :

- Backend
- Frontend
- Intégration
- Performances
- Gestion des erreurs
- Validation des résultats

Les résultats des exécutions seront documentés dans **Test_Results.md**, tandis que les scénarios détaillés seront décrits dans **Test_Cases.md**.

---

# Objectifs

Les tests devront permettre de vérifier :

- le bon fonctionnement de chaque module
- la communication entre les modules
- la stabilité de l'application
- la fiabilité du pipeline complet
- la gestion des erreurs
- les performances générales

---

# Types de tests

## Tests unitaires

Les tests unitaires vérifieront individuellement chaque module Backend et Frontend.

Modules Backend concernés :

- Upload
- Process
- Progress
- Download
- Health
- Quality

Modules Frontend concernés :

- Home
- Upload
- Progress
- Download
- Affichage des résultats

---

## Tests d'intégration

Les tests d'intégration permettront de vérifier la communication entre :

- Frontend ↔ Backend
- Backend ↔ Faster-Whisper
- Backend ↔ FFmpeg
- Backend ↔ Ollama

Ils permettront également de valider le fonctionnement complet du pipeline.

---

## Tests fonctionnels

Les tests fonctionnels consisteront à vérifier que les fonctionnalités répondent aux besoins définis dans le cahier des charges.

Ils porteront notamment sur :

- import des fichiers
- traitement audio
- traitement vidéo
- transcription
- génération du résumé
- téléchargement des résultats

---

## Tests de validation

Ces tests permettront de vérifier :

- les extensions autorisées
- les types MIME
- la taille maximale des fichiers
- les paramètres utilisateur
- les erreurs de validation

---

## Tests de performance

Les performances seront évaluées sur plusieurs critères :

- temps d'import
- temps d'extraction audio
- temps de transcription
- temps de génération du résumé
- temps total du pipeline

---

## Tests de robustesse

Ces tests auront pour objectif de vérifier le comportement de l'application face à différentes situations exceptionnelles.

Exemples :

- fichier inexistant
- fichier vide
- fichier corrompu
- format non supporté
- erreur FFmpeg
- erreur Faster-Whisper
- erreur Ollama
- manque de ressources système

---

# Organisation des tests

Les tests seront réalisés selon les phases suivantes :

## Phase 1

Tests unitaires Backend.

## Phase 2

Tests unitaires Frontend.

## Phase 3

Tests d'intégration.

## Phase 4

Tests de performance.

## Phase 5

Validation finale de l'application.

---

# Outils

Les principaux outils utilisés seront :

Backend :

- Pytest

Frontend :

- React Testing Library
- Vitest (si retenu)

Tests API :

- Swagger UI
- FastAPI TestClient

---

# Critères de validation

Le projet sera considéré comme validé lorsque :

- tous les tests critiques seront réussis
- aucun blocage majeur ne subsistera
- le pipeline complet fonctionnera correctement
- les erreurs seront correctement gérées
- les performances seront jugées satisfaisantes

---

# Planning

Les tests seront réalisés durant la Phase 8 du projet.

Jour 18 :

- Tests Backend

Jour 19 :

- Tests Frontend

Jour 20 :

- Tests d'intégration
- Tests de performance
- Validation finale
