# -*- coding: utf-8 -*-
"""Studio field port on ir.rule — free-form description field."""
from odoo import fields, models


class IrRule(models.Model):
    _inherit = 'ir.rule'

    x_studio_description = fields.Text(string='Description', copy=True)
