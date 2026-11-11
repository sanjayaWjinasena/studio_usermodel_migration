"""res.partner Studio field port — customer / vendor group cluster.

Three fields on res.partner that reference the sibling catalogue
models (customer_group, vendor_group) in this module.

Ported v0.0.3. On Clear-DB these are state='manual' owned by
studio_customization; module upgrade flips state to 'base' and
Python owns them.
"""

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_group = fields.Many2one(
        "customer_group",
        string="Customer Group",
    )
    vendor_group = fields.Many2one(
        "vendor_group",
        string="Vendor Group",
    )
    # Selection stored per-partner. On Clear-DB this stays in sync with
    # customer_group.group_type via a Studio
    # automation; port that automation as a compute or on_change in a
    # future chunk if the read is heavy — for now it's a plain
    # selection matching the parent group's set.
    group_type = fields.Selection(
        selection=[
            ("General", "General"),
            ("Distributor", "Distributor"),
            ("Dealer", "Dealer"),
        ],
        string="Group Type",
    )
