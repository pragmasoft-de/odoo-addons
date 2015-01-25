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
__author__ = 'a.bertram@equitania.com'
import xmlrpclib

username = "admin"
pwd = "xxx"
dbname = "xxx"
baseurl = "http://localhost:8069"

sock_common = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/common")

uid = sock_common.login(dbname, username, pwd)

sock = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/object")

#Purchase Tax
purchase_tax = sock.execute(dbname, uid, pwd, 'account.tax', 'search', [('description', '=', '19% VSt')])

products_without_purchase_tax = sock.execute(dbname, uid, pwd, 'product.template', 'search', [('supplier_taxes_id', '=', False)])

for product_id in products_without_purchase_tax:
    sock.execute(dbname, uid, pwd, 'product.template', 'write', product_id, {'supplier_taxes_id': [(6, 0, [purchase_tax[-1]])]})
    print('Steuern für Produkt ' + str(product_id) + ' hinzugefügt.')
    
#Sale Tax
sale_tax = sock.execute(dbname, uid, pwd, 'account.tax', 'search', [('description', '=', '19% USt')])

products_without_sale_tax = sock.execute(dbname, uid, pwd, 'product.template', 'search', [('taxes_id', '=', False)])

for product_id in products_without_sale_tax:
    sock.execute(dbname, uid, pwd, 'product.template', 'write', product_id, {'taxes_id': [(6, 0, [sale_tax[-1]])]})
    print('Steuern für Produkt ' + str(product_id) + ' hinzugefügt.')
