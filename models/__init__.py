# -*- coding: utf-8 -*-
from . import res_users
from . import x_customer_group
from . import x_vendor_group
from . import res_partner
# v0.0.14: reverted x_sales_report_type/_model migration - it triggered
# a KeyError during Odoo registry.setup_models on repair-test-101 that
# blocked ALL module upgrades. Root cause under investigation. The 5
# model files stay on disk for the follow-up but aren't imported yet:
#   x_sales_report_type, x_sales_report_model, account_move,
#   account_move_line, sale_order_line
# When we re-attempt, the plan is: (1) reproduce on a scratch DB
# outside of production, (2) diagnose exact setup-order behavior,
# (3) find safe reintroduction path.

from . import x_customer_group_gap
from . import x_vendor_group_gap
