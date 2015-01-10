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

data = open('csv/Adresse_Ansprechpartner.csv', 'rb')

reader = csv.reader(data)

next(reader)
for row in reader:
    Partner = sock.execute(dbname, uid, pwd, 'res.partner', 'search', [('eq_custom01', '=', row[0])])
    if len(Partner):
        if row[6] != '' and row[6] != None:
            Partner = {         
                       'eq_firstname': row[5] if row[5] != None else False,
                       'name': row[6] if row[6] != None else False,
                       'function': row[7] if row[7] != None else False,
                       'phone': row[12] if row[12] != None else False,
                       'fax': row[13] if row[13] != None else False,
                       'mobile': row[14] if row[14] != None else False,
                       'email': row[17] if row[17] != None else False,
                       'street': row[21] if row[21] != None else False,
                       'zip': row[22] if row[22] != None else False,
                       'city': row[23] if row[23] != None else False,
                       'is_company': False,
                       }
            
            #Geburtstag
            try:
                if row[18] != None and row[18] != '':
                    Geburtstag = datetime.strptime(row[18], "%m/%d/%Y %H:%M")
                    Partner['eq_birthday'] = Geburtstag.strftime("%Y-%m-%d %H:%M")
            except:
                print 'Das Geburtsdatum des Ansprechpartners ' + row[0] + ' hat eine falsche Formatierung.'
            
            #Titel
            TitelId = sock.execute(dbname, uid, pwd, 'res.partner.title', 'search', [('name', '=', row[4])])
            if len(TitelId) == 1:
                Partner['title'] = TitelId[0]
            elif not TitelId: #Wenn der Tag nicht vorhanden ist, wird er erstellt und im Dictonary gespeichert.
                Partner['title'] = sock.execute(dbname, uid, pwd, 'res.partner.title', 'create', {'name': row[4]})
            
            #Land
            if row[24] != None:
                country = sock.execute(dbname, uid, pwd, 'res.country', 'search', [('code', '=', row[24])])
                if isinstance(country, list) and country != []:
                    Partner['country_id'] =  country[0]
                elif isinstance(country, int):
                    Partner['country_id'] =  country
                else:
                    Germany =  sock.execute(dbname, uid, pwd, 'res.country', 'search', [('code', '=', 'DE')])
                    if isinstance(Germany, list) and country != []:
                        Partner['country_id'] =  Germany[0]
                    elif isinstance(Germany, int):
                        Partner['country_id'] =  Germany
        
            
            #Gruppe/Tag
            CategoryID = sock.execute(dbname, uid, pwd, 'res.partner.category', 'search', [('name', '=', row[8])])
            if len(CategoryID) == 1:
                Partner['category_id'] = CategoryID
            elif not CategoryID: #Wenn der Tag nicht vorhanden ist, wird er erstellt und im Dictonary gespeichert.
                K = sock.execute(dbname, uid, pwd, 'res.partner.category', 'create', {'name': row[8]})
                Partner['category_id'] = K if isinstance(K, list) else [K]
            
            #VaterID/Bezug zur Adresse
            Vater_Id = sock.execute(dbname, uid, pwd, 'res.partner', 'search', [('eq_custom01', '=', row[1])])
            if isinstance(Vater_Id, list) and Vater_Id != []:
                Partner['parent_id'] = Vater_Id[0]
            elif isinstance(Vater_Id, int):
                Partner['parent_id'] = Vater_Id
            
            Kontakt_Id = sock.execute(dbname, uid, pwd, 'res.partner', 'search', ['&', '&', ('name', '=', row[6]), ('eq_firstname', '=', row[5]),  ('type', '=', 'contact')])
            
            if len(Kontakt_Id) == 0:      
                sock.execute(dbname, uid, pwd, 'res.partner', 'create', Partner)               
                print "Kontakt " + str(row[0]) + " wurde erfolgreich erstellt"     
            else:
                sock.execute(dbname, uid, pwd, 'res.partner', 'write', Kontakt_Id, Partner)               
                print "Kontakt " + str(row[0]) + " wurde erfolgreich bearbeitet"  
print 'Fertig!'