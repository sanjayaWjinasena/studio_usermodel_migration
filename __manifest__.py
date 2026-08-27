# -*- coding: utf-8 -*-
{
    'name': 'Studio User-Model Migration',
    'version': '17.0.1.0.8',
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
    #
    # NOTE: studio_migrations is a real dep — it declares
    # res.users.x_studio_attendance_administrator, which is referenced
    # by the Odoo Studio view in the DB ("Odoo Studio: res.users.form
    # customization"). Odoo validates the full view tree when loading
    # this module's res_users_views.xml, so studio_migrations must be
    # fully loaded first or that validation fails.
    # The cycle was broken instead by removing studio_usermodel_migration
    # from BugFix-Sales's depends (v52 of BugFix-Sales): BugFix-Sales
    # uses nothing from studio_usermodel_migration at schema/model-load
    # time, so that dep was the over-strict one.
    'depends': ['base', 'hr_recruitment', 'account', 'studio_migrations'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/res_users_studio_ported.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
