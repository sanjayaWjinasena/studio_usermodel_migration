# -*- coding: utf-8 -*-
"""Studio field ports on base.automation (CDB Studio-manual fields).

These 2 fields were added on CDB via Studio directly on the core
`base.automation` model to annotate v15 migration status on individual
automation records. Purely metadata — no compute, no validation.
"""
from odoo import fields, models


class BaseAutomation(models.Model):
    _inherit = 'base.automation'

    x_studio_comments = fields.Char(string='Comments', copy=True)
    x_studio_status = fields.Selection(
        selection=[
            ('None', 'None'),
            ('Active in V15', 'Active in V15'),
            ('Archived in V15', 'Archived in V15'),
            ('Reactivated in V15', 'Reactivated in V15'),
        ],
        string='Status',
        copy=True,
    )
