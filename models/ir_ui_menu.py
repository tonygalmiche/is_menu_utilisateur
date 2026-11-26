# -*- coding: utf-8 -*-
import inspect

from odoo import _, api, fields, models  # type: ignore
from odoo.exceptions import AccessError  # type: ignore

GROUPE_REDACTION = 'is_menu_utilisateur.group_rediger_descriptions'


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    is_description = fields.Text(
        "Description", translate=True,
        help="Description personnalisée du menu (page « Mes menus »). Vide : "
             "description par défaut (docstring du modèle, sinon libellé du modèle).",
    )

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
    def _is_description_modele(self, model_name):
        """Description par défaut d'un modèle : docstring de la classe si elle
        vient d'un module InfoSaône (is_*), sinon libellé du modèle."""
        if not model_name or model_name not in self.env:
            return ''
        for cls in type(self.env[model_name]).mro():
            if cls.__doc__:
                if (getattr(cls, '_module', None) or '').startswith('is_'):
                    return inspect.cleandoc(cls.__doc__)
                break
        return self.env['ir.model'].sudo()._get(model_name).name or ''

    @api.model
    def is_get_mes_menus(self):
        """Menus autorisés à l'utilisateur (masqués compris), pour la page « Mes menus »."""
        menus = self.with_context(is_tous_les_menus=True).search([])
        masques = set(self.env.user.sudo().is_menu_masque_ids.ids)
        cache_modeles = {}
        lignes = []
        for menu in menus:
            action = menu.sudo().action
            model_name = action.res_model if action and action._name == 'ir.actions.act_window' else False
            if model_name not in cache_modeles:
                cache_modeles[model_name] = self._is_description_modele(model_name)
            lignes.append({
                'id': menu.id,
                'name': menu.name,
                'parent_id': menu.parent_id.id or False,
                'action_id': action.id if action else False,
                'masque': menu.id in masques,
                'description': menu.sudo().is_description or '',
                'description_defaut': cache_modeles[model_name],
            })
        return {
            'menus': lignes,
            'peut_rediger': self.env.user.has_group(GROUPE_REDACTION),
        }

    @api.model
    def is_set_menu_masque(self, menu_id, masque):
        """Masque ou réaffiche un menu pour l'utilisateur connecté."""
        commande = 4 if masque else 3
        self.env.user.sudo().write({'is_menu_masque_ids': [(commande, int(menu_id))]})
        self.clear_caches()
        return True

    @api.model
    def is_set_description(self, menu_id, description):
        """Enregistre la description personnalisée d'un menu (groupe de rédaction)."""
        if not self.env.user.has_group(GROUPE_REDACTION):
            raise AccessError(_("Réservé au groupe « Rédiger les descriptions des menus »."))
        self.sudo().browse(int(menu_id)).write({'is_description': (description or '').strip() or False})
        return True
