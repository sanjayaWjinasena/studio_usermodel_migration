"""Post-install hooks for studio_usermodel_migration.

v0.0.4: seed customer + vendor group catalogue rows from bundled
Clear-DB snapshot (24 customer groups + 20 vendor groups).
"""

import json
import logging
import os

from odoo.tools import SQL

_logger = logging.getLogger(__name__)


def _resolve_company(env, company_name):
    """Look up a res.company by exact name. Returns False if missing."""
    if not company_name:
        return False
    Company = env["res.company"].sudo()
    rec = Company.search([("name", "=", company_name)], limit=1)
    return rec if rec else False


def seed_customer_vendor_groups(env):
    """Read data/customer_vendor_groups_seed.json and create any
    missing (name, company_id) row in customer_group / vendor_group.

    Skipped fields:
      * receivable_account / _payable_account — Clear-DB
        account ids don't map to dev-env ids. Set False so the field
        exists but the user assigns manually.
      * payment_term — same reasoning. Set False.

    Idempotent: search-by-(name, company_id) before create; skips
    existing. Every write wrapped in env.cr.savepoint() so a bad row
    doesn't poison the transaction.
    """
    payload_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "customer_vendor_groups_seed.json",
    )
    if not os.path.exists(payload_path):
        _logger.warning(
            "studio_usermodel_migration: seed JSON missing at %s",
            payload_path,
        )
        return
    with open(payload_path, encoding="utf-8") as f:
        snap = json.load(f)

    CustGrp = env["customer_group"].sudo()
    VendGrp = env["vendor_group"].sudo()

    created_cust, skipped_cust = 0, 0
    for row in snap.get("customer_group", []):
        company = _resolve_company(env, row.get("company_name"))
        if not company:
            skipped_cust += 1
            continue
        domain = [
            ("name", "=", row["name"]),
            ("accounting_company_id", "=", company.id),
        ]
        existing = CustGrp.search(domain, limit=1)
        if existing:
            skipped_cust += 1
            continue
        try:
            with env.cr.savepoint():
                CustGrp.create(
                    {
                        "name": row["name"],
                        "sequence": row.get("sequence") or 10,
                        "active": row.get("active", True),
                        "description": row.get("description") or "",
                        "group_type": row.get("group_type") or "General",
                        "accounting_company_id": company.id,
                    }
                )
                created_cust += 1
        except Exception as e:
            _logger.warning(
                "studio_usermodel_migration: could not create customer "
                "group %r (%r): %s",
                row["name"],
                row.get("company_name"),
                e,
                exc_info=True,
            )

    created_vend, skipped_vend = 0, 0
    for row in snap.get("vendor_group", []):
        company = _resolve_company(env, row.get("company_name"))
        if not company:
            skipped_vend += 1
            continue
        domain = [
            ("name", "=", row["name"]),
            ("accounting_company_id", "=", company.id),
        ]
        existing = VendGrp.search(domain, limit=1)
        if existing:
            skipped_vend += 1
            continue
        try:
            with env.cr.savepoint():
                VendGrp.create(
                    {
                        "name": row["name"],
                        "sequence": row.get("sequence") or 10,
                        "active": row.get("active", True),
                        "description": row.get("description") or "",
                        "accounting_company_id": company.id,
                    }
                )
                created_vend += 1
        except Exception as e:
            _logger.warning(
                "studio_usermodel_migration: could not create vendor group %r (%r): %s",
                row["name"],
                row.get("company_name"),
                e,
                exc_info=True,
            )

    _logger.info(
        "studio_usermodel_migration: seed_customer_vendor_groups done "
        "(customer: %d created, %d skipped; vendor: %d created, %d skipped)",
        created_cust,
        skipped_cust,
        created_vend,
        skipped_vend,
    )


# upgrade-testing branch: this branch installs functions only onto an existing database.
# Steps that write or seed business/config data are skipped while SEED_DATA is False.
SEED_DATA = False


def post_init_hook(env):
    if SEED_DATA:
        seed_customer_vendor_groups(env)
    _ensure_res_users_47_columns(env)


def _ensure_res_users_47_columns(env):
    """Fresh-install path: ensure the 47 x_studio_ columns exist on res_users.
    Mirrors migrations/17.0.1.0.43/pre-migrate.py — safe to re-run."""
    cr = env.cr
    cols = [
        ("binary_field_0lxfw_filename", "VARCHAR"),
        ("binary_field_6Qgy3_filename", "VARCHAR"),
        ("boolean_field_5hcBi", "BOOLEAN"),
        ("boolean_field_IhZPZ", "BOOLEAN"),
        ("boolean_field_iWSSd", "BOOLEAN"),
        ("char_field_169HD", "VARCHAR"),
        ("char_field_vHXsn", "VARCHAR"),
        ("char_field_zMp65", "VARCHAR"),
        ("created_date", "DATE"),
        ("created_date_1", "DATE"),
        ("accounting_credit_limit", "NUMERIC"),
        ("customer_group1", "INTEGER"),
        ("customer_group2", "INTEGER"),
        ("date_field_Gq9rN", "DATE"),
        ("date_field_TBq7w", "DATE"),
        ("float_field_73nGS", "NUMERIC"),
        ("float_field_zLCsm", "NUMERIC"),
        ("mandatory_bank_gu", "BOOLEAN"),
        ("many2one_field_3LBKs", "INTEGER"),
        ("many2one_field_3xHed", "INTEGER"),
        ("many2one_field_9xxxo", "INTEGER"),
        ("many2one_field_V9cmo", "INTEGER"),
        ("many2one_field_hl9yL", "INTEGER"),
        ("many2one_field_jhSr4", "INTEGER"),
        ("many2one_field_pbZO1", "INTEGER"),
        ("many2one_field_qX4FU", "INTEGER"),
        ("payment_term", "INTEGER"),
        ("related_field_49eDN", "BOOLEAN"),
        ("related_field_TZMCl", "VARCHAR"),
        ("related_field_Uojrf", "VARCHAR"),
        ("related_field_UwEX1", "VARCHAR"),
        ("related_field_YVuN0", "VARCHAR"),
        ("related_field_j3X4Q", "INTEGER"),
        ("related_field_ngmve", "INTEGER"),
        ("related_field_pEksg", "VARCHAR"),
        ("related_field_tLbBY", "INTEGER"),
        ("related_field_xfyUN", "VARCHAR"),
        ("sdfsdf", "DATE"),
        ("selection_field_3FlOG", "VARCHAR"),
        ("selection_field_VAQjO", "VARCHAR"),
        ("selection_field_lm0NR", "VARCHAR"),
        ("selection_field_sDxoe", "VARCHAR"),
        ("terms_of_payment", "INTEGER"),
        ("vendor_group1", "INTEGER"),
    ]
    for name, sqltype in cols:
        try:
            with cr.savepoint():
                cr.execute(
                    SQL(
                        "ALTER TABLE res_users ADD COLUMN IF NOT EXISTS %s %s",
                        SQL.identifier(name),
                        SQL(sqltype),
                    )
                )
        except Exception as e:
            _logger.warning(
                "post_init: failed to add res_users.%s (%s): %s",
                name,
                sqltype,
                e,
                exc_info=True,
            )
