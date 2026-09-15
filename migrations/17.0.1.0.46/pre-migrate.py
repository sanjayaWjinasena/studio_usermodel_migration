"""Pre-migrate v0.46: belt-and-braces ALTER TABLE IF NOT EXISTS.

v0.45 already created these columns; v0.46 adds the Python field
declarations. This pre-migrate re-runs the ALTERs harmlessly in case
someone upgrades directly from <=v0.44 to v0.46 skipping v0.45.
"""

import logging
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return
    cols = [
        ('x_studio_binary_field_0lxfw_filename', 'VARCHAR'),
        ('x_studio_binary_field_6Qgy3_filename', 'VARCHAR'),
        ('x_studio_boolean_field_5hcBi', 'BOOLEAN'),
        ('x_studio_boolean_field_IhZPZ', 'BOOLEAN'),
        ('x_studio_boolean_field_iWSSd', 'BOOLEAN'),
        ('x_studio_char_field_169HD', 'VARCHAR'),
        ('x_studio_char_field_vHXsn', 'VARCHAR'),
        ('x_studio_char_field_zMp65', 'VARCHAR'),
        ('x_studio_created_date', 'DATE'),
        ('x_studio_created_date_1', 'DATE'),
        ('x_studio_credit_limit', 'NUMERIC'),
        ('x_studio_customer_group1', 'INTEGER'),
        ('x_studio_customer_group2', 'INTEGER'),
        ('x_studio_date_field_Gq9rN', 'DATE'),
        ('x_studio_date_field_TBq7w', 'DATE'),
        ('x_studio_float_field_73nGS', 'NUMERIC'),
        ('x_studio_float_field_zLCsm', 'NUMERIC'),
        ('x_studio_mandatory_bank_gu', 'BOOLEAN'),
        ('x_studio_many2one_field_3LBKs', 'INTEGER'),
        ('x_studio_many2one_field_3xHed', 'INTEGER'),
        ('x_studio_many2one_field_9xxxo', 'INTEGER'),
        ('x_studio_many2one_field_V9cmo', 'INTEGER'),
        ('x_studio_many2one_field_hl9yL', 'INTEGER'),
        ('x_studio_many2one_field_jhSr4', 'INTEGER'),
        ('x_studio_many2one_field_pbZO1', 'INTEGER'),
        ('x_studio_many2one_field_qX4FU', 'INTEGER'),
        ('x_studio_payment_term', 'INTEGER'),
        ('x_studio_related_field_49eDN', 'BOOLEAN'),
        ('x_studio_related_field_TZMCl', 'VARCHAR'),
        ('x_studio_related_field_Uojrf', 'VARCHAR'),
        ('x_studio_related_field_UwEX1', 'VARCHAR'),
        ('x_studio_related_field_YVuN0', 'VARCHAR'),
        ('x_studio_related_field_j3X4Q', 'INTEGER'),
        ('x_studio_related_field_ngmve', 'INTEGER'),
        ('x_studio_related_field_pEksg', 'VARCHAR'),
        ('x_studio_related_field_tLbBY', 'INTEGER'),
        ('x_studio_related_field_xfyUN', 'VARCHAR'),
        ('x_studio_sdfsdf', 'DATE'),
        ('x_studio_selection_field_3FlOG', 'VARCHAR'),
        ('x_studio_selection_field_VAQjO', 'VARCHAR'),
        ('x_studio_selection_field_lm0NR', 'VARCHAR'),
        ('x_studio_selection_field_sDxoe', 'VARCHAR'),
        ('x_studio_terms_of_payment', 'INTEGER'),
        ('x_studio_vendor_group1', 'INTEGER'),
    ]
    for name, sqltype in cols:
        try:
            cr.execute(
                'ALTER TABLE res_users ADD COLUMN IF NOT EXISTS "'
                + name + '" ' + sqltype
            )
        except Exception as e:
            _logger.warning("pre-migrate v0.46 belt-and-braces: %s (%s): %s", name, sqltype, e)
