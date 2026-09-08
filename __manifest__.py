# -*- coding: utf-8 -*-
{
    'name': 'Jinasena : Masterdata : User',
    'version': '17.0.1.0.21',
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
    # v0.0.14 reverts the sale dep added in v0.0.13. The upstream
    # migration of x_sales_report_type failed during Odoo registry
    # setup on repair-test-101 (KeyError on x_studio_journal_items_id
    # during related-field setup) and blocked all further upgrades
    # on the env. Reverted here so the env can move again while we
    # diagnose offline.
    'depends': ['base', 'hr_recruitment', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/res_users_studio_ported.xml',
        'data/record_rules.xml',
        'data/server_actions_backlog.xml',
        'data/automations_backlog.xml',
        'data/window_actions_backlog.xml',
        'data/menus_all_models.xml',
        'data/menus_from_routing.xml',
        'data/mail_templates_from_routing.xml',
        'data/server_actions_gap.xml',
        'data/ir_defaults_gap.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
