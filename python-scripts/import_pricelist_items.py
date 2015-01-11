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

data = open('csv/Preislisten_Artikel.csv', 'rb')

reader = csv.reader(data)
Sequenzen = {}
next(reader)
for row in reader:
    Preislistenversion_id = sock.execute(dbname, uid, pwd, 'product.pricelist.version', 'search', [('eq_custom01', '=', row[0])])
    if Preislistenversion_id != []:
        Preislistenversion_id = Preislistenversion_id if isinstance(Preislistenversion_id, int) else Preislistenversion_id[0]
        Produkt_id = sock.execute(dbname, uid, pwd, 'product.template', 'search', [('eq_default_code', '=', row[1])])
        if len(Produkt_id) != 0:
            Produkt_id = Produkt_id if isinstance(Produkt_id, int) else Produkt_id[0],
            Produkt = {
                       'name': row[1],
                       'price_discount': -1,
                       'price_surcharge': float(row[3]),
                       'base': 1,
                       'product_id': Produkt_id[0],
                       'price_version_id': Preislistenversion_id,
                       'min_quantity': 0,
                       }
            
            #Sequenz
            if Preislistenversion_id in Sequenzen:
                Sequenzen[Preislistenversion_id] = Sequenzen[Preislistenversion_id] + 10
            else:
                Sequenzen[Preislistenversion_id] = 10
            Produkt['sequence'] = Sequenzen[Preislistenversion_id]
                
            #AbMenge
            if row[2] != None and row[2] != '':
                MBM = int(row[2])
                Produkt['min_quantity'] = MBM
            else:
                Produkt['min_quantity'] = 0
                
            
            Vorhandenes_Produkt = sock.execute(dbname, uid, pwd, 'product.pricelist.item', 'search', ['&', '&', ('price_version_id', '=', Preislistenversion_id), ('price_surcharge', '=', float(row[3])), ('product_id', '=', Produkt_id),('min_quantity', '=', MBM),])
            
            if len(Vorhandenes_Produkt) != 0:
                sock.execute(dbname, uid, pwd, 'product.pricelist.item', 'write', Vorhandenes_Produkt, Produkt)
                print 'Produkt ' + row[1]+ ' für die Preisliste ' + row[0] + ' wurde bearbeitet.'
            else:        
                sock.execute(dbname, uid, pwd, 'product.pricelist.item', 'create', Produkt)
                print 'Produkt ' + row[1]+ ' wurde in die Preisliste ' + row[0] + ' eingefügt.'

print 'Fertig'
    