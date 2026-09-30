# -*- coding: utf-8 -*-
"""Studio field ports on ir.model.access.

Two readonly display/reporting fields Studio added to ACL rows on CDB
to make the access-rights list view more searchable — user_name is
the group's members' logins concatenated, number_of_users is the M2M
of those users. Both are read-only; no compute defined by Studio.
"""
from odoo import fields, models


class IrModelAccess(models.Model):
    _inherit = 'ir.model.access'

    x_studio_user_name = fields.Char(string='User Name', readonly=True)
    x_studio_number_of_users = fields.Many2many(
        'res.users',
        string='Users',
        readonly=True,
    )
