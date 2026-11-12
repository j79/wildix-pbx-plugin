# wildix-tools — catalogue de plugins Claude

Dépôt privé contenant le plugin **wildix-pbx** : interroger et administrer n'importe quel PBX Wildix et les services cloud Wildix via leurs API REST, avec une référence API embarquée (mise à jour à partir de docs.wildix.com).

## Installation

1. Acceptez l'invitation GitHub reçue par e-mail (accès en lecture à ce dépôt privé).
2. Reliez votre compte GitHub à Claude (Customize › Connectors › GitHub).
3. Dans Claude, ajoutez ce dépôt comme source de plugins : `j79/wildix-pbx-plugin`.
4. Installez le plugin **wildix-pbx**.

Dans Claude Code : `/plugin marketplace add j79/wildix-pbx-plugin`, puis `/plugin install wildix-pbx@wildix-tools`.

Les nouvelles versions publiées ici vous parviennent ensuite automatiquement.

## Mises à jour

Une tâche planifiée vérifie chaque vendredi la documentation des API Wildix. Une nouvelle version n'est proposée que si des routes ont été **ajoutées** ; les routes retirées de la documentation sont conservées et marquées *deprecated*. Chaque proposition arrive sous forme de demande de fusion (pull request), avec son rapport des écarts dans `reports/`, et n'est publiée qu'après validation par le propriétaire.

Détails du plugin : [plugins/wildix-pbx/README.md](plugins/wildix-pbx/README.md).
