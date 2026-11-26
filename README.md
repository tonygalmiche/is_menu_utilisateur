# is_menu_utilisateur

Chaque utilisateur masque les menus qui ne l'intéressent pas, pour alléger son interface. Étude : `Documentation/modules-generiques/is_menu_utilisateur.md`.

- Accès : menu de l'avatar (en haut à droite) → **Mes menus**.
- Page : arborescence des menus autorisés à l'utilisateur, une case par menu (cochée par défaut), pliage / dépliage, recherche.
- Menu décoché : masqué dans la barre de menus pour cet utilisateur (sous-menus compris) ; enregistré tout de suite, barre rechargée.
- Pas de sécurité : droits d'accès inchangés.

## Technique

- `res.users.is_menu_masque_ids` : menus masqués.
- `ir.ui.menu._visible_menu_ids` : résultat d'Odoo (en cache par groupes) filtré par utilisateur ; contexte `is_tous_les_menus` pour la page.
- Client action `is_menu_utilisateur.mes_menus`, entrée `user_menuitems`.

## À venir

- Descriptions des menus (✎, info-bulle), statistiques (nombre, dernière modification).
