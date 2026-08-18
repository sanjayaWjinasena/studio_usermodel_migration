# -*- coding: utf-8 -*-
{
    'name': 'Studio User-Model Migration',
    'version': '17.0.1.0.5',
    'post_init_hook': 'post_init_hook',
    'summary': (
        'Ports res.users Studio customisations + customer/vendor group '
        'catalogues (x_customer_group, x_vendor_group) into proper '
        'Python modules. Companion to Fix-repair, which owns the '
        'repair-flow user fields (location m2o, super-user booleans). '
        'This module owns res.users Studio fields that don\'t fit the '
        'repair-workflow domain plus the customer/vendor classification '
        'master data (which drives per-partner payment terms + '
        'receivable/payable accounts).'
    ),
    'author': 'Jinasena Agricultural Machinery (Pvt) Ltd.',
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    # v0.0.3: added account (for account.account + account.payment.term
    # targets on the customer / vendor group catalogues).
    'depends': ['base', 'hr_recruitment', 'account', 'Fix-repair'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
