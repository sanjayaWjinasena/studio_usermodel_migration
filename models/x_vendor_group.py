# -*- coding: utf-8 -*-
"""x_vendor_group — Studio custom catalogue model ported to Python.

Sister to x_customer_group but for vendors (payable-side classification).
Clear-DB has 20+ rows across three companies covering categories like
CA-PUR (Cash Purchase Vendors), CR-PUR (Credit Purchase Vendors),
IMP-VEN (Import Vendors), EMP-PAY (Employee-related payments), etc.

Field schema mirrors Clear-DB verbatim (RPC dump 2026-08-17).
"""
from odoo import fields, models


class XVendorGroup(models.Model):
    _name = 'x_vendor_group'
    _description = 'Vendor Group'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'x_name'
    _order = 'x_studio_sequence asc, id asc'

    x_active = fields.Boolean(string='Active', default=True)
    x_name = fields.Char(string='Name', required=True)
    x_studio_sequence = fields.Integer(string='Sequence', default=10)
    x_studio_description = fields.Char(string='Description')
    x_studio_company_id = fields.Many2one(
        'res.company',
        string='Company',
    )
    x_studio_payable_account = fields.Many2one(
        'account.account',
        string='Payable Account',
    )
    x_studio_payment_term = fields.Many2one(
        'account.payment.term',
        string='Payment Term',
    )
    x_studio_one2many_field_5cEfV = fields.One2many(
        'res.partner',
        'x_studio_vendor_group',
        string='Vendors',
    )
    # v0.0.5: Studio-auto smart-button counter of linked vendors.
    x_x_studio_vendor_group__res_partner_count = fields.Integer(
        string='Res Partner Count',
        compute='_compute_res_partner_count',
        store=False,
    )

    def _compute_res_partner_count(self):
        Partner = self.env['res.partner']
        for rec in self:
            rec.x_x_studio_vendor_group__res_partner_count = Partner.search_count(
                [('x_studio_vendor_group', '=', rec.id)]
            )
