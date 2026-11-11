"""res.users Studio field port.

Ports the 4 Studio-manual x_studio_* fields on res.users that
Fix-repair's helpdesk_ticket views + the res.users form arch (id 2392
on Clear-DB, owned by Fix-repair) reference. Declared here rather
than in Fix-repair because they're user-master metadata (company,
recruitment stages, stock-location counters) — distinct from the
repair-flow location fields that legitimately live in Fix-repair
(source_location, virtual_location, etc.).

Fields:
  - accounting_company_id           (m2o res.company) — per-user
      "Current Company" flag used by view-arch invisible expressions
      to swap between _1 fields across companies
  - recr_stages          (m2m hr.recruitment.stage) —
      Recruitment tab
  - users_stock_location_stock_location_count (int) —
      companion counter for the stock.location m2m on stock.location
  - users_internal_transfer_stock_location_count (int) —
      companion counter for the second stock.location m2m
"""

from odoo import _, api, fields, models
from odoo.exceptions import UserError

# NOTE (v1.0.60): the Many2one(s) customer_group2 /
# many2one_field_3LBKs /
# many2one_field_9xxxo / many2one_field_V9cmo (-> customer_groups)
# were MOVED to BugFix-Studio-Misc v0.0.112 models/res_users.py.
# Their comodel is owned by a DOWNSTREAM module; declared here they were
# `_unknown` for the whole upgrade-mode registry build (see BugFix-Purchase
# models/upstream_link_fields.py). Do NOT re-add them here.


class ResUsers(models.Model):
    _inherit = "res.users"

    accounting_company_id = fields.Many2one(
        "res.company",
        string="Current Company",
    )
    recr_stages = fields.Many2many(
        "hr.recruitment.stage",
        relation="res_users_studio_recr_stages_rel",
        column1="user_id",
        column2="stage_id",
        string="Recruitment Stages",
    )
    # Studio-generated companion counter fields — mirrored so the
    # Studio-arch stat buttons don't break the view load. Not
    # currently populated by Python compute since the corresponding
    # stat buttons (actions 2487/2488) are DB-specific and skipped
    # in the ported view arch. Left here as sentinels for arch
    # compatibility in case a future view inherit references them.
    users_stock_location_stock_location_count = fields.Integer(
        string="Users (Stock Location) count",
    )
    users_internal_transfer_stock_location_count = fields.Integer(
        string="Users (Internal Transfer) count",
    )
    # v0.0.2: the two res.users-side halves of the Studio m2m to
    # stock.location. Fix-repair declares the reverse side (on
    # stock.location) in models/stock_location.py:54-67 using specific
    # relation-table names — Q50dg / bQRSA use those SAME names so
    # both sides read/write the same relation rows. This lets Studio
    # arch that references the fields from either direction resolve
    # to a single set of user↔location links.
    many2many_field_Q50dg = fields.Many2many(
        "stock.location",
        relation="stock_location_users_stock_location_rel",
        column1="user_id",
        column2="location_id",
        string="Inventory Locations (Stock)",
    )
    many2many_field_bQRSA = fields.Many2many(
        "stock.location",
        relation="stock_location_users_internal_transfer_rel",
        column1="user_id",
        column2="location_id",
        string="Inventory Locations (Internal Transfer)",
    )

    # v0.0.7: repair-flow location fields moved here from Fix-repair.
    # The res.users form view in this module's views/res_users_views.xml
    # references virtual_location, which broke registry setup
    # when studio_usermodel_migration loaded before Fix-repair.
    # These four fields are pure res.users Studio schema -- they
    # belong in this res.users-scoped module. Fix-repair's
    # helpdesk.ticket related fields still resolve because
    # studio_usermodel_migration now loads first in the graph.
    source_location = fields.Many2one(
        "stock.location",
    )
    source_location_1 = fields.Many2one(
        "stock.location",
        string="Source Location",
    )
    virtual_location = fields.Many2one(
        "stock.location",
    )
    virtual_location_1 = fields.Many2one(
        "stock.location",
        string="Virtual Location",
    )

    # v0.0.11: sentinels for Studio-manual fields that Wave 5A view-port
    # surfaces from Clear-DB. Not populated on dev; declared as inert
    # placeholders so the ported view arch validates. Fix-repair
    # ports the actual super_user booleans (see repair_admin_groups.py).
    super_user = fields.Boolean(
        string="Super User (All Items)",
        copy=True,
    )
    super_user_melt_items = fields.Boolean(
        string="Super User (Melt Items)",
        copy=True,
    )
    attendance_administrator = fields.Boolean()

    # v0.0.7: super-user permission booleans (moved from
    # Fix-repair/models/res_users.py, declared above). Native port of Studio
    # server action id 2544 which enforced mutual exclusion.

    def _super_user_validate(self):
        """Studio server action id 2544 native port. Guards that a
        single user cannot hold BOTH super-user permissions."""
        for record in self:
            if record.super_user_melt_items and record.super_user:
                raise UserError(
                    _(
                        "Both the super user permissions can not be "
                        "assigned to a single user."
                    )
                )

    @api.model_create_multi
    def create(self, vals_list):
        """Replaces automation 250 'Super User Validate' -- create branch."""
        records = super().create(vals_list)
        records._super_user_validate()
        return records

    def write(self, vals):
        """Replaces automation 250 'Super User Validate' -- write branch."""
        result = super().write(vals)
        self._super_user_validate()
        return result

    # v0.0.46: 47 res.users x_studio_ fields.
    # SQL columns provisioned by migrations/17.0.1.0.45/pre-migrate.py
    # (or v0.46 as belt-and-braces). Plain fields, no related=.
    # CDB has broken related=partner_id.X paths for these; source fields
    # do not exist on res.partner. See feedback-related-field-source-ordering.
    binary_field_0lxfw = fields.Binary(string="New File")
    binary_field_0lxfw_filename = fields.Char(string="Filename for binary_field_0lxfw")
    binary_field_6Qgy3 = fields.Binary(string="New File")
    binary_field_6Qgy3_filename = fields.Char(string="Filename for binary_field_6Qgy3")
    boolean_field_5hcBi = fields.Boolean(string="New Checkbox")
    boolean_field_IhZPZ = fields.Boolean(string="New Checkbox")
    boolean_field_iWSSd = fields.Boolean(string="New Checkbox")
    char_field_169HD = fields.Char(string="New Text")
    char_field_vHXsn = fields.Char(string="New Text")
    char_field_zMp65 = fields.Char(string="New Text")
    created_date = fields.Date(string="Created DAte")
    created_date_1 = fields.Date()
    accounting_credit_limit = fields.Float(string="Credit Limit")
    customer_group1 = fields.Many2one("customer_group")
    date_field_Gq9rN = fields.Date(string="New Date")
    date_field_TBq7w = fields.Date(string="New Date")
    float_field_73nGS = fields.Float(string="New Decimal")
    float_field_zLCsm = fields.Float(string="New Decimal")
    mandatory_bank_gu = fields.Boolean()
    many2many_field_f1lwc = fields.Many2many("res.partner", string="Contact")
    many2one_field_3xHed = fields.Many2one("res.partner", string="Contact")
    many2one_field_hl9yL = fields.Many2one("customer_group", string="Customer Group")
    many2one_field_jhSr4 = fields.Many2one("res.partner", string="Contact")
    many2one_field_pbZO1 = fields.Many2one("res.partner", string="Contact")
    many2one_field_qX4FU = fields.Many2one("vendor_group", string="Vendor Group")
    payment_term = fields.Many2one("account.payment.term", string="Payment Term-Delete")
    related_field_49eDN = fields.Boolean(string="New Related Field")
    related_field_TZMCl = fields.Char(string="New Related Field")
    related_field_Uojrf = fields.Char(string="New Related Field")
    related_field_UwEX1 = fields.Char(string="New Related Field")
    related_field_YVuN0 = fields.Char(string="New Related Field")
    related_field_j3X4Q = fields.Many2one(
        "account.payment.term", string="New Related Field"
    )
    related_field_ngmve = fields.Many2one(
        "account.payment.term", string="New Related Field"
    )
    related_field_pEksg = fields.Selection(selection=[], string="New Related Field")
    related_field_tLbBY = fields.Many2one(
        "account.payment.term", string="New Related Field"
    )
    related_field_xfyUN = fields.Char(string="New Related Field")
    sdfsdf = fields.Date()
    selection_field_3FlOG = fields.Selection(selection=[], string="New Selection")
    selection_field_VAQjO = fields.Selection(selection=[], string="New Selection")
    selection_field_lm0NR = fields.Selection(selection=[], string="New Selection")
    selection_field_sDxoe = fields.Selection(selection=[], string="New Selection")
    terms_of_payment = fields.Many2one(
        "account.payment.term", string="Terms of Payment"
    )
    vendor_group1 = fields.Many2one("vendor_group")
