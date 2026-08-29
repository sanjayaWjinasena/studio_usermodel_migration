# -*- coding: utf-8 -*-
"""Inverse M2O for x_sales_report_type.x_studio_sales_lines_id.
Moved from BugFix-Sales/models/sale_order_line.py so both sides of
the O2M relationship live in the same module. Prevents the cycle
that would otherwise form between this module and BugFix-Sales.
"""
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_studio_sales_report_type = fields.Many2one(
        'x_sales_report_type',
        string='Sales Report Type',
    )
