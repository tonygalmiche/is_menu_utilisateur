/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

function normaliser(texte) {
    return (texte || "")
        .normalize("NFD")
        .replace(/[̀-ͯ]/g, "")
        .toLowerCase();
}

export class MesMenus extends Component {
    setup() {
        this.orm = useService("orm");
        this.menuService = useService("menu");
        this.state = useState({
            racines: [],
            ouverts: {},
            recherche: "",
        });
        onWillStart(() => this.charger());
    }

    async charger() {
        const lignes = await this.orm.call("ir.ui.menu", "is_get_mes_menus", []);
        const parId = {};
        for (const ligne of lignes) {
            parId[ligne.id] = { ...ligne, enfants: [] };
        }
        const racines = [];
        for (const ligne of lignes) {
            const noeud = parId[ligne.id];
            if (!ligne.parent_id) {
                racines.push(noeud);
            } else if (parId[ligne.parent_id]) {
                parId[ligne.parent_id].enfants.push(noeud);
            }
            // Parent non autorisé : menu absent de la barre de menus (comme dans Odoo), ignoré.
        }
        this.state.racines = racines;
    }

    /** Arborescence aplatie : lignes à afficher, selon le pliage et la recherche. */
    get lignes() {
        const recherche = normaliser(this.state.recherche.trim());
        const correspond = (noeud) =>
            !recherche ||
            normaliser(noeud.name).includes(recherche) ||
            noeud.enfants.some(correspond);
        const lignes = [];
        const parcourir = (noeuds, niveau, parentMasque) => {
            for (const noeud of noeuds) {
                if (!correspond(noeud)) {
                    continue;
                }
                const ouvert = Boolean(recherche) || Boolean(this.state.ouverts[noeud.id]);
                lignes.push({
                    noeud,
                    niveau,
                    ouvert,
                    grise: noeud.masque || parentMasque,
                });
                if (ouvert) {
                    parcourir(noeud.enfants, niveau + 1, noeud.masque || parentMasque);
                }
            }
        };
        parcourir(this.state.racines, 0, false);
        return lignes;
    }

    basculerPli(noeud) {
        if (!noeud.enfants.length) {
            return;
        }
        this.state.ouverts[noeud.id] = !this.state.ouverts[noeud.id];
    }

    toutPlier() {
        this.state.ouverts = {};
    }

    toutDeplier() {
        const ouverts = {};
        const parcourir = (noeuds) => {
            for (const noeud of noeuds) {
                if (noeud.enfants.length) {
                    ouverts[noeud.id] = true;
                    parcourir(noeud.enfants);
                }
            }
        };
        parcourir(this.state.racines);
        this.state.ouverts = ouverts;
    }

    async basculerMasque(noeud) {
        noeud.masque = !noeud.masque;
        await this.orm.call("ir.ui.menu", "is_set_menu_masque", [noeud.id, noeud.masque]);
        await this.menuService.reload();
    }
}

MesMenus.template = "is_menu_utilisateur.MesMenus";

registry.category("actions").add("is_menu_utilisateur.mes_menus", MesMenus);
