Jinasena : Masterdata : User
============================

Ports res.users Studio customisations + customer/vendor group catalogues (x_customer_group, x_vendor_group) into proper Python modules. Companion to Fix-repair, which owns the repair-flow user fields (location m2o, super-user booleans). This module owns res.users Studio fields that don't fit the repair-workflow domain plus the customer/vendor classification master data (which drives per-partner payment terms + receivable/payable accounts).

Information
-----------

* Technical name: ``studio_usermodel_migration``
* Version: ``17.0.1.0.63``
* Depends on: ``base``, ``hr_recruitment``, ``account``, ``bank-data``
* Author: Jinasena Agricultural Machinery (Pvt) Ltd.
* License: LGPL-3

Further documentation
---------------------

* Functional documentation: ``Functional_Documentation.md``
* Change history: ``CHANGELOG.md``
