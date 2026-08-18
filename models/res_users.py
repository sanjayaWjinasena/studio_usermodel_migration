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
