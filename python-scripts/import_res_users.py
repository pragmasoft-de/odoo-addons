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

data = open('csv/Vertreter.csv', 'rb')

reader = csv.reader(data)

i = 1

for row in reader:
    if row[12] == '-1' and row[9] != 'verstorben':
        i = i +1
        User = sock.execute(dbname, uid, pwd, 'res.users', 'search', [('eq_custom01', '=', row[0])])
        User = User if isinstance(User, list) else [User]
        login = row[9].replace(' ', '')
        login = login.replace(',', '')
        login = login.replace('.', '')
            
        Vertreter = {
                     'eq_custom01': row[0],
                     'name': row[9],                     
                     }
        
        SameUser = sock.execute(dbname, uid, pwd, 'res.users', 'search', ['&', ('login', '=', login), ('eq_custom01', '=', row[0])])
        if SameUser != User or len(User) == 0:
            Vertreter['login'] = login + str(i)
        else:
            Ver = sock.execute(dbname, uid, pwd, 'res.users', 'read', User)
            Vertreter['login'] = Ver.login
        
        if len(User) != 0:
            sock.execute(dbname, uid, pwd, 'res.users', 'write', User[0], Vertreter)
            print 'Vertreter ' + row[0] + ' wurder erfolgreich bearbeitet'
        else:
            sock.execute(dbname, uid, pwd, 'res.users', 'create', Vertreter)
            print 'Vertreter ' + row[0] + ' wurder erfolgreich erstellt'

print 'Fertig'