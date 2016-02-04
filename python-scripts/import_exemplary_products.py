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

username = "admin"
pwd = "Passwort der DB"
dbname = "Datenbankname"
baseurl = "http://localhost:8069"

i = 1   #Zaehlvariable 

sock_common = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/common")

uid = sock_common.login(dbname, username, pwd)

sock = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/object")

data = open('csv/Exemplary_product_csv.csv')

lines = data.readlines()
number_of_lines = len(lines)-1
print "Anzahl Datensätze: ", number_of_lines
     
reader_data = open('csv/Exemplary_product_csv.csv')
 
reader = csv.reader(reader_data,delimiter=';') #delimiter bezeichnet das Trennzeichen der CSV-Datei

Kategorien = {}
Durchgang2 = []


next(reader)
for row in reader:
    ProductData = {
                   'name': row[1],                                  #Bezeichnung
                   'standart_price': row[7],                        #LetzterEK
                   'purchase_ok': False if row[6] == '0' else True, #IstBestellartikel
                   'sale_ok': False if row[7] == '0' else True,     #IstVerkaufsartikel
                   'active': True,
                   'state': 'sellable',
                   'taxes_id': [(6, 0, [12])],
                   'supplier_taxes_id': [(6, 0, [14])],
                   'lst_price': row[8],
                   'standard_price':  row[7],
                   }
    #Produktnummer
    if row[0] != '':
        ProductData['eq_default_code'] = row[0]
        ProductData['default_code'] = row[0]

    #Produktcategori
    if row[2] != '':
        Catag_id = sock.execute(dbname, uid, pwd, 'product.category', 'search', [('name', '=', row[2])])
        if len(Catag_id) != 0:
            ProductData['categ_id'] = Catag_id[0]
             
    ProductData['uom_id'] = 1
 
    Search = sock.execute(dbname, uid, pwd, 'product.template', 'search', [('name', '=', row[1])])
    if len(Search) == 0:
        pro_id = sock.execute(dbname, uid, pwd, 'product.template', 'create', ProductData)
        print str(i) + '/'+str(number_of_lines) + 'Artikel mit der Artikelnummer ' + row[0] + ' wurde erstellt.'
        i= i+1
    else:
        sock.execute(dbname, uid, pwd, 'product.template', 'write', Search, ProductData)
        pro_id = Search
        print str(i) + '/'+str(number_of_lines) + ' Artikel mit der Artikelnummer ' + row[0] + ' wurde bearbeitet.' 
        i= i+1
    
    #EAN
    if row[4] != '':
        try:
            EAN = {'ean13': row[4]}
            sock.execute(dbname, uid, pwd, 'product.template', 'write', pro_id, EAN)
        except:
            print 'Die EAN ' + row[4] + ' für das Produkt mit der Artikelnummer ' + row[0] + ' ist ungültig.'
            
        
print 'Fertig'