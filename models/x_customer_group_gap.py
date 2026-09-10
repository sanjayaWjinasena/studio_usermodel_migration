# -*- coding: utf-8 -*-
from odoo import models, fields

class XCustomerGroupGap(models.Model):
    _inherit = 'x_customer_group'

    x_active = fields.Boolean(string='Active')
    x_name = fields.Char(string='Code')
