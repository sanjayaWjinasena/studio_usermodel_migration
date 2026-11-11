"""Ports sales_report_model from BugFix-Accounting to the shared
Masterdata root. Companion to sales_report_type.

All 16 direct O2M targets (x_rm_*) still live in BugFix-Accounting.
That means: BugFix-Accounting depends on this module, this module
does NOT depend on BugFix-Accounting. The direct O2M inverse fields
declared on the x_rm_* target models (sales_report_model_id)
will be resolved at BugFix-Accounting load time, which is fine because
Odoo tolerates late-bound O2M inverses as long as they exist at
registry finalization.
"""

from odoo import fields, models


class XSalesReportModel(models.Model):
    _name = "sales_report_model"
    _rec_name = "name"  # Clear-DB Studio model: records are named by name
    _description = "X Sales Report Model"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    active = fields.Boolean(string="Active")
    name = fields.Char(string="Name")

    # --- Basic scalar fields ------------------------------------------
    actual_gp_ = fields.Float(string="Actual GP")
    actuals = fields.Boolean(string="Actuals")
    as_on_date = fields.Date(string="As on Date")
    as_on_date_1 = fields.Date(string="From Date")
    as_on_date_2 = fields.Date(string="To Date")
    auto_generated = fields.Boolean(string="Auto Generated")
    contingency_ = fields.Float(string="Contingency %")
    created_date = fields.Date(string="Created Date")
    date_updated = fields.Boolean(string="Date Updated")
    distributor_addition = fields.Float(string="Distributor Addition %")
    estimated_gp_ = fields.Float(string="Estimated GP")
    factory_oh = fields.Float(string="Factory OH")
    factory_oh_labour = fields.Float(string="Factory OH (Labour)")
    financial_progress = fields.Float(string="Financial Progress")
    from_date = fields.Date(string="From Date")
    idling_rate = fields.Float(string="Idling Rate %")
    management_purpose = fields.Boolean(string="Management Purpose")
    month_end_entry_updated = fields.Boolean(string="Month End Entry Updated")
    oh_absorbed_2_factory = fields.Float(string="OH Absorbed 2 (Factory)")
    oh_absorbed_2_other = fields.Float(string="OH Absorbed 2 (Other)")
    oh_absorbed_2_sales = fields.Float(string="OH Absorbed 2 (Sales)")
    oh_absorbed_factory = fields.Float(string="OH Absorbed (Factory)")
    oh_absorbed_other = fields.Float(string="OH Absorbed (Other)")
    oh_absorbed_sales = fields.Float(string="OH Absorbed (Sales)")
    other_oh = fields.Float(string="Other OH")
    profit_mark_up_ = fields.Float(string="Profit Mark Up %")
    report_code = fields.Selection(
        string="Report Code",
        related="report_type.report_code",
        store=True,
        readonly=True,
    )
    sales_oh = fields.Float(string="Sales OH")
    selection_field_Fbw0x = fields.Selection(
        [("Draft", "Draft"), ("Done", "Done")], string="Status"
    )
    sequence = fields.Integer(string="Sequence")
    sscl = fields.Float(string="SSCL %")

    # --- Many2one to standard modules already in this module's deps ---
    created_from_project_update = fields.Many2one(
        "project.update", string="Created From Project Update"
    )
    customer = fields.Many2many(
        "res.partner",
        "x_sales_report_model_x_studio_customer_rel",
        "host_id",
        "target_id",
        string="Customer",
    )
    project_no = fields.Many2one("project.project", string="Project No")
    report_type = fields.Many2one("sales_report_type", string="Report Type")
    sales_centre = fields.Many2many(
        "crm.team",
        "x_sales_report_model_x_studio_sales_centre_rel",
        "host_id",
        "target_id",
        string="Sales Centre",
    )

    # Direct O2Ms to x_rm_* models (16 total) NOT declared here.
    # Those x_rm_* target models live in BugFix-Accounting. Since
    # this module loads FIRST (masterdata root), their inverse M2O
    # fields (sales_report_model_id on each x_rm_*) aren't
    # registered yet at our load-time and O2M inverse validation
    # would fail. BugFix-Accounting adds all 16 via _inherit on
    # sales_report_model in its own model file - symmetric with
    # the stock/mrp deferral above.

    # Related O2Ms navigating through report_type. All 4
    # intermediate targets are declared in sales_report_type above
    # (their inverse M2Os also live in this module), so these related
    # paths are safe here at load time.
    journal_item_ids = fields.One2many(
        "account.move.line",
        related="report_type.journal_items_id",
        string="Journal Item Ids",
        readonly=True,
    )
    related_field_DqBBB = fields.One2many(
        "sale.order.line",
        related="report_type.sales_lines_id",
        string="New Related Field",
        readonly=True,
    )
    related_field_n589a = fields.One2many(
        "account.move.line",
        related="report_type.journal_items_id",
        string="New Related Field",
        readonly=True,
    )
    related_field_nfrkz = fields.One2many(
        "account.move",
        related="report_type.journal_entry_id",
        string="New Related Field",
        readonly=True,
    )
    # Stock/MRP related-navigation O2Ms (5) NOT declared. Their
    # related paths would go through report_type fields that
    # aren't declared upstream either (see sales_report_type.py).
    # Restoration comes from BugFix-Stock/MRP via _inherit on this
    # model in a follow-up (see INSTALL_JOURNEY.md item #1).
