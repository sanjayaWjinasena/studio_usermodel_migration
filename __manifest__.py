# -*- coding: utf-8 -*-
{
    'name': 'Studio User-Model Migration',
    'version': '17.0.1.0.7',
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
    # v0.0.6: dropped Fix-repair from depends. Adding
    # studio_usermodel_migration as a dep on BugFix-Sales (v0.47)
    # closed a 3-way cycle:
    #   studio_usermodel_migration -> Fix-repair -> BugFix-Sales
    #     -> studio_usermodel_migration
    # None of the 3 modules could install because each waited on
    # the others. Fix-repair only used this module at runtime (view
    # references to x_customer_group / x_vendor_group), never at
    # schema/model-load time -- so the manifest dep was over-strict.
    # Runtime resolution via env['x_customer_group'] still works
    # because both modules end up loaded together.
    'depends': ['base', 'hr_recruitment', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
