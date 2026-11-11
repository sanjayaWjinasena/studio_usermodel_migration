from . import base_automation
from . import res_users
from . import customer_group
from . import vendor_group
from . import res_partner
# v0.0.14: reverted sales_report_type/_model migration - it triggered
# a KeyError during Odoo registry.setup_models on repair-test-101 that
# blocked ALL module upgrades. Root cause under investigation. The 5
# model files stay on disk for the follow-up but aren't imported yet:
#   sales_report_type, sales_report_model, account_move,
#   account_move_line, sale_order_line
# When we re-attempt, the plan is: (1) reproduce on a scratch DB
# outside of production, (2) diagnose exact setup-order behavior,
# (3) find safe reintroduction path.
