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
__author__ = 'm.schmid@equitania.com'
import xmlrpclib
import csv

username = "admin"
pwd = "***"
dbname = "dbbane"
baseurl = "http://192.168.0.29:8069"

sock_common = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/common")

uid = sock_common.login(dbname, username, pwd)

sock = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/object")

#"CNKEY","CN","EN","DE","FR"
reader = csv.reader(open('intrastat_codes.csv', 'rb'))

intI = 1
for row in reader:
    print row[0] + " " + row[3] + " Durchlauf:" + str(intI)
    if (intI > 0):
        # Intrastatcode
        intrastat = {
            'name': row[0][:2],
            'description': row[3]

        }
        intrastat_id = sock.execute(dbname, uid, pwd, 'report.intrastat.code', 'create', intrastat)

    intI += 1

print 'Fertig'
