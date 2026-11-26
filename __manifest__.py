# -*- coding: utf-8 -*-

{
    "name": "InfoSaône - Menus par utilisateur",
    "version": "16.0.1.0.0",
    "author": "InfoSaône / Tony Galmiche",
    "category": "InfoSaône",
    "description": """
InfoSaône - Menus par utilisateur

- Page « Mes menus » (menu de l'avatar, en haut à droite) : arborescence des
  menus autorisés à l'utilisateur, une case à cocher par menu.
- Menu décoché : masqué dans la barre de menus pour cet utilisateur seulement
  (sous-menus compris). Simple confort d'affichage, pas de sécurité.
""",
    "maintainer": "InfoSaône",
    "website": "http://www.infosaone.com",
    "depends": [
        "base",
        "web",
    ],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "is_menu_utilisateur/static/src/user_menu_item.js",
            "is_menu_utilisateur/static/src/mes_menus/mes_menus.js",
            "is_menu_utilisateur/static/src/mes_menus/mes_menus.xml",
            "is_menu_utilisateur/static/src/mes_menus/mes_menus.scss",
        ],
    },
    "installable": True,
    "application": False,
    "license": "AGPL-3",
}
