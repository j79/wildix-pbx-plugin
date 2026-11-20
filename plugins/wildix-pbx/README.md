# wildix-pbx

Plugin Claude pour interroger et administrer **n'importe quel PBX Wildix** et les services cloud associés via leurs API REST.

## Ce qu'il fait

- Demande, pour chaque PBX, le domaine, la **Company API Key** (`wsk-v1-…`) et, au besoin, un **Bearer token** pour l'API WMS historique.
- Trouve la bonne route parmi ~940 (50 API, dont la plateforme Wilma) grâce à une référence embarquée consultée par morceaux.
- Exécute les lectures directement ; **toute écriture (POST/PUT/PATCH/DELETE) est présentée puis exécutée seulement après accord explicite**.
- Enregistre les grosses réponses dans des fichiers et en livre une synthèse (tableau, CSV, XLSX).

Exemples de demandes : « liste les utilisateurs du PBX client.wildixin.com », « sors l'historique d'appels de la semaine dernière », « récupère les résumés d'appel de l'extension 201 », « quelles routes permettent de gérer les call groups ? ».

## Sécurité

- Aucune clé n'est incluse dans le plugin. Chaque utilisateur saisit ses propres accès.
- Les accès sont conservés dans un fichier protégé (0600) du répertoire temporaire du système, jamais dans la mémoire de Claude ni dans les fichiers produits. `logout` les efface.

## Prérequis réseau

L'environnement Claude doit pouvoir joindre `*.wildixin.com`, `*.wildix.com`, `api.x-bees.com` et `broadcasts.x-hoppers.com`. Sur une offre Team ou Enterprise, c'est l'administrateur de l'organisation qui autorise ces domaines.

## Contenu

- `skills/wildix-pbx/SKILL.md` — méthode suivie par Claude.
- `skills/wildix-pbx/scripts/wildix.py` — client en ligne de commande (Python standard, sans dépendance).
- `skills/wildix-pbx/references/` — référence API Wildix (révision du 2026-11-20, 50 services), un fichier par API, plus un index des routes et les webhooks.

## Mettre à jour la référence (mainteneur)

Le dossier `maintainer/` contient l'outillage de mise à jour : `python3 maintainer/update.py --work <dossier>`.

- Il découvre les pages de référence REST de docs.wildix.com, télécharge leurs spécifications OpenAPI et compare leurs empreintes à `maintainer/spec-hashes.json`.
- Sans changement, il affiche `NO_CHANGE` et s'arrête.
- Si des routes ont seulement été retirées, ou si seuls des schémas ont changé, il affiche `MINOR_CHANGE` et ne produit aucune version : ces changements seront intégrés à la prochaine version comportant des ajouts.
- Si des routes ont été ajoutées (nouvelles routes, nouveaux services, routes de nouveau publiées), il régénère le référentiel en **conservant toutes les routes disparues** (marquées « deprecated (non publiée) » avec leur date de retrait), produit un rapport des écarts et construit une nouvelle version du plugin (`wildix-pbx-<version>.plugin`) dans le dossier de travail, à republier dans l'organisation.
- Le plugin installé n'est jamais modifié. Une tâche planifiée hebdomadaire peut lancer cette commande.

---

*English summary: Claude plugin to query and administer any Wildix PBX and Wildix cloud services through their REST APIs. Users supply their own Company API Key (and optionally a legacy PBX Bearer token) at run time; write operations always require explicit confirmation.*
