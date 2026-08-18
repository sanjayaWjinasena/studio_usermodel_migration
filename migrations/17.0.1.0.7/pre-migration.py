# -*- coding: utf-8 -*-
"""v0.0.7 pre-migration -- create res.users columns before ORM reads them.

The 4 x_studio_*_location + 2 x_studio_super_user_* fields were newly
adopted by this module in v0.0.7. On dev envs where Fix-repair never
successfully installed those columns (transient install failures
during the migration project), a fresh boot with these fields declared
here triggers:

    psycopg2.errors.UndefinedColumn: column
    res_users.x_studio_source_location does not exist

...on any query that fetches res.users. Odoo would normally auto-init
the columns during this module's upgrade, but the read can happen
BEFORE upgrade -- e.g. during load_modules' vacuum_cron trigger, which
resolves env.company -> fetches user -> SELECTs all declared columns.

Fix: add all 6 columns idempotently via raw SQL before any ORM code
runs. Odoo's normal _auto_init pass later fills in constraint metadata
if needed.
"""


def migrate(cr, version):
    for col in (
        'x_studio_source_location',
        'x_studio_source_location_1',
        'x_studio_virtual_location',
        'x_studio_virtual_location_1',
    ):
        cr.execute(
            f'ALTER TABLE res_users ADD COLUMN IF NOT EXISTS {col} integer'
        )
    for col in (
        'x_studio_super_user',
        'x_studio_super_user_melt_items',
    ):
        cr.execute(
            f'ALTER TABLE res_users ADD COLUMN IF NOT EXISTS {col} boolean'
        )
