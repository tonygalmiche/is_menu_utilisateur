# -*- coding: utf-8 -*-
from odoo import api, models  # type: ignore


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def _visible_menu_ids(self, debug=False):
        """Retire des menus visibles ceux que l'utilisateur a masqués
        (et leurs sous-menus). Le résultat d'Odoo reste en cache par
        groupes ; le filtre par utilisateur est appliqué après."""
        visible_ids = super()._visible_menu_ids(debug)
        if self.env.context.get('is_tous_les_menus'):
            return visible_ids
        masques = set(self.env.user.sudo().is_menu_masque_ids.ids)
        if not masques:
            return visible_ids
        result = set()
        menus = self.sudo().with_context(**{'ir.ui.menu.full_list': True}).browse(list(visible_ids))
        for menu in menus:
            chemin = {int(x) for x in (menu.parent_path or '').split('/') if x}
            if not chemin & masques:
                result.add(menu.id)
        return result

    @api.model
    def is_get_mes_menus(self):
        """Menus autorisés à l'utilisateur (masqués compris), pour la page « Mes menus »."""
        menus = self.with_context(is_tous_les_menus=True).search([])
        masques = set(self.env.user.sudo().is_menu_masque_ids.ids)
        return [{
            'id': menu.id,
            'name': menu.name,
            'parent_id': menu.parent_id.id or False,
            'masque': menu.id in masques,
        } for menu in menus]

    @api.model
    def is_set_menu_masque(self, menu_id, masque):
        """Masque ou réaffiche un menu pour l'utilisateur connecté."""
        commande = 4 if masque else 3
        self.env.user.sudo().write({'is_menu_masque_ids': [(commande, int(menu_id))]})
        self.clear_caches()
        return True
