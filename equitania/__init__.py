# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import eq_install_func
import res_users
import wizard
import eq_partner_extension
import eq_lead_referred
import sale
import res_partner_old
import res_groups
import stock
import sale_layout
import reports
import res_config
import res_partner
import eq_report_helper
import product
import eq_clean_data
import stock_old
import company
import crm
import account_invoice_old
import purchase_old
import sale_old
import product_old
import purchase
import eq_open_sale_order_line

# NOTE: causing big problem right now - it's not possible to save users with this module installed !
# NOTE: try to create new user and save
#import eq_email

# NOTE: causing next problem - it's not possible to save users with this module installed !
# NOTE: try to change employee by existing user and save
#import hr