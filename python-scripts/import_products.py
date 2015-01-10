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
import csv
from datetime import datetime, timedelta

username = "admin"
pwd = "****"
dbname = "yourdbname"
baseurl = "http://localhost:8069"

sock_common = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/common")

uid = sock_common.login(dbname, username, pwd)

sock = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/object")

reader = csv.reader(open('csv/Artikel zum Uebertrag.csv', 'rb'))

Kategorien = {}
Durchgang2 = []

next(reader)
next(reader)
for row in reader:
    ProductData = {
                   'name': row[1] + ' ' + row[2],                   #Bezeichnung1 + Bezeichnung2
                   'standart_price': row[9],                        #LetzterEK
                   'purchase_ok': False if row[6] == '0' else True, #IstBestellartikel
                   'sale_ok': False if row[7] == '0' else True,     #IstVerkaufsartikel
                   'active': True,
                   'state': 'sellable',
                   'taxes_id': [(6, 0, [12])],
                   'supplier_taxes_id': [(6, 0, [14])],
                   'list_price': row[19],
                   'standard_price':  row[9],
                   }
    #Produktnummer
    if row[0] != '':
        ProductData['eq_default_code'] = row[0]
        ProductData['default_code'] = row[0]

    
    """
    #Basismengeneinheit
    if row[5] != None and row[5] != '':
        UOM_id = sock.execute(dbname, uid, pwd, 'product.uom', 'search', [('name', '=', row[5])])
        if len(UOM_id) == 1:
            ProductData['uom_id'] =  UOM_id if isinstance(UOM_id, int) else UOM_id[0]
        elif not UOM_id:
            K =  sock.execute(dbname, uid, pwd, 'product.uom', 'create', {'name': row[5], 'active': True, 'uom_type': 'reference', 'rounding': 1.000, 'factor':1.000000000000, 'category_id': 1,})
            ProductData['uom_id'] =  K if isinstance(K, int) else K[0]
    """"""
    #Basismengeneinheit
    if row[5] != None and row[5] != '':
        if row[5] == 'Stk':
            ProductData['uom_id'] = 1
        elif row[5] == 'kg':
            ProductData['uom_id'] = 3
            """
    #Produktcategori
    if row[3] != '':
        Catag_id = sock.execute(dbname, uid, pwd, 'product.category', 'search', [('eq_custom01', '=', row[3])])
        if len(Catag_id) != 0:
            ProductData['categ_id'] = Catag_id[0]
            
    ProductData['uom_id'] = 1

    Search = sock.execute(dbname, uid, pwd, 'product.template', 'search', [('name', '=', row[1] + ' ' + row[2])])
    if len(Search) == 0:
        pro_id = sock.execute(dbname, uid, pwd, 'product.template', 'create', ProductData)
        print 'Artikel mit der Artikelnummer ' + row[0] + ' wurde erstellt.'
    else:
        pro_id = sock.execute(dbname, uid, pwd, 'product.template', 'write', Search, ProductData)
        print 'Artikel mit der Artikelnummer ' + row[0] + ' wurde bearbeitet.' 
        
        #Lieferanten
    if row[12] != '' and row[12] != None:
        Lieferant_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search', [('eq_creditor_ref', '=', row[17][1:])])
        if len(Lieferant_id) != 0:
            Lieferant = sock.execute(dbname, uid, pwd, 'res.partner', 'read', Lieferant_id)
            LieferantData = {
                             'name': Lieferant[0]['id'],
                             'product_name': row[13],
                             'min_qty': 1,
                             'product_tmpl_id': pro_id if pro_id != True else Search[0],
                             }
            Vorhanden = sock.execute(dbname, uid, pwd, 'product.supplierinfo', 'search', ['&', '&', ('name', '=', Lieferant[0]['id']), ('product_name', '=', row[13]), ('product_tmpl_id', '=', pro_id if pro_id != True else Search[0])])
            if len(Vorhanden) == 0:
                seller_id = sock.execute(dbname, uid, pwd, 'product.supplierinfo', 'create', LieferantData)
            else:
                sock.execute(dbname, uid, pwd, 'product.supplierinfo', 'write', Vorhanden, LieferantData)
                seller_id = Vorhanden
    
    #EAN
    if row[4] != '':
        try:
            EAN = {'ean13': row[4]}
            sock.execute(dbname, uid, pwd, 'product.supplierinfo', 'write', seller_id, EAN)
        except:
            print 'Die EAN ' + row[4] + ' für das Produkt mit der Artikelnummer ' + row[0] + ' ist ungültig.'
            
        
print 'Fertig'