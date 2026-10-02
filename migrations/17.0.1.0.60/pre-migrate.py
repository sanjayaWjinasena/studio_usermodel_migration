# -*- coding: utf-8 -*-
"""v1.0.60: hand the sticky-`_unknown` Many2one(s) below over to BugFix-Studio-Misc v0.0.112.

Part of the 2026-10-02 ownership move: a Python Many2one whose comodel is owned
by a module that loads LATER is rewritten to comodel '_unknown' by Odoo 17 at
this module's setup pass and never recovers for the rest of an upgrade-mode
registry build (Jinasena_All cascade crashed on a MasterData CSV with
`relation "_unknown" does not exist`). The only load-order-proof fix is a
single declaration in the comodel-owning module, so the field declarations
left this module and now live in BugFix-Studio-Misc v0.0.112.

This pre-migrate does two ORM-only things (no cr.execute):

1. Detaches this module's ir.model.data pointers for the moved fields.
   Otherwise ir.model.data._process_end would see xmlids that were not
   re-loaded and, if no other xmlid pointed at the same ir.model.fields row,
   UNLINK the field and DROP its column (live data). With the pointer gone
   the field row is never a cleanup candidate; BugFix-Studio-Misc v0.0.112 re-attaches its own
   xmlids on reflection.

2. Unlinks the extension views of this module whose arch referenced the moved
   fields. Odoo rewrites a parent view first and validates the combined arch
   with the children AS STORED IN THE DB (old arch, field still referenced)
   -> "Field X does not exist in model Y". A dangling xmlid makes
   _load_records recreate the view from the new file arch (same xmlid, new
   id). None of these views has inheriting children (RPC-verified).

Idempotent: no-op on fresh installs (version is None) and when rows are gone.
"""
import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

MODULE = 'studio_usermodel_migration'
MOVED_FIELDS = (
    ('res.users', 'x_studio_customer_group2'),
    ('res.users', 'x_studio_many2one_field_3LBKs'),
    ('res.users', 'x_studio_many2one_field_9xxxo'),
    ('res.users', 'x_studio_many2one_field_V9cmo'),
)
STALE_VIEWS = (
    # (none)
)


def migrate(cr, version):
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    Fields = env['ir.model.fields'].sudo()
    IMD = env['ir.model.data'].sudo()

    field_ids = []
    for model, name in MOVED_FIELDS:
        field_ids += Fields.search([('model', '=', model), ('name', '=', name)]).ids
    if field_ids:
        imd = IMD.search([
            ('module', '=', MODULE),
            ('model', '=', 'ir.model.fields'),
            ('res_id', 'in', field_ids),
        ])
        if imd:
            names = imd.mapped('name')
            imd.unlink()
            _logger.info("%s v1.0.60: detached %d ir.model.data pointer(s) for moved "
                         "fields: %s", MODULE, len(names), names)

    View = env['ir.ui.view'].sudo().with_context(active_test=False)
    for xmlid in STALE_VIEWS:
        view = env.ref(xmlid, raise_if_not_found=False)
        if not view:
            continue
        view = View.browse(view.id)
        _logger.info("%s v1.0.60: unlinking stale extension view %s (id=%s, model=%s) "
                     "for recreation from the new file arch", MODULE, xmlid, view.id, view.model)
        view.unlink()
