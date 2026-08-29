# -*- coding: utf-8 -*-
"""Ports x_sales_report_type from BugFix-Accounting to the shared
Masterdata root. Owning it here breaks the cycle that prevented
BugFix-Stock/BugFix-MRP from being depped by BugFix-Accounting.

Whole chain, when this module lands:
  * sale.order.line, account.move, account.move.line inverse M2Os
    also live here (see corresponding files in this dir).
  * BugFix-Stock/MRP can safely declare `Many2one('x_sales_report_type')`
    now that the target model loads before them.
  * BugFix-Accounting's stripped v0.0.31/v0.0.32 tabs can be
    restored in a follow-up commit once Stock/MRP add the O2Ms here.
"""
from odoo import fields, models


class XSalesReportType(models.Model):
    _name = 'x_sales_report_type'
    _description = 'X Sales Report Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    x_active = fields.Boolean(string='Active')
    x_name = fields.Char(string='Report Name')
    x_studio_report_code = fields.Selection([], string='Report Code')
    x_studio_sequence = fields.Integer(string='Sequence')

    # One2manys navigating through inverse M2Os that also live in this
    # module (see account_move.py, account_move_line.py, sale_order_line.py).
    x_studio_journal_entry_id = fields.One2many(
        'account.move',
        'x_studio_report_type_s_cust_aging',
        string='Journal Entry Id',
    )
    x_studio_journal_items_id = fields.One2many(
        'account.move.line',
        'x_studio_sales_report_type',
        string='Journal Items Id',
    )
    x_studio_sales_lines_id = fields.One2many(
        'sale.order.line',
        'x_studio_sales_report_type',
        string='Sales Lines Id',
    )
    x_studio_test = fields.One2many(
        'account.move.line',
        'x_studio_many2one_field_kiSUJ',
        string='test',
    )

    # Stock/MRP-side O2Ms (5) intentionally NOT declared here.
    # Their inverse M2Os live in BugFix-Stock and BugFix-MRP and would
    # only resolve when those modules are loaded. Declaring here would
    # force this Masterdata root to depend on stock + mrp modules just
    # to route Studio reports, which pollutes the module's semantics.
    #
    # Restoration path: BugFix-Stock and BugFix-MRP add the reverse
    # O2Ms via _inherit on x_sales_report_type when they land, using
    # their own inverse M2Os as the field pointer. See
    # BugFix-Accounting/INSTALL_JOURNEY.md follow-up item #1.
    #
    # Missing fields (for reference):
    #   x_studio_prod_summary_split_id  (stock.move.line)
    #   x_studio_production_order_id    (mrp.production)
    #   x_studio_production_variance_id (stock.move)
    #   x_studio_sales_prod_purch_id    (stock.move.line)
    #   x_studio_slow_moving_item_id    (stock.move.line)
