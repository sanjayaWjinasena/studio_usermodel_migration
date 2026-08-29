# -*- coding: utf-8 -*-
"""Inverse M2Os for x_sales_report_type One2manys targeting
account.move.line. Moved from BugFix-Accounting/models/account_move_line.py
so both sides of the O2M relationship live in the same module.
"""
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # Inverse of x_sales_report_type.x_studio_journal_items_id and
    # x_sales_report_type.x_studio_sales_lines_id (used from sale side too)
    x_studio_sales_report_type = fields.Many2one(
        'x_sales_report_type',
        string='Report Type (S- Incentive Calculation)',
    )

    # Inverse of x_sales_report_type.x_studio_test
    x_studio_many2one_field_kiSUJ = fields.Many2one(
        'x_sales_report_type',
        string='Sales Report Type',
    )
