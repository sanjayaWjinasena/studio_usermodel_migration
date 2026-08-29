# -*- coding: utf-8 -*-
"""Ports x_sales_report_model from BugFix-Accounting to the shared
Masterdata root. Companion to x_sales_report_type.

All 16 direct O2M targets (x_rm_*) still live in BugFix-Accounting.
That means: BugFix-Accounting depends on this module, this module
does NOT depend on BugFix-Accounting. The direct O2M inverse fields
declared on the x_rm_* target models (x_studio_sales_report_model_id)
will be resolved at BugFix-Accounting load time, which is fine because
Odoo tolerates late-bound O2M inverses as long as they exist at
registry finalization.
"""
from odoo import fields, models


class XSalesReportModel(models.Model):
    _name = 'x_sales_report_model'
    _description = 'X Sales Report Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    x_active = fields.Boolean(string='Active')
    x_name = fields.Char(string='Name')

    # --- Basic scalar fields ------------------------------------------
    x_studio_actual_gp_ = fields.Float(string='Actual GP')
    x_studio_actuals = fields.Boolean(string='Actuals')
    x_studio_as_on_date = fields.Date(string='As on Date')
    x_studio_as_on_date_1 = fields.Date(string='From Date')
    x_studio_as_on_date_2 = fields.Date(string='To Date')
    x_studio_auto_generated = fields.Boolean(string='Auto Generated')
    x_studio_contingency_ = fields.Float(string='Contingency %')
    x_studio_created_date = fields.Date(string='Created Date')
    x_studio_date_updated = fields.Boolean(string='Date Updated')
    x_studio_distributor_addition = fields.Float(string='Distributor Addition %')
    x_studio_estimated_gp_ = fields.Float(string='Estimated GP')
    x_studio_factory_oh = fields.Float(string='Factory OH')
    x_studio_factory_oh_labour = fields.Float(string='Factory OH (Labour)')
    x_studio_financial_progress = fields.Float(string='Financial Progress')
    x_studio_from_date = fields.Date(string='From Date')
    x_studio_idling_rate = fields.Float(string='Idling Rate %')
    x_studio_management_purpose = fields.Boolean(string='Management Purpose')
    x_studio_month_end_entry_updated = fields.Boolean(string='Month End Entry Updated')
    x_studio_oh_absorbed_2_factory = fields.Float(string='OH Absorbed 2 (Factory)')
    x_studio_oh_absorbed_2_other = fields.Float(string='OH Absorbed 2 (Other)')
    x_studio_oh_absorbed_2_sales = fields.Float(string='OH Absorbed 2 (Sales)')
    x_studio_oh_absorbed_factory = fields.Float(string='OH Absorbed (Factory)')
    x_studio_oh_absorbed_other = fields.Float(string='OH Absorbed (Other)')
    x_studio_oh_absorbed_sales = fields.Float(string='OH Absorbed (Sales)')
    x_studio_other_oh = fields.Float(string='Other OH')
    x_studio_profit_mark_up_ = fields.Float(string='Profit Mark Up %')
    x_studio_report_code = fields.Selection([], string='Report Code')
    x_studio_sales_oh = fields.Float(string='Sales OH')
    x_studio_selection_field_Fbw0x = fields.Selection([], string='Status')
    x_studio_sequence = fields.Integer(string='Sequence')
    x_studio_sscl = fields.Float(string='SSCL %')

    # --- Many2one to standard modules already in this module's deps ---
    x_studio_created_from_project_update = fields.Many2one('project.update', string='Created From Project Update')
    x_studio_customer = fields.Many2many('res.partner', 'x_sales_report_model_x_studio_customer_rel', 'host_id', 'target_id', string='Customer')
    x_studio_project_no = fields.Many2one('project.project', string='Project No')
    x_studio_report_type = fields.Many2one('x_sales_report_type', string='Report Type')
    x_studio_sales_centre = fields.Many2many('crm.team', 'x_sales_report_model_x_studio_sales_centre_rel', 'host_id', 'target_id', string='Sales Centre')

    # Direct O2Ms to x_rm_* models (16 total) NOT declared here.
    # Those x_rm_* target models live in BugFix-Accounting. Since
    # this module loads FIRST (masterdata root), their inverse M2O
    # fields (x_studio_sales_report_model_id on each x_rm_*) aren't
    # registered yet at our load-time and O2M inverse validation
    # would fail. BugFix-Accounting adds all 16 via _inherit on
    # x_sales_report_model in its own model file - symmetric with
    # the stock/mrp deferral above.

    # Related O2Ms navigating through x_studio_report_type. All 4
    # intermediate targets are declared in x_sales_report_type above
    # (their inverse M2Os also live in this module), so these related
    # paths are safe here at load time.
    x_studio_journal_item_ids = fields.One2many(
        'account.move.line',
        related='x_studio_report_type.x_studio_journal_items_id',
        string='Journal Item Ids',
        readonly=True,
    )
    x_studio_related_field_DqBBB = fields.One2many(
        'sale.order.line',
        related='x_studio_report_type.x_studio_sales_lines_id',
        string='New Related Field',
        readonly=True,
    )
    x_studio_related_field_n589a = fields.One2many(
        'account.move.line',
        related='x_studio_report_type.x_studio_journal_items_id',
        string='New Related Field',
        readonly=True,
    )
    x_studio_related_field_nfrkz = fields.One2many(
        'account.move',
        related='x_studio_report_type.x_studio_journal_entry_id',
        string='New Related Field',
        readonly=True,
    )
    # Stock/MRP related-navigation O2Ms (5) NOT declared. Their
    # related paths would go through x_studio_report_type fields that
    # aren't declared upstream either (see x_sales_report_type.py).
    # Restoration comes from BugFix-Stock/MRP via _inherit on this
    # model in a follow-up (see INSTALL_JOURNEY.md item #1).
