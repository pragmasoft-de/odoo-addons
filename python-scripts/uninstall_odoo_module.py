#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Mit diesem Skript kann man odoo Module deinstallieren
#
# Beispiel: ./uninstall_odoo_module.py -d equitania -u admin -w '***' -s 'https://myodoo.de' website_lang
# ./uninstall_odoo_module.py -d basis_skr04 -u admin -w '***' -s 'http://localhost:8069' pad
#
##############################################################################
#
#    Shell Script for Odoo, Open Source Management Solution
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
"""Uninstall a module"""

import xmlrpclib
import argparse
import getpass

parser = argparse.ArgumentParser()
# Connection args
parser.add_argument('-d', '--database', help="Use DB as the database name",
                    action='store', metavar='DB', default=getpass.getuser())
parser.add_argument('-u', '--user', help="Use USER as the database user name",
                    action='store', metavar='USER', default='admin')
parser.add_argument('-w', '--password',
                    help="Use PASSWORD as the database password.",
                    action='store', metavar='PASSWORD', default='admin')
parser.add_argument('-s', '--url',
                    help="Point to the web services hosted at URL",
                    action='store', metavar='URL',
                    default='http://localhost:8069')
# Feature args
parser.add_argument('module', help="Uninstall the module MODULE",
                    action='store', metavar='MODULE')

args = vars(parser.parse_args())

# Log in
ws_common = xmlrpclib.ServerProxy(args['url'] + '/xmlrpc/common')
uid = ws_common.login(args['database'], args['user'], args['password'])
print "Logged in to the common web service."
# Get the object proxy
ws_object = xmlrpclib.ServerProxy(args['url'] + '/xmlrpc/object')
print "Connected to the object web service."

# Find the parent location by name
res_ids = ws_object.execute(
    args['database'], uid, args['password'],
    'ir.module.module', 'search', [('name', '=', args['module'])])
if len(res_ids) != 1:
    raise Exception("Search failed")

# Uninstall the module
print "Uninstalling '%s'" % args['module']
ws_object.execute(
    args['database'], uid, args['password'],
    'ir.module.module', "button_immediate_uninstall", res_ids)

print "All done."

