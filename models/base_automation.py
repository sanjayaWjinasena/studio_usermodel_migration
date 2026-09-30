# -*- coding: utf-8 -*-
"""Studio field ports on base.automation — DISABLED in v0.54.

v0.53 shipped these 2 fields as stored columns. That crashed Dev's
server on restart: Odoo's `base_automation._register_hook` (runs at
every registry init) does a SELECT of every stored column. On a
code-pull without an `-u studio_usermodel_migration` the Python class
knew about the new columns but ALTER TABLE hadn't run, so the SELECT
crashed with `column base_automation.x_studio_comments does not exist`.

Fields removed entirely in v0.54 to unbreak the server. Re-ship these
2 fields safely later via a data-XML `<field name="ttype">` approach
that inserts the columns before the Python class registers them.
"""
