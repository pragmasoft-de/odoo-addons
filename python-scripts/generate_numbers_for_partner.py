# -*- coding: UTF-8 -*-
##############################################################################
#
# Python Script for Odoo, Open Source Management Solution
# Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
__author__ = 'a.bertram@equitania.com'

import xmlrpclib

username = "admin"
pwd = "****"
dbname = "yourdbname"
baseurl = "http://localhost:8069"

sock_common = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/common")

uid = sock_common.login(dbname, username, pwd)

sock = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/object")

#Customer and Supplier Numbers
customer_number = 10000
supplier_number = 70000

#Gets all Partners
partner_ids = sock.execute(dbname, uid, pwd, 'res.partner', 'search', [])

for partner_id in partner_ids:
    vals = {}
    partner = sock.execute(dbname, uid, pwd, 'res.partner', 'read', partner_id)
    if partner['customer'] == True and partner['is_company'] == True:
        vals['eq_customer_ref'] = customer_number
        customer_number += 1
    if partner['supplier'] == True and partner['is_company'] == True:
        vals['eq_creditor_ref'] = supplier_number
        supplier_number += 1
    sock.execute(dbname, uid, pwd, 'res.partner', 'write', partner_id, vals)
    print('Die Kunden/Lieferantennummer wurde für den Partner mit der ID "' + str(partner_id) + '" gesetzt.')
print('Fertig!')