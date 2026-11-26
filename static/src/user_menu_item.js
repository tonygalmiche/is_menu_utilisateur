/** @odoo-module **/

import { registry } from "@web/core/registry";

function mesMenusItem(env) {
    return {
        type: "item",
        id: "is_mes_menus",
        description: env._t("Mes menus"),
        callback: () => {
            env.services.action.doAction(
                {
                    type: "ir.actions.client",
                    tag: "is_menu_utilisateur.mes_menus",
                    name: env._t("Mes menus"),
                    target: "current",
                },
                { clearBreadcrumbs: true }
            );
        },
        sequence: 55,
    };
}

registry.category("user_menuitems").add("is_mes_menus", mesMenusItem);
