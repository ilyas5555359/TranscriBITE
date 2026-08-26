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

* Faster-Whisper : 1.1.1

* Compute type : `int8`



---



## Résultats



| Modèle | Temps chargement | Temps transcription | RAM avant | RAM après | Langue | Segments | Résultat |

| ------ | ---------------: | ------------------: | --------: | --------: | ------ | -------: | -------- |

| tiny   | 1.50 s | 8.16 s | 17.80 MB | 139.14 MB | fr | 12 | Succès |

| base   | 0.87 s | 11.98 s | 98.35 MB | 191.15 MB | fr | 14 | Succès |

| small  | 2.00 s | 34.61 s | 106.05 MB | 366.35 MB | fr | 18 | Succès |



---



## Analyse



### Modèle tiny



Le modèle `tiny` est le plus rapide et présente la plus faible consommation mémoire.



Cependant, il offre une capacité de transcription inférieure aux modèles plus grands.



Il est intéressant lorsque la rapidité et la faible consommation de ressources sont prioritaires.



### Modèle base



Le modèle `base` présente un temps de transcription raisonnable tout en consommant beaucoup moins de mémoire que `small`.



La détection de la langue française fonctionne correctement.



Il constitue donc un bon compromis entre performance et qualité.



### Modèle small



Le modèle `small` fournit une transcription plus détaillée mais son temps d'exécution est nettement supérieur.



Sa consommation mémoire est également beaucoup plus importante.



Sur une machine CPU-only disposant de 16 GB de RAM, cette différence doit être prise en compte.



---



## Décision technique



Le modèle retenu pour TranscriBITE est :



```text

WHISPER\_MODEL=base

device=cpu
compute_type=int8
Cette configuration permet d'exécuter la transcription localement sans GPU dédié.

---

## Justification du choix

Le modèle `base` a été retenu pour les raisons suivantes :

1. temps de transcription acceptable
2. consommation mémoire raisonnable
3. détection correcte de la langue
4. fonctionnement stable sur CPU
5. bon compromis entre rapidité et qualité
6. compatibilité avec les contraintes matérielles du projet

---

## Conclusion

Les trois modèles testés fonctionnent correctement sur l'environnement CPU.

Le modèle `tiny` est le plus rapide.

Le modèle `small` consomme davantage de ressources et augmente fortement le temps de transcription.

Le modèle `base` constitue le compromis retenu pour la version actuelle de TranscriBITE.

La configuration officielle utilisée par le backend est donc :

```text
WHISPER_MODEL=base
device=cpu
compute_type=int8
```
