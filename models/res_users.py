# -*- coding: utf-8 -*-
from odoo import fields, models  # type: ignore


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_menu_masque_ids = fields.Many2many(
        'ir.ui.menu', 'is_menu_masque_res_users_rel', 'user_id', 'menu_id',
        string="Menus masqués",
        help="Menus que l'utilisateur a choisi de ne plus afficher (page « Mes menus »)",
    )
