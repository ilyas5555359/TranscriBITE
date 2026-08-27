# Scripts

Ce dossier contient les scripts utilitaires utilisés pour la maintenance et la préparation de TranscriBITE.

Depuis la racine du projet :

```powershell
python scripts/create_folders.py
python scripts/check_environment.py
python scripts/install_models.py --model gemma2:2b
python scripts/benchmark_whisper.py storage/samples/sample.wav --model base --language fr
python scripts/clean_temp.py
```

`check_environment.py` retourne un code différent de zéro lorsqu'une dépendance
ou un outil système est absent. L'installation des modèles Whisper et Ollama
reste volontairement manuelle afin d'éviter un téléchargement implicite.