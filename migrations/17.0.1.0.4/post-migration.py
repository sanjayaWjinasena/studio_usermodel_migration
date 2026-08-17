# -*- coding: utf-8 -*-
"""v0.0.4 upgrade — seed customer + vendor group catalogue rows.

post_init_hook only fires on fresh install; upgrade path runs the
same hook via this migration. Idempotent — search-by-(name,
company_id) skips existing rows.
"""
import importlib.util
import os

from odoo import api, SUPERUSER_ID
from odoo.modules.module import get_module_path


def migrate(cr, version):
    if not version:
        return
    hooks_path = os.path.join(
        get_module_path('studio_usermodel_migration'), 'hooks.py'
    )
    spec = importlib.util.spec_from_file_location('summ_hooks', hooks_path)
    hooks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hooks)
    env = api.Environment(cr, SUPERUSER_ID, {})
    hooks.seed_customer_vendor_groups(env)
