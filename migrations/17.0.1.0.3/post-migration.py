# -*- coding: utf-8 -*-
"""v0.0.3 upgrade — declare x_customer_group + x_vendor_group models
and 3 res.partner FKs in Python.

On Clear-DB, the corresponding state='manual' rows already exist —
Odoo's module loader detects the Python declaration on load and
flips the state to 'base' so studio_usermodel_migration takes
ownership without touching the existing 24 customer-group / 20
vendor-group rows.

No data migration script needed; the file exists to establish the
migration folder convention.
"""


def migrate(cr, version):
    if not version:
        return
    return
