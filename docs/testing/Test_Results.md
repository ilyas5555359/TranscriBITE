# Test Results

## Présentation

Ce document regroupe les résultats des campagnes de tests réalisées tout au long du développement de **TranscriBITE**.

Il permettra de suivre l'évolution de la qualité du projet et de conserver une trace des différentes validations effectuées.

Les scénarios de test sont définis dans **Test_Cases.md**.

Le planning des campagnes de tests est décrit dans **Test_Plan.md**.

---

# Organisation des résultats

Les résultats seront renseignés au fur et à mesure des campagnes de tests prévues durant la Phase 8 du projet.

Chaque résultat indiquera :

- l'identifiant du test
- le nom du test
- la date d'exécution
- le résultat obtenu
- les observations éventuelles
- les actions correctives réalisées

---

# Légende

| Statut | Signification |
|---------|---------------|
| ✅ PASS | Test réussi |
| ❌ FAIL | Test échoué |
| ⚠️ WARNING | Fonctionnement partiel |
| ⏳ NOT EXECUTED | Test non encore réalisé |

---

# Jour 18 — Tests Backend

Date d'exécution : 2026-08-26

Environnement : Python 3.12.10 dans `.venv`, dépendances backend verrouillées installées avec succès.

Commande : `PYTHONPATH=backend .venv/Scripts/pytest.exe -q tests/backend`

Résultat initial : **56 tests réussis**.

Modules couverts :

- Audio / extraction FFmpeg : 5 tests réussis
- Upload et validation : 20 tests réussis, dont 10 combinaisons extension/MIME
- Process et pipelines audio/vidéo : 9 tests réussis
- Progression et états d'échec : 9 tests réussis
- Téléchargement TXT/JSON : 8 tests réussis
- Health : 7 tests réussis
- Qualité audio : 8 tests réussis

Correction vérifiée : les fichiers vides sont rejetés et une étape active passe à `FAILED` lorsqu'un traitement échoue.

---

# Jour 19 — Tests Frontend

Date d'exécution : 2026-08-26

Commandes : `npm test`, `npm run lint`, `npm run build`

Résultat :

- Vitest : **3 tests réussis**
- ESLint : **réussi**
- Build Vite : **réussi**
- `npm audit --audit-level=high` : **0 vulnérabilité**

Scénarios couverts : bouton désactivé sans fichier, workflow transcription/résumé réussi et affichage d'une erreur backend.

---

# Jour 20 — Tests d'intégration et performances

Validation manuelle exécutée le 2026-08-26 :

- `/health` : HTTP 200
- `/upload/` : HTTP 200
- `/process/start` : HTTP 200 avec Faster-Whisper `base` CPU/int8
- `/summary` : HTTP 200 avec Ollama `gemma2:2b`
- `/progress/{file_id}` : progression à 100 %
- `/download/{file_id}/txt` : HTTP 200
- `/download/{file_id}/json` : HTTP 200 et JSON valide

Les 10 formats configurés ont été exécutés avec des fixtures vocales générées localement : `.wav`, `.mp3`, `.m4a`, `.flac`, `.aac`, `.ogg`, `.mp4`, `.avi`, `.mov` et `.mkv`. Upload et traitement réel : **10/10 réussis**.

Les résultats de performance définitifs Whisper ne sont pas réexécutés conformément au plan.

Les tests suivants restent à compléter :

- des tests d'intégration
- des tests de performance
- des tests de validation finale

---

# Bilan intermédiaire

État au 2026-08-26 :

- 90 tests backend réussis et 5 tests frontend réussis
- 92 tests backend réussis et 5 tests frontend réussis
- aucun échec dans les campagnes automatisées exécutées
- pipeline réel audio → transcription → résumé → téléchargement validé
- vulnérabilité npm haute corrigée
- un test d'intégration HTTP automatisé est ajouté et réussi
- les 10 extensions déclarées sont couvertes par les tests de validation et de routage
- les dix formats ont été générés et vérifiés par FFmpeg/FFprobe
- benchmark réel CPU/int8 sur un court fichier vocal en français : tiny 8,79 s,
  base 9,44 s, small 15,14 s
- les traitements Whisper complets des dix codecs restent à exécuter séparément

Les tests HTTP utilisent `fastapi.testclient.TestClient`. La version actuelle
de Starlette signale une dépréciation liée à `httpx`; les tests passent et cet
avertissement est accepté jusqu'à l'harmonisation future des dépendances.
