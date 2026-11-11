"""Ports sales_report_type from BugFix-Accounting to the shared
Masterdata root. Owning it here breaks the cycle that prevented
BugFix-Stock/BugFix-MRP from being depped by BugFix-Accounting.

Whole chain, when this module lands:
  * sale.order.line, account.move, account.move.line inverse M2Os
    also live here (see corresponding files in this dir).
  * BugFix-Stock/MRP can safely declare `Many2one('sales_report_type')`
    now that the target model loads before them.
  * BugFix-Accounting's stripped v0.0.31/v0.0.32 tabs can be
    restored in a follow-up commit once Stock/MRP add the O2Ms here.
"""

from odoo import fields, models


class XSalesReportType(models.Model):
    _name = "sales_report_type"
    _rec_name = "name"  # Clear-DB Studio model: records are named by name
    _description = "X Sales Report Type"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    active = fields.Boolean(string="Active")
    name = fields.Char(string="Report Name")
    report_code = fields.Selection(
        [
            ("Daily Sales Summary", "Daily Sales Summary"),
            ("Sales Details for Incentive Calc.", "Sales Details for Incentive Calc."),
            ("Production Overview - WIP", "Production Overview - WIP"),
            ("Customer Aging Report", "Customer Aging Report"),
            ("Slow Moving Items", "Slow Moving Items"),
            (
                "Sales - Production - Purchase Report",
                "Sales - Production - Purchase Report",
            ),
            ("Production Summary - Split", "Production Summary - Split"),
            ("Production Job Variance", "Production Job Variance"),
            ("Casting Melt", "Casting Melt"),
            ("Import Transaction", "Import Transaction"),
            ("Project Gross Margin", "Project Gross Margin"),
            ("Costing Work Sheet", "Costing Work Sheet"),
        ],
        string="Report Code",
    )
    sequence = fields.Integer(string="Sequence")

    # One2manys navigating through inverse M2Os that also live in this
    # module (see account_move.py, account_move_line.py, sale_order_line.py).
    journal_entry_id = fields.One2many(
        "account.move",
        "report_type_s_cust_aging",
        string="Journal Entry Id",
    )
    journal_items_id = fields.One2many(
        "account.move.line",
        "sales_report_type",
        string="Journal Items Id",
    )
    sales_lines_id = fields.One2many(
        "sale.order.line",
        "sales_report_type",
        string="Sales Lines Id",
    )
    test = fields.One2many(
        "account.move.line",
        "many2one_field_kiSUJ",
        string="test",
    )

    # Stock/MRP-side O2Ms (5) intentionally NOT declared here.
    # Their inverse M2Os live in BugFix-Stock and BugFix-MRP and would
    # only resolve when those modules are loaded. Declaring here would
    # force this Masterdata root to depend on stock + mrp modules just
    # to route Studio reports, which pollutes the module's semantics.
    #
    # Restoration path: BugFix-Stock and BugFix-MRP add the reverse
    # O2Ms via _inherit on sales_report_type when they land, using
    # their own inverse M2Os as the field pointer. See
    # BugFix-Accounting/INSTALL_JOURNEY.md follow-up item #1.
    #
    # Missing fields (for reference):
    #   prod_summary_split_id  (stock.move.line)
    #   production_order_id    (mrp.production)
    #   production_variance_id (stock.move)
    #   sales_prod_purch_id    (stock.move.line)
    #   slow_moving_item_id    (stock.move.line)
