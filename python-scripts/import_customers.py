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

data = open('csv/Adressen.csv', 'rb')

reader = csv.reader(data)

#Hilfvariablen zum verbinden des Kreditoren und Debitorendatensatzes
LastAddress = '0'
LastID = 0
NeedOtherInvoiceAddress = {}
Zahlungsbedingungen_id = 4

#Loop
next(reader)
for row in reader:
    Partner = sock.execute(dbname, uid, pwd, 'res.partner', 'search', ['|', ('eq_creditor_ref', '=', row[0][1:]), ('eq_customer_ref', '=', row[0][1:])])
    if len(Partner) == 0:
        if row[3] != LastAddress:
            PartnerDaten = {
                            'supplier': False,
                            'customer': False,
                            'is_company': True,
                            'eq_custom01': row[3],
                            }
            LastAddress = row[3]
                        
            #Debitoren- und Kreditorennummer
            if row[0][0] == "K":
                PartnerDaten['eq_creditor_ref'] =  row[0][1:]
                PartnerDaten['supplier'] =  True
            elif row[0][0] == "D":
                PartnerDaten['eq_customer_ref'] = row[0][1:]
                PartnerDaten['ref'] = row[0][1:]
                PartnerDaten['customer'] =  True
            """
            #EULand
            if row[6] != None and row[6] != '':
                if row[6] == 'AT': PartnerDaten['country_id'] = 13
                if row[6] == 'CZ': PartnerDaten['country_id'] = 57
                if row[6] == 'DK': PartnerDaten['country_id'] = 60
                if row[6] == 'EC': PartnerDaten['country_id'] = 64
                if row[6] == 'FR': PartnerDaten['country_id'] = 76
                if row[6] == 'GB': PartnerDaten['country_id'] = 233
                if row[6] == 'HU': PartnerDaten['country_id'] = 100
                if row[6] == 'IT': PartnerDaten['country_id'] = 110
                if row[6] == 'LU': PartnerDaten['country_id'] = 134
                if row[6] == 'NL': PartnerDaten['country_id'] = 160
                if row[6] == 'SI': PartnerDaten['country_id'] = 201
            """
            
            #Gruppe/Tag
            CategoryID = sock.execute(dbname, uid, pwd, 'res.partner.category', 'search', [('name', '=', row[10])])
            if len(CategoryID) == 1:
                PartnerDaten['category_id'] = CategoryID
            elif not CategoryID: #Wenn der Tag nicht vorhanden ist, wird er erstellt und im Dictonary gespeichert.
                PartnerDaten['category_id'] = sock.execute(dbname, uid, pwd, 'res.partner.category', 'create', {'name': row[10]})
            
            #Vertreter
            user_id = sock.execute(dbname, uid, pwd, 'res.users', 'search', [('eq_custom01', '=', row[11])])
            if len(user_id) != 0:
                PartnerDaten['user_id'] = user_id if isinstance(user_id, int) else user_id[0]

            #Letzter Umsatz
            if row[19] != None and row[19] != '':
                last_reconciliation_date = datetime.strptime(row[19], "%m/%d/%Y %H:%M")
                last_reconciliation_date.strftime("%Y-%m-%d %H:%M")

            #IstGesperrt
            if row[20] == "-1":
                PartnerDaten['sale_warn'] = 'block'
                PartnerDaten['sale_warn_msg'] = 'Der Kunde ist gesperrt'
                PartnerDaten['purchase_warn'] =  'block'
                PartnerDaten['purchase_warn_msg'] = 'Der Kunde ist gesperrt'
                PartnerDaten['picking_warn'] =  'block'
                PartnerDaten['picking_warn_msg'] = 'Der Kunde ist gesperrt'
                PartnerDaten['invoice_warn'] =  'block'
                PartnerDaten['invoice_warn_msg'] = 'Der Kunde ist gesperrt'

            #Preislist
            if row[22] != None and row[22] != '':
                Preislistenversion_id = sock.execute(dbname, uid, pwd, 'product.pricelist.version', 'search', [('eq_custom01', '=', row[22])])
                if len(Preislistenversion_id) != 0:
                    Preisliste = sock.execute(dbname, uid, pwd, 'product.pricelist.version', 'read', Preislistenversion_id)
                    PartnerDaten['property_product_pricelist'] = int(Preisliste[0]['pricelist_id'][0])
                else:
                    PartnerDaten['property_product_pricelist'] = 6

            #Kundenrabatt
            if row[25] != None and row[25] != '':
                PartnerDaten['eq_partner_disocunt'] =  row[25]
            """
            #Versandt
            if row[27] != None and row[27] != '':
            
            else:
            UPS eintragen!!!!
            """
            """
            #Lieferbedingungen
            if row[27] != None and row[19] != '':
                In der Kundenmaske nicht vorhanden
            """
            #Zahlungsbedingungen
            if row[8] != None and row[8] != '':
                PartnerDaten['property_payment_term'] =  Zahlungsbedingungen_id
                
            #Email
            if row[33] != None and row[33] != '':
                PartnerDaten['email'] =  row[33]
                
            #Gruppe
            if row[35] != None and row[35] != '':
                CategoryID = sock.execute(dbname, uid, pwd, 'res.partner.category', 'search', [('name', '=', row[35]),])
                if len(CategoryID) == 1:
                    PartnerDaten['category_id'] =  CategoryID
                elif not CategoryID: #Wenn der Tag nicht vorhanden ist, wird er erstellt und im Dictonary gespeichert.
                    list = []
                    list.append(sock.execute(dbname, uid, pwd, 'res.partner.category', 'create', {'name': row[35]}))
                    PartnerDaten['category_id'] =  list
                
            #Homepage
            if row[36] != None and row[36] != '':
                PartnerDaten['homepage'] =  row[36]
    
            #Memo
            if row[43] != None and row[43] != '':
                PartnerDaten['comment'] =  row[43]
                
            #Mobile
            if row[44] != None and row[44] != '':
                PartnerDaten['mobile'] =  row[44]
                
            #Name1
            if row[45] != None and row[45] != '':
                PartnerDaten['name'] =  row[45]
            """
            #Name2
            if row[46] != None and row[46] != '':
                PartnerDaten['eq_name2'] =  row[46]
            """
            #Postland. Fügt die Id des Landes ein, welches mit dem Code in der Odoo Datenbank übereinstimmte.
            if row[47] != None and row[47] != '':
                country = sock.execute(dbname, uid, pwd, 'res.country', 'search', [('code', '=', row[47])])
                if country != []:
                    PartnerDaten['country_id'] =  country[0]
                else:
                    PartnerDaten['country_id'] =  sock.execute(dbname, uid, pwd, 'res.country', 'search', [('code', '=', 'DE')])[0]
                    
            #PostOrt
            if row[48] != None and row[48] != '':
                PartnerDaten['city'] =  row[48]
                                     
            #PostPLZ
            if row[49] != None and row[49] != '':
                PartnerDaten['zip'] =  row[49]
                                     
            #PostStr
            if row[50] != None and row[50] != '':
                PartnerDaten['street'] =  row[50]
                                     
            #PostZusatz
            if row[51] != None and row[51] != '':
                PartnerDaten['street2'] =  row[51]
                
            id = sock.execute(dbname, uid, pwd, 'res.partner', 'create', PartnerDaten)
            print "Kunde " + str(row[3]) + " wurde erfolgreich erstellt"
            
            try:
                if row[7] != None and row[7] != '':
                    sock.execute(dbname, uid, pwd, 'res.partner', 'write', id, {'vat': row[7]})
            except:
                print 'Die UStID für den Kunden mit der Debitoren/Kreditorennummer ' + str(row[0][1:]) + ' konnte nicht erfasst werden.'
                pass
            
            LastID = id

            #Rechnungsempfänger
            if row[17] != row[0] and row[17] != None:
                NeedOtherInvoiceAddress[row[17]] =  (id, row)

            #Lieferadresse
            if row[38] != row[47] or row[39] != row[48] or row[40] != row[49] or row[41] != row[50] or row[42] != row[49]:
                
                LA = sock.execute(dbname, uid, pwd, 'res.partner', 'search', ['&', ('name', '=', row[45]), ('type', '=', 'delivery')])
                #Lieferland.
                Lieferadresse = {
                            'customer': PartnerDaten['customer'],
                            'supplier': PartnerDaten['supplier'],
                            'customer': False,
                            }
                country = sock.execute(dbname, uid, pwd, 'res.country', 'search', [('code', '=', row[38])])
                if len(country) != 0:
                    Lieferadresse['country_id'] =  country[0]
                elif isinstance(country, int):
                    Lieferadresse['country_id'] =  country
                else:
                    Germany =  sock.execute(dbname, uid, pwd, 'res.country', 'search', [('code', '=', 'DE')])
                    if country != []:
                        if isinstance(Germany, list):
                            Lieferadresse['country_id'] =  Germany[0]
                    elif isinstance(Germany, int):
                        Lieferadresse['country_id'] =  Germany
                        
                #Name 
                Lieferadresse['name'] =  row[45]
                
                #Lieferort
                if row[39] != None and row[39] != '':
                    Lieferadresse['city'] =  row[39]
                                         
                #LieferPLZ
                if row[40] != None and row[40] != '':
                    Lieferadresse['zip'] =  row[40]
                                         
                #LieferStr
                if row[41] != None and row[41] != '':
                    Lieferadresse['street'] =  row[41]
                                         
                #LieferZusatz
                if row[42] != None and row[42] != '':
                    Lieferadresse['street2'] =  row[42]
                    
                #VaterKontakt
                Lieferadresse['parent_id'] = id if isinstance(id, int) else id[0]
                
                #Typ Lieferadresse
                Lieferadresse['type'] = 'delivery'
                if len(LA) == 0:      
                    sock.execute(dbname, uid, pwd, 'res.partner', 'create', Lieferadresse)               
                    print "Lieferadresse für Kunde " + str(row[3]) + " wurde erfolgreich erstellt"     
                else:
                    sock.execute(dbname, uid, pwd, 'res.partner', 'write', LA, Lieferadresse)               
                    print "Lieferadresse für Kunde " + str(row[3]) + " wurde erfolgreich bearbeitet"                 
        else:
            #Debitoren- und Kreditorennummer
            if row[0][0] == "K":
                id = sock.execute(dbname, uid, pwd, 'res.partner', 'write', LastID, {'supplier': True, 'eq_creditor_ref': row[0][1:]})
            elif row[0][0] == "D":
                id = sock.execute(dbname, uid, pwd, 'res.partner', 'write', LastID, {'customer': True, 'eq_customer_ref': row[0][1:]})               
            print "Kunde " + str(row[3]) + " wurde erfolgreich bearbeitet"
                    
    else:        
        if row[3] != LastAddress:
            PartnerDaten = {
                            'is_company': True,
                            'eq_custom01': row[3],
                            }
            Lastaddress = row[3]
            
            #Debitoren- und Kreditorennummer
            if row[0][0] == "K":
                PartnerDaten['eq_creditor_ref'] =  row[0][1:]
                PartnerDaten['supplier'] =  True
            elif row[0][0] == "D":
                PartnerDaten['eq_customer_ref'] =  row[0][1:]
                PartnerDaten['ref'] = row[0][1:]
                PartnerDaten['customer'] =  True
            """
            #EULand
            if row[6] != None and row[6] != '':
                if row[6] == 'AT': PartnerDaten['country_id'] = 13
                if row[6] == 'CZ': PartnerDaten['country_id'] = 57
                if row[6] == 'DK': PartnerDaten['country_id'] = 60
                if row[6] == 'EC': PartnerDaten['country_id'] = 64
                if row[6] == 'FR': PartnerDaten['country_id'] = 76
                if row[6] == 'GB': PartnerDaten['country_id'] = 233
                if row[6] == 'HU': PartnerDaten['country_id'] = 100
                if row[6] == 'IT': PartnerDaten['country_id'] = 110
                if row[6] == 'LU': PartnerDaten['country_id'] = 134
                if row[6] == 'NL': PartnerDaten['country_id'] = 160
                if row[6] == 'SI': PartnerDaten['country_id'] = 201
            """            
            #Gruppe/Tag
            CategoryID = sock.execute(dbname, uid, pwd, 'res.partner.category', 'search', [('name', '=', row[10])])
            if len(CategoryID) == 1:
                PartnerDaten['category_id'] =  CategoryID
            elif not CategoryID: #Wenn der Tag nicht vorhanden ist, wird er erstellt und im Dictonary gespeichert.
                PartnerDaten['category_id'] =  sock.execute(dbname, uid, pwd, 'res.partner.category', 'create', {'name': row[10]})

            #Vertreter
            user_id = sock.execute(dbname, uid, pwd, 'res.users', 'search', [('eq_custom01', '=', row[11])])
            if len(user_id) != 0:
                PartnerDaten['user_id'] = user_id if isinstance(user_id, int) else user_id[0]
            
            #Letzter Umsatz
            if row[19] != None and row[19] != '':
                last_reconciliation_date = datetime.strptime(row[19], "%m/%d/%Y %H:%M")
                last_reconciliation_date.strftime("%Y-%m-%d %H:%M")
                
            #IstGesperrt
            if row[20] == "-1":
                PartnerDaten['sale_warn'] = 'block'
                PartnerDaten['sale_warn_msg'] = 'Der Kunde ist gesperrt'
                PartnerDaten['purchase_warn'] =  'block'
                PartnerDaten['purchase_warn_msg'] = 'Der Kunde ist gesperrt'
                PartnerDaten['picking_warn'] =  'block'
                PartnerDaten['picking_warn_msg'] = 'Der Kunde ist gesperrt'
                PartnerDaten['invoice_warn'] =  'block'
                PartnerDaten['invoice_warn_msg'] = 'Der Kunde ist gesperrt'
                
            #Preislist
            if row[22] != None and row[22] != '':
                Preislistenversion_id = sock.execute(dbname, uid, pwd, 'product.pricelist.version', 'search', [('eq_custom01', '=', row[22])])
                if len(Preislistenversion_id) != 0:
                    Preisliste = sock.execute(dbname, uid, pwd, 'product.pricelist.version', 'read', Preislistenversion_id)
                    PartnerDaten['property_product_pricelist'] = int(Preisliste[0]['pricelist_id'][0])
                else:
                    PartnerDaten['property_product_pricelist'] = 6
                
            #Kundenrabatt
            if row[25] != None and row[25] != '':
                PartnerDaten['eq_partner_disocunt'] =  row[25]
            """
            #Versandt
            if row[27] != None and row[27] != '':
            
            else:
            UPS eintragen!!!!
            """
            """
            #Lieferbedingungen
            if row[27] != None and row[27] != '':
                In der Kundenmaske nicht vorhanden
            """
            #Zahlungsbedingungen
            if row[8] != None and row[8] != '':
                PartnerDaten['property_payment_term'] =  Zahlungsbedingungen_id
                
            #Email
            if row[33] != None and row[33] != '':
                PartnerDaten['email'] =  row[33]
                
            #Gruppe
            if row[35] != None and row[35] != '':
                CategoryID = sock.execute(dbname, uid, pwd, 'res.partner.category', 'search', [('name', '=', row[35])])
                if len(CategoryID) == 1:
                    PartnerDaten['category_id'] =  CategoryID
                elif not CategoryID: #Wenn der Tag nicht vorhanden ist, wird er erstellt und im Dictonary gespeichert.
                    K = sock.execute(dbname, uid, pwd, 'res.partner.category', 'create', {'name': row[35]})
                    PartnerDaten['category_id'] =  K if isinstance(K, int) else K[0]
                
            #Homepage
            if row[36] != None and row[36] != '':
                PartnerDaten['homepage'] =  row[36]
    
            #Memo
            if row[43] != None and row[43] != '':
                PartnerDaten['comment'] =  row[43]
                
            #Mobile
            if row[44] != None and row[44] != '':
                PartnerDaten['mobile'] =  row[44]
                
            #Name1
            if row[45] != None and row[45] != '':
                PartnerDaten['name'] =  row[45]
            """
            #Name2
            if row[46] != None and row[46] != '':
                PartnerDaten['eq_name2'] =  row[46]
            """
            #Postland. Fügt die Id des Landes ein, welches mit dem Code in der Odoo Datenbank übereinstimmte.
            if row[47] != None and row[47] != '':
                country = sock.execute(dbname, uid, pwd, 'res.country', 'search', [('code', '=', row[47])])
                if country != []:
                    PartnerDaten['country_id'] =  country[0]
                elif isinstance(country, int):
                    PartnerDaten['country_id'] =  country
                else:
                    Germany =  sock.execute(dbname, uid, pwd, 'res.country', 'search', [('code', '=', 'DE')])
                    if isinstance(Germany, list) and country != []:
                        PartnerDaten['country_id'] =  Germany[0]
                    elif isinstance(Germany, int):
                        PartnerDaten['country_id'] =  Germany
                
            #PostOrt
            if row[48] != None and row[48] != '':
                PartnerDaten['city'] =  row[48]
                                     
            #PostPLZ
            if row[49] != None and row[49] != '':
                PartnerDaten['zip'] =  row[49]
                                     
            #PostStr
            if row[50] != None and row[50] != '':
                PartnerDaten['street'] =  row[50]
                                     
            #PostZusatz
            if row[51] != None and row[51] != '':
                PartnerDaten['street2'] =  row[51]
                
            id = sock.execute(dbname, uid, pwd, 'res.partner', 'write', Partner[0],  PartnerDaten)                                   
            print "Kunde " + str(row[3]) + " wurde erfolgreich erstellt"
            #EUUStID
            try:
                if row[7] != None:
                    sock.execute(dbname, uid, pwd, 'res.partner', 'write', id, {'vat': row[7]})
            except:
                print 'Die UStID für den Kunden mit der Debitoren/Kreditorennummer ' + str(row[0][1:]) + ' konnte nicht erfasst werden.'
                pass
            
            LastID = id

            #Rechnungsempfänger
            if row[17] != row[0] and row[17] != None:
                NeedOtherInvoiceAddress[row[17]] =  (Partner, row)

            #Lieferadresse
            if row[38] != row[47] or row[39] != row[48] or row[40] != row[49] or row[41] != row[50] or row[42] != row[49]:
                
                LA = sock.execute(dbname, uid, pwd, 'res.partner', 'search', ['&', ('name', '=', row[45]), ('type', '=', 'delivery')])
                
                #Lieferland.
                Lieferadresse = {
                            'supplier': False,
                            'customer': False,
                            }
                country = sock.execute(dbname, uid, pwd, 'res.country', 'search', [('code', '=', row[38])])
                if len(country) != 0:
                    Lieferadresse['country_id'] =  country[0]
                elif isinstance(country, int):
                    Lieferadresse['country_id'] =  country
                else:
                    Germany =  sock.execute(dbname, uid, pwd, 'res.country', 'search', [('code', '=', 'DE')])
                    if country != []:
                        if isinstance(Germany, list):
                            Lieferadresse['country_id'] =  Germany[0]
                    elif isinstance(Germany, int):
                        Lieferadresse['country_id'] =  Germany
                                               
                #Name 
                Lieferadresse['name'] =  row[45]
                
                #Lieferort
                if row[39] != None and row[39] != '':
                    Lieferadresse['city'] =  row[39]
                                         
                #LieferPLZ
                if row[40] != None and row[40] != '':
                    Lieferadresse['zip'] =  row[40]
                                         
                #LieferStr
                if row[41] != None and row[41] != '':
                    Lieferadresse['street'] =  row[41]
                                         
                #LieferZusatz
                if row[42] != None and row[42] != '':
                    Lieferadresse['street2'] =  row[42]
                    
                #VaterKontakt
                Lieferadresse['parent_id'] = Partner[0]
                
                #Typ Lieferadresse
                Lieferadresse['type'] = 'delivery'
                
                
                if len(LA) == 0:      
                    sock.execute(dbname, uid, pwd, 'res.partner', 'create', Lieferadresse)               
                    print "Lieferadresse für Kunde " + str(row[3]) + " wurde erfolgreich erstellt"     
                else:
                    sock.execute(dbname, uid, pwd, 'res.partner', 'write', LA, Lieferadresse)               
                    print "Lieferadresse für Kunde " + str(row[3]) + " wurde erfolgreich bearbeitet"  
        else:
            #Debitoren- und Kreditorennummer
            if row[0][0] == "K":
                id = sock.execute(dbname, uid, pwd, 'res.partner', 'write', LastID, {'supplier': True, 'eq_creditor_ref': row[0][1:]})
            elif row[0][0] == "D":
                id = sock.execute(dbname, uid, pwd, 'res.partner', 'write', LastID, {'customer': True, 'eq_customer_ref': row[0][1:]})                       
            print "Kunde " + str(row[3]) + " wurde erfolgreich bearbeitet"

data.close()
data = open('csv/Adressen.csv', 'rb')

reader = csv.reader(data)

for row in reader:
    if row[0] in NeedOtherInvoiceAddress:
        RA = sock.execute(dbname, uid, pwd, 'res.partner', 'search', ['&', '&', ('name', '=', row[45]), ('type', '=', 'invoice'), ('parent_id', '=', NeedOtherInvoiceAddress[row[0]][0])])
        
        Rechnungsadresse = {
                          'type': 'invoice',
                          'name': row[45],
                          'city': row[39],
                          'zip': row[40],
                          'street': row[41],
                          'street2': row[42],
                          'parent_id': NeedOtherInvoiceAddress[row[0]][0]if isinstance(NeedOtherInvoiceAddress[row[0]][0], int) else NeedOtherInvoiceAddress[row[0]][0][0] or NeedOtherInvoiceAddress[row[0]][0],                          
                          'supplier': False,
                          'customer': False,
                          }        
        if len(RA) == 0:      
            sock.execute(dbname, uid, pwd, 'res.partner', 'create', Rechnungsadresse)               
            print "Rechnungsadresse für Kunde " + str(row[3]) + " wurde erfolgreich erstellt"     
        else:
            sock.execute(dbname, uid, pwd, 'res.partner', 'write', RA, Rechnungsadresse)               
            print "Rechnungsadresse für Kunde " + str(row[3]) + " wurde erfolgreich bearbeitet"  
data.close()
print 'Fertig'

