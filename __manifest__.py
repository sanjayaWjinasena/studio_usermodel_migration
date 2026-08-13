# -*- coding: utf-8 -*-
{
    'name': 'Studio User-Model Migration',
    'version': '17.0.1.0.2',
    'summary': (
        'Ports res.users Studio customisations (custom fields + form '
        'inherit) into a proper Python module. Companion to Fix-repair, '
        'which owns the repair-flow user fields (location m2o, super-user '
        'booleans). This module owns the res.users-side fields that '
        'don\'t fit the repair-workflow domain: x_studio_company_id, '
        'x_studio_recr_stages (m2m hr.recruitment.stage), and the two '
        'Studio companion counter integers.'
    ),
    'author': 'Jinasena Agricultural Machinery (Pvt) Ltd.',
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    # base for res.users, hr_recruitment for the m2m target, Fix-repair
    # because we co-own the res.users form arch with the location fields
    # it declares.
    'depends': ['base', 'hr_recruitment', 'Fix-repair'],
    'data': [
        'views/res_users_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
