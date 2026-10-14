"""v1.0.63: give back the menus that the rohana_access app locked to the Rohana group.

rohana_access 17.0.2.0.0 (post_init_hook, step 4) adds this module's Rohana group
(group_studio_518_rohana) to the menus listed below. A menu with no groups is
visible to every user; once one group is added, ONLY that group sees it. Every
menu in the list that had no groups (the whole Sales app, CRM > Sales,
Inventory > Products, ...) became Rohana-only, so users lost the Sales app.
Uninstalling rohana_access does not undo it: the group belongs to this module.

This post-migrate removes the Rohana group from those menus only, and only where
Rohana is the menu's sole group, which restores Clear-DB's state (visible to
everyone). Menus with other groups are left alone. ORM only, idempotent.
"""
import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

# Menus rohana_access 17.0.2.0.0 adds the Rohana group to (ROHANA_MENU_XMLIDS).
ROHANA_ACCESS_MENUS = (
    'crm.crm_menu_sales',
    'crm.menu_crm_opportunities',
    'crm.crm_lead_menu_my_activities',
    'crm.sales_team_menu_team_pipeline',
    'crm.res_partner_menu_customer',
    'crm.crm_team_config',
    'stock.menu_stock_root',
    'stock.menu_stock_inventory_control',
    'stock.menu_product_variant_config_stock',
    'stock.product_product_menu',
    'account_reports.menu_action_account_report_sales',
    'point_of_sale.menu_point_of_sale_list',
    'point_of_sale.menu_report_order_details',
    'sale.sale_menu_root',
    'sale.sale_order_menu',
    'sale.menu_sale_quotations',
    'sale.menu_sale_order',
    'sale.report_sales_team',
    'sale.res_partner_menu',
    'sale.menu_sale_invoicing',
    'sale.menu_sale_order_invoice',
    'sale.menu_sale_order_upselling',
    'sale.product_menu_catalog',
    'sale.menu_product_template_action',
    'sale.menu_products',
    'sale.menu_product_pricelist_main',
    'sale.menu_sale_report',
    'sale.menu_reporting_sales',
    'sale.menu_reporting_salespeople',
    'sale.menu_reporting_product',
    'sale.menu_reporting_customer',
    'sale.menu_sale_config',
    'sale.menu_sale_general_settings',
    'sale.sales_team_config',
    'sale.menu_sales_config',
    'sale.menu_tag_config',
    'sale.prod_config_main',
    'sale.menu_product_attribute_action',
    'sale.menu_product_categories',
    'sale.payment_menu',
    'sale.payment_provider_menu',
    'sale.payment_method_menu',
    'sale.next_id_16',
    'sale.menu_product_uom_categ_form_action',
    'sale.sale_menu_config_activity_plan',
    'delivery.sale_menu_action_delivery_carrier_form',
    'sale_crm.sale_order_menu_quotations_crm',
    'sale_loyalty.menu_discount_loyalty_type_config',
    'sale_loyalty.menu_gift_ewallet_type_config',
    'sale_management.sale_order_template_menu',
    'website_sale.menu_report_sales',
    'sale_planning.sale_planning_menu_schedule_by_sale_order',
    'jinasena_helpdesk_repair.menu_repair_sales_order_list',
)


def migrate(cr, version):
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    rohana = env.ref('studio_usermodel_migration.group_studio_518_rohana', raise_if_not_found=False)
    if not rohana:
        return
    menus = env['ir.ui.menu'].with_context(active_test=False)
    for xmlid in ROHANA_ACCESS_MENUS:
        menus |= env.ref(xmlid, raise_if_not_found=False) or env['ir.ui.menu']
    locked = menus.filtered(lambda m: m.groups_id == rohana)
    if locked:
        locked.write({'groups_id': [(3, rohana.id)]})
    _logger.info("studio_usermodel_migration v1.0.63: removed Rohana-only restriction from %s menu(s): %s",
                 len(locked), ', '.join(locked.mapped('complete_name')))
