from odoo import fields, models


class XVendorGroupGap(models.Model):
    _inherit = 'x_vendor_group'

    x_active = fields.Boolean(string='Active')
    x_name = fields.Char(string='Code')
