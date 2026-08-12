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
from odoo import fields, models


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
