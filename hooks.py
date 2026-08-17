# -*- coding: utf-8 -*-
"""Post-install hooks for studio_usermodel_migration.

v0.0.4: seed customer + vendor group catalogue rows from bundled
Clear-DB snapshot (24 customer groups + 20 vendor groups).
"""
import json
import logging
import os

_logger = logging.getLogger(__name__)


def _resolve_company(env, company_name):
    """Look up a res.company by exact name. Returns False if missing."""
    if not company_name:
        return False
    Company = env['res.company'].sudo()
    rec = Company.search([('name', '=', company_name)], limit=1)
    return rec if rec else False


def seed_customer_vendor_groups(env):
    """Read data/customer_vendor_groups_seed.json and create any
    missing (name, company_id) row in x_customer_group / x_vendor_group.

    Skipped fields:
      * x_studio_receivable_account / _payable_account — Clear-DB
        account ids don't map to dev-env ids. Set False so the field
        exists but the user assigns manually.
      * x_studio_payment_term — same reasoning. Set False.

    Idempotent: search-by-(name, company_id) before create; skips
    existing. Every write wrapped in env.cr.savepoint() so a bad row
    doesn't poison the transaction.
    """
    payload_path = os.path.join(
        os.path.dirname(__file__), 'data', 'customer_vendor_groups_seed.json',
    )
    if not os.path.exists(payload_path):
        _logger.warning(
            'studio_usermodel_migration: seed JSON missing at %s',
            payload_path,
        )
        return
    with open(payload_path, encoding='utf-8') as f:
        snap = json.load(f)

    CustGrp = env['x_customer_group'].sudo()
    VendGrp = env['x_vendor_group'].sudo()

    created_cust, skipped_cust = 0, 0
    for row in snap.get('x_customer_group', []):
        company = _resolve_company(env, row.get('company_name'))
        if not company:
            skipped_cust += 1
            continue
        domain = [('x_name', '=', row['name']),
                  ('x_studio_company_id', '=', company.id)]
        existing = CustGrp.search(domain, limit=1)
        if existing:
            skipped_cust += 1
            continue
        try:
            with env.cr.savepoint():
                CustGrp.create({
                    'x_name': row['name'],
                    'x_studio_sequence': row.get('sequence') or 10,
                    'x_active': row.get('active', True),
                    'x_studio_description': row.get('description') or '',
                    'x_studio_group_type': row.get('group_type') or 'General',
                    'x_studio_company_id': company.id,
                })
                created_cust += 1
        except Exception as e:
            _logger.warning(
                'studio_usermodel_migration: could not create customer '
                'group %r (%r): %s',
                row['name'], row.get('company_name'), e,
            )

    created_vend, skipped_vend = 0, 0
    for row in snap.get('x_vendor_group', []):
        company = _resolve_company(env, row.get('company_name'))
        if not company:
            skipped_vend += 1
            continue
        domain = [('x_name', '=', row['name']),
                  ('x_studio_company_id', '=', company.id)]
        existing = VendGrp.search(domain, limit=1)
        if existing:
            skipped_vend += 1
            continue
        try:
            with env.cr.savepoint():
                VendGrp.create({
                    'x_name': row['name'],
                    'x_studio_sequence': row.get('sequence') or 10,
                    'x_active': row.get('active', True),
                    'x_studio_description': row.get('description') or '',
                    'x_studio_company_id': company.id,
                })
                created_vend += 1
        except Exception as e:
            _logger.warning(
                'studio_usermodel_migration: could not create vendor '
                'group %r (%r): %s',
                row['name'], row.get('company_name'), e,
            )

    _logger.info(
        'studio_usermodel_migration: seed_customer_vendor_groups done '
        '(customer: %d created, %d skipped; vendor: %d created, %d skipped)',
        created_cust, skipped_cust, created_vend, skipped_vend,
    )


def post_init_hook(env):
    seed_customer_vendor_groups(env)
