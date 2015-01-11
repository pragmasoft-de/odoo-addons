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

reader = csv.reader(open('csv/Artikelgruppen.csv', 'rb'))

Kategorien = {}
Durchgang2 = []

next(reader)
for row in reader:
    if row[2] == 'EMPTY':
        Kat = sock.execute(dbname, uid, pwd, 'product.category', 'search', [('name', '=', row[3])])
        if len(Kat) == 0:
            Ka = sock.execute(dbname, uid, pwd, 'product.category', 'create', {'name': row[3], 'parent_id': 1, 'eq_custom01': row[1]})
            K = [Ka]
            Kategorien[row[1]] = K if isinstance(Ka, int) else Ka
            print 'Kategorie ' + row[3] + ' wurde erstellt.'
        else:
            Kategorien[row[1]] = Kat
            sock.execute(dbname, uid, pwd, 'product.category', 'write', Kat, {'name': row[3], 'eq_custom01': row[1]})
            print 'Kategorie ' + row[3] + ' wurde bearbeitet.'
    elif row[2] in Kategorien:
        Kat = sock.execute(dbname, uid, pwd, 'product.category', 'search', [('name', '=', row[3])])
        if len(Kat) == 0:
            Ka = sock.execute(dbname, uid, pwd, 'product.category', 'create', {'name': row[3], 'parent_id': Kategorien[row[2]][0], 'eq_custom01': row[1]})
            K = [Ka]
            Kategorien[row[1]] = K if isinstance(Ka, int) else Ka
            print 'Kategorie ' + row[3] + ' wurde erstellt.'
        else:
            Kategorien[row[1]] = Kat
            sock.execute(dbname, uid, pwd, 'product.category', 'write', Kat, {'name': row[3], 'parent_id': Kategorien[row[2]][0], 'eq_custom01': row[1]})
            print 'Kategorie ' + row[3] + ' wurde bearbeitet.'
    else:
        Durchgang2.append[row]

Durchgang2.sort(key=lambda row: row[2])


for row in Durchgang2:
    if row[2] in Kategorien:
        Kat = sock.execute(dbname, uid, pwd, 'product.category', 'search', [('name', '=', row[3])])
        if len(Kat) == 0:
            Ka = sock.execute(dbname, uid, pwd, 'product.category', 'create', {'name': row[3], 'parent_id': Kategorien[row[2]][0], 'eq_custom01': row[3]})
            K = [Ka]
            Kategorien[row[1]] = K if isinstance(Ka, int) else Ka
            print 'Kategorie ' + row[3] + ' wurde erstellt.'
        else:
            Kategorien[row[1]] = Kat
            print 'Kategorie ' + row[3] + ' besteht bereits.'

print 'Fertig'