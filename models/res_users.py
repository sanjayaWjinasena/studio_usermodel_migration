# -*- coding: utf-8 -*-
"""res.users Studio field port.

Ports the 4 Studio-manual x_studio_* fields on res.users that
Fix-repair's helpdesk_ticket views + the res.users form arch (id 2392
on Clear-DB, owned by Fix-repair) reference. Declared here rather
than in Fix-repair because they're user-master metadata (company,
recruitment stages, stock-location counters) — distinct from the
repair-flow location fields that legitimately live in Fix-repair
(x_studio_source_location, x_studio_virtual_location, etc.).

Fields:
  - x_studio_company_id           (m2o res.company) — per-user
      "Current Company" flag used by view-arch invisible expressions
      to swap between _1 fields across companies
  - x_studio_recr_stages          (m2m hr.recruitment.stage) —
      Recruitment tab
  - x_x_studio_users_stock_location_stock_location_count (int) —
      companion counter for the stock.location m2m on stock.location
  - x_x_studio_users_internal_transfer_stock_location_count (int) —
      companion counter for the second stock.location m2m
"""
from odoo import api, fields, models
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = 'res.users'

    x_studio_company_id = fields.Many2one(
        'res.company',
        string='Current Company',
    )
    x_studio_recr_stages = fields.Many2many(
        'hr.recruitment.stage',
        relation='res_users_studio_recr_stages_rel',
        column1='user_id',
        column2='stage_id',
        string='Recruitment Stages',
    )
    # Studio-generated companion counter fields — mirrored so the
    # Studio-arch stat buttons don't break the view load. Not
    # currently populated by Python compute since the corresponding
    # stat buttons (actions 2487/2488) are DB-specific and skipped
    # in the ported view arch. Left here as sentinels for arch
    # compatibility in case a future view inherit references them.
    x_x_studio_users_stock_location_stock_location_count = fields.Integer(
        string='Users (Stock Location) count',
    )
    x_x_studio_users_internal_transfer_stock_location_count = fields.Integer(
        string='Users (Internal Transfer) count',
    )
    # v0.0.2: the two res.users-side halves of the Studio m2m to
    # stock.location. Fix-repair declares the reverse side (on
    # stock.location) in models/stock_location.py:54-67 using specific
    # relation-table names — Q50dg / bQRSA use those SAME names so
    # both sides read/write the same relation rows. This lets Studio
    # arch that references the fields from either direction resolve
    # to a single set of user↔location links.
    x_studio_many2many_field_Q50dg = fields.Many2many(
        'stock.location',
        relation='stock_location_users_stock_location_rel',
        column1='user_id',
        column2='location_id',
        string='Inventory Locations (Stock)',
    )
    x_studio_many2many_field_bQRSA = fields.Many2many(
        'stock.location',
        relation='stock_location_users_internal_transfer_rel',
        column1='user_id',
        column2='location_id',
        string='Inventory Locations (Internal Transfer)',
    )

    # v0.0.7: repair-flow location fields moved here from Fix-repair.
    # The res.users form view in this module's views/res_users_views.xml
    # references x_studio_virtual_location, which broke registry setup
    # when studio_usermodel_migration loaded before Fix-repair.
    # These four fields are pure res.users Studio schema -- they
    # belong in this res.users-scoped module. Fix-repair's
    # helpdesk.ticket related fields still resolve because
    # studio_usermodel_migration now loads first in the graph.
    x_studio_source_location = fields.Many2one(
        'stock.location',
        string='Source Location',
    )
    x_studio_source_location_1 = fields.Many2one(
        'stock.location',
        string='Source Location',
    )
    x_studio_virtual_location = fields.Many2one(
        'stock.location',
        string='Virtual Location',
    )
    x_studio_virtual_location_1 = fields.Many2one(
        'stock.location',
        string='Virtual Location',
    )

    # v0.0.11: sentinels for Studio-manual fields that Wave 5A view-port
    # surfaces from Clear-DB. Not populated on dev; declared as inert
    # placeholders so the ported view arch validates. Fix-repair
    # ports the actual super_user booleans (see repair_admin_groups.py).
    x_studio_super_user = fields.Boolean(string='Super User (All Items)')
    x_studio_super_user_melt_items = fields.Boolean(
        string='Super User (Melt Items)',
    )
    x_studio_attendance_administrator = fields.Boolean(
        string='Attendance Administrator',
    )

    # v0.0.7: super-user permission booleans (moved from
    # Fix-repair/models/res_users.py). Native port of Studio
    # server action id 2544 which enforced mutual exclusion.
    x_studio_super_user = fields.Boolean(
        string='Super User (All Items)',
        copy=True,
    )
    x_studio_super_user_melt_items = fields.Boolean(
        string='Super User (Melt Items)',
        copy=True,
    )

    def _super_user_validate(self):
        """Studio server action id 2544 native port. Guards that a
        single user cannot hold BOTH super-user permissions."""
        for record in self:
            if record.x_studio_super_user_melt_items and record.x_studio_super_user:
                raise UserError(
                    'Both the super user permissions can not be '
                    'assigned to a single user.'
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


    # v0.0.N: Bulk-ported 47 res.users Studio fields (Fields-gap closure)
    # Auto-generated by scripts/_ship_res_users_47.py — RPC-fetched from CDB
    x_studio_binary_field_0lxfw = fields.Binary(string='New File', related='partner_id.x_studio_binary_field_0lxfw')
    x_studio_binary_field_0lxfw_filename = fields.Char(string='Filename for x_studio_binary_field_0lxfw', related='partner_id.x_studio_binary_field_0lxfw_filename')
    x_studio_binary_field_6Qgy3 = fields.Binary(string='New File', related='partner_id.x_studio_binary_field_6Qgy3')
    x_studio_binary_field_6Qgy3_filename = fields.Char(string='Filename for x_studio_binary_field_6Qgy3', related='partner_id.x_studio_binary_field_6Qgy3_filename')
    x_studio_boolean_field_5hcBi = fields.Boolean(string='New Checkbox', related='partner_id.x_studio_boolean_field_5hcBi')
    x_studio_boolean_field_IhZPZ = fields.Boolean(string='New Checkbox', related='partner_id.x_studio_boolean_field_IhZPZ')
    x_studio_boolean_field_iWSSd = fields.Boolean(string='New Checkbox', related='partner_id.x_studio_boolean_field_iWSSd')
    x_studio_char_field_169HD = fields.Char(string='New Text', related='partner_id.x_studio_char_field_169HD')
    x_studio_char_field_vHXsn = fields.Char(string='New Text', related='partner_id.x_studio_char_field_vHXsn')
    x_studio_char_field_zMp65 = fields.Char(string='New Text', related='partner_id.x_studio_char_field_zMp65')
    x_studio_created_date = fields.Date(string='Created DAte', related='partner_id.x_studio_created_date')
    x_studio_created_date_1 = fields.Date(string='X Studio Created Date 1', related='partner_id.x_studio_created_date_1')
    x_studio_credit_limit = fields.Float(string='Credit Limit', related='partner_id.x_studio_credit_limit')
    x_studio_customer_group1 = fields.Many2one('x_customer_group', string='Customer Group1', related='partner_id.x_studio_customer_group1')
    x_studio_customer_group2 = fields.Many2one('x_customer_groups', string='Customer Group2', related='partner_id.x_studio_customer_group2')
    x_studio_date_field_Gq9rN = fields.Date(string='New Date', related='partner_id.x_studio_date_field_Gq9rN')
    x_studio_date_field_TBq7w = fields.Date(string='New Date', related='partner_id.x_studio_date_field_TBq7w')
    x_studio_float_field_73nGS = fields.Float(string='New Decimal', related='partner_id.x_studio_float_field_73nGS')
    x_studio_float_field_zLCsm = fields.Float(string='New Decimal', related='partner_id.x_studio_float_field_zLCsm')
    x_studio_mandatory_bank_gu = fields.Boolean(string='Mandatory Bank Gu', related='partner_id.x_studio_mandatory_bank_gu', readonly=True)
    x_studio_many2many_field_f1lwc = fields.Many2many('res.partner', string='Contact', related='partner_id.x_studio_many2many_field_f1lwc')
    x_studio_many2one_field_3LBKs = fields.Many2one('x_customer_groups', string='Group', related='partner_id.x_studio_many2one_field_3LBKs')
    x_studio_many2one_field_3xHed = fields.Many2one('res.partner', string='Contact', related='partner_id.x_studio_many2one_field_3xHed')
    x_studio_many2one_field_9xxxo = fields.Many2one('x_customer_groups', string='Customer Groups XXX', related='partner_id.x_studio_many2one_field_9xxxo')
    x_studio_many2one_field_V9cmo = fields.Many2one('x_customer_groups', string='Customer Groups', related='partner_id.x_studio_many2one_field_V9cmo')
    x_studio_many2one_field_hl9yL = fields.Many2one('x_customer_group', string='Customer Group', related='partner_id.x_studio_many2one_field_hl9yL')
    x_studio_many2one_field_jhSr4 = fields.Many2one('res.partner', string='Contact', related='partner_id.x_studio_many2one_field_jhSr4')
    x_studio_many2one_field_pbZO1 = fields.Many2one('res.partner', string='Contact', related='partner_id.x_studio_many2one_field_pbZO1')
    x_studio_many2one_field_qX4FU = fields.Many2one('x_vendor_group', string='Vendor Group', related='partner_id.x_studio_many2one_field_qX4FU')
    x_studio_payment_term = fields.Many2one('account.payment.term', string='Payment Term-Delete', related='partner_id.x_studio_payment_term', readonly=True)
    x_studio_related_field_49eDN = fields.Boolean(string='New Related Field', related='partner_id.x_studio_related_field_49eDN', readonly=True)
    x_studio_related_field_TZMCl = fields.Char(string='New Related Field', related='partner_id.x_studio_related_field_TZMCl', readonly=True)
    x_studio_related_field_Uojrf = fields.Char(string='New Related Field', related='partner_id.x_studio_related_field_Uojrf', readonly=True)
    x_studio_related_field_UwEX1 = fields.Char(string='New Related Field', related='partner_id.x_studio_related_field_UwEX1', readonly=True)
    x_studio_related_field_YVuN0 = fields.Char(string='New Related Field', related='partner_id.x_studio_related_field_YVuN0', readonly=True)
    x_studio_related_field_j3X4Q = fields.Many2one('account.payment.term', string='New Related Field', related='partner_id.x_studio_related_field_j3X4Q', readonly=True)
    x_studio_related_field_ngmve = fields.Many2one('account.payment.term', string='New Related Field', related='partner_id.x_studio_related_field_ngmve', readonly=True)
    x_studio_related_field_pEksg = fields.Selection(selection=[], string='New Related Field', related='partner_id.x_studio_related_field_pEksg', readonly=True)
    x_studio_related_field_tLbBY = fields.Many2one('account.payment.term', string='New Related Field', related='partner_id.x_studio_related_field_tLbBY', readonly=True)
    x_studio_related_field_xfyUN = fields.Char(string='New Related Field', related='partner_id.x_studio_related_field_xfyUN', readonly=True)
    x_studio_sdfsdf = fields.Date(string='X Studio Sdfsdf', related='partner_id.x_studio_sdfsdf')
    x_studio_selection_field_3FlOG = fields.Selection(selection=[], string='New Selection', related='partner_id.x_studio_selection_field_3FlOG')
    x_studio_selection_field_VAQjO = fields.Selection(selection=[], string='New Selection', related='partner_id.x_studio_selection_field_VAQjO')
    x_studio_selection_field_lm0NR = fields.Selection(selection=[], string='New Selection', related='partner_id.x_studio_selection_field_lm0NR')
    x_studio_selection_field_sDxoe = fields.Selection(selection=[], string='New Selection', related='partner_id.x_studio_selection_field_sDxoe')
    x_studio_terms_of_payment = fields.Many2one('account.payment.term', string='Terms of Payment', related='partner_id.x_studio_terms_of_payment', readonly=True)
    x_studio_vendor_group1 = fields.Many2one('x_vendor_group', string='Vendor Group1', related='partner_id.x_studio_vendor_group1')
