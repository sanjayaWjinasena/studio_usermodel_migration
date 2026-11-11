"""Inverse M2O for sales_report_type.journal_entry_id.
Moved from BugFix-Accounting/models/account_move.py so both sides
of the O2M relationship live in the same module. Prevents the cycle
that would otherwise form between this module and BugFix-Accounting.
"""

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    report_type_s_cust_aging = fields.Many2one(
        "sales_report_type",
        string="Report Type (S - Cust Aging)",
    )
