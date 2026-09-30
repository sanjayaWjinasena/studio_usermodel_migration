# -*- coding: utf-8 -*-
"""Studio field port on ir.rule — DISABLED in v0.55.

Same crash pattern as v0.53's base.automation port:
  ERROR: column ir_rule.x_studio_description does not exist
`session_info` calls `ir.rule._compute_domain` on every request,
which SELECTs every stored column on ir.rule. On a code-pull without
`-u studio_usermodel_migration`, the ALTER TABLE hasn't run yet →
every request 500s.

Removed to unblock server. Re-ship via safer path (data-XML
ir.model.fields insert that runs ALTER TABLE before Python model
loads, or a pre_init_hook that executes the ALTER TABLE raw SQL).
"""
