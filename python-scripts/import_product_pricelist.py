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

data = open('csv/Preislisten.csv', 'rb')

reader = csv.reader(data)

IDs_for_import = ['27', '35', '38', '39']

next(reader)
for row in reader:
    if row[0] in IDs_for_import:
        Vorhanden = sock.execute(dbname, uid, pwd, 'product.pricelist.version', 'search', [('eq_custom01', '=', row[0])])
        startDatum = None        
        if row[5] != None and row[5] != '':
            ds = datetime.strptime(row[5], "%m/%d/%Y %H:%M")
            startDatum =  ds.strftime("%Y-%m-%d %H:%M")
        endDatum = None
        if row[6] != None and row[6] != '':
            de = datetime.strptime(row[6], "%m/%d/%Y %H:%M")
            endDatum =  de.strftime("%Y-%m-%d %H:%M")
            
        PreislisteDaten = {
                           'eq_custom01': row[0],
                           'name': row[1],
                           'active': True if datetime.now() > ds and datetime.now() < de else False,
                           'type': 'sale',
                           }
        if len(Vorhanden) == 0:
            pricelist_id = sock.execute(dbname, uid, pwd, 'product.pricelist', 'create', PreislisteDaten)
            pricelist_id = pricelist_id if isinstance(pricelist_id, int) else pricelist_id[0]
            print ' Preisliste erstellt'
        else:
            Preisliste = sock.execute(dbname, uid, pwd, 'product.pricelist.version', 'read', Vorhanden)
            sock.execute(dbname, uid, pwd, 'product.pricelist', 'write', Preisliste[0]['pricelist_id'], PreislisteDaten)
            print ' Preisliste bearbeitet'
        
        PreislistenverisonDaten = {
                                  'name': row[1],
                                  'eq_custom01': row[0],
                                  'pricelist_id': int(pricelist_id),
                                  }
        
        if len(Vorhanden) == 0:
            pricelist_version_id = sock.execute(dbname, uid, pwd, 'product.pricelist.version', 'create', PreislistenverisonDaten)
            pricelist_version_id = pricelist_id if isinstance(pricelist_id, int) else pricelist_id[0]
            print ' Preislistenversion erstellt'
        else:
            pricelist_version_id = Vorhanden if isinstance(Vorhanden, int) else Vorhanden[0]
            sock.execute(dbname, uid, pwd, 'product.pricelist.version', 'write', pricelist_version_id, PreislistenverisonDaten)
            print ' Preislistenversion bearbeitet'

print 'Fertig'