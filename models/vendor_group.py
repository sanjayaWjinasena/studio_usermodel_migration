"""vendor_group — Studio custom catalogue model ported to Python.

Sister to customer_group but for vendors (payable-side classification).
Clear-DB has 20+ rows across three companies covering categories like
CA-PUR (Cash Purchase Vendors), CR-PUR (Credit Purchase Vendors),
IMP-VEN (Import Vendors), EMP-PAY (Employee-related payments), etc.

Field schema mirrors Clear-DB verbatim (RPC dump 2026-08-17).
"""

from odoo import fields, models


class XVendorGroup(models.Model):
    _name = "vendor_group"
    _description = "Vendor Group"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"
    _order = "sequence asc, id asc"

    active = fields.Boolean(default=True)
    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(default=10)
    description = fields.Char()
    accounting_company_id = fields.Many2one(
        "res.company",
        string="Company",
    )
    payable_account = fields.Many2one(
        "account.account",
    )
    payment_term = fields.Many2one(
        "account.payment.term",
    )
    one2many_field_5cEfV = fields.One2many(
        "res.partner",
        "vendor_group",
        string="Vendors",
    )
    # v0.0.5: Studio-auto smart-button counter of linked vendors.
    vendor_group__res_partner_count = fields.Integer(
        string="Res Partner Count",
        compute="_compute_res_partner_count",
        store=False,
    )

    def _compute_res_partner_count(self):
        Partner = self.env["res.partner"]
        for rec in self:
            rec.vendor_group__res_partner_count = Partner.search_count(
                [("vendor_group", "=", rec.id)]
            )


class XVendorGroupGap(models.Model):
    _inherit = "vendor_group"

    active = fields.Boolean()
    name = fields.Char(string="Code")
