# -*- coding: utf-8 -*-
"""x_customer_group — Studio custom catalogue model ported to Python.

Clear-DB defines this as a `state='manual'` model with 10 custom fields
under module=studio_customization. Ported here so any target env
without Studio can install it fresh; on Clear-DB the module upgrade
flips the state to `'base'` and takes ownership without touching the
existing 24+ catalogue rows.

Related fields on other models that reference this catalogue:
  * res.partner.x_studio_customer_group (m2o, in res_partner.py here)
  * res.partner.x_studio_group_type (Selection, mirror of the group's
    x_studio_group_type for indexing)
  * sale.order.line and product.pricelist read the group's group_type
    for pricing rules

Field schema mirrors Clear-DB verbatim (RPC dump 2026-08-17):
  x_studio_group_type in ('General', 'Distributor', 'Dealer')
  x_studio_receivable_account m2o account.account
  x_studio_payment_term m2o account.payment.term
"""
from odoo import fields, models


class XCustomerGroup(models.Model):
    _name = 'x_customer_group'
    _description = 'Customer Group'
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
    x_studio_group_type = fields.Selection(
        selection=[
            ('General', 'General'),
            ('Distributor', 'Distributor'),
            ('Dealer', 'Dealer'),
        ],
        string='Group Type',
        default='General',
    )
    # Receivable account + payment term drive per-group pricing /
    # accounting defaults on the customer partners referencing this
    # group. Both m2o targets provided by the account module (added
    # to manifest depends in v0.0.3).
    x_studio_receivable_account = fields.Many2one(
        'account.account',
        string='Receivable Account',
    )
    x_studio_payment_term = fields.Many2one(
        'account.payment.term',
        string='Payment Term',
    )
    # One2many to res.partner. On Clear-DB the inverse field is
    # `x_studio_customer_group` on res.partner (declared in
    # res_partner.py in this module). The Studio cryptic name
    # `x_studio_one2many_field_hfDGm` kept verbatim for view-arch
    # portability.
    x_studio_one2many_field_hfDGm = fields.One2many(
        'res.partner',
        'x_studio_customer_group',
        string='Customers',
    )
    # v0.0.5: Studio-auto smart-button counter of linked customers.
    # On Clear-DB this is a Studio-generated Integer computed via a
    # search-count on the O2M. Declaring it here keeps port parity;
    # the compute is stubbed as a stored=False search-based method.
    x_x_studio_customer_group__res_partner_count = fields.Integer(
        string='Res Partner Count',
        compute='_compute_res_partner_count',
        store=False,
    )

    def _compute_res_partner_count(self):
        Partner = self.env['res.partner']
        for rec in self:
            rec.x_x_studio_customer_group__res_partner_count = Partner.search_count(
                [('x_studio_customer_group', '=', rec.id)]
            )
