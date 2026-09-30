# -*- coding: utf-8 -*-
"""Studio field port on ir.model.access — DISABLED in v0.55.

Preemptive removal after ir.rule + base.automation crashed with the same
pattern. ir.model.access is queried whenever any ACL check runs (i.e.,
constantly). Adding a stored column without a prior ALTER TABLE would
crash on the next admin request.

Removed to keep the server stable. Re-ship via safer path (see
ir_rule.py comment).
"""
