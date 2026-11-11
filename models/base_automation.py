"""base.automation Studio fields, declared in code.

Until now Comments / Status were 'manual' fields created from data/ir_model_data.xml, which keeps them
on Studio names (Odoo only allows x_ names for manual fields). Declared here they are ordinary module
fields: the Studio rename migration renames them like every other field and Odoo sets them to 'base'.
Same columns, type and choices as before.
"""

from odoo import fields, models


class BaseAutomation(models.Model):
    _inherit = "base.automation"

    comments = fields.Char(string="Comments", copy=True)
    status = fields.Selection(
        [
            ("None", "None"),
            ("Active in V15", "Active in V15"),
            ("Archived in V15", "Archived in V15"),
            ("Reactivated in V15", "Reactivated in V15"),
        ],
        string="Status",
        copy=True,
    )
