# -*- coding: UTF-8 -*-
##############################################################################
#
#    Python Script for Odoo, Open Source Management Solution
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

import xmlrpclib
import csv
from datetime import datetime, timedelta

username = "username"
pwd = "pwd"
dbname = "dbname"
baseurl = "http://localhost:8069"

sock_common = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/common")

uid = sock_common.login(dbname, username, pwd)

sock = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/object")

product_id = sock.execute(dbname, uid, pwd, 'product.template', 'search', [('default_code', '=', '508110.176')])
print"Product ID: ", product_id

#route_id = sock.execute(dbname, uid, pwd, 'stock.location.route', 'search', [('name', '=', 'Make To Order')])
route_id = sock.execute(dbname, uid, pwd, 'stock.location.route', 'search', [('name', '=', 'Buy')])

route_obj = sock.execute(dbname, uid, pwd, 'stock.location.route', 'read', route_id, ['id', 'name'])
print"Route-Obj: ", route_obj[0]['name']

RoutingData = {
                             'route_ids': [(6, 0, [route_id])],
                             }

sock.execute(dbname, uid, pwd, 'product.template', 'write', product_id, RoutingData)

print"Update Route von Produkt mit ID " + str(product_id[0]) + ' zu ' + route_obj[0]['name'] + ' geändert.'