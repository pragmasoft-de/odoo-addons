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
 
username = "admin"
pwd = "Passwort der DB"
dbname = "Datenbankname"
baseurl = "http://localhost:8069"

i = 1   #Zaehlvariable 
 
sock_common = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/common")
 
uid = sock_common.login(dbname, username, pwd)
 
sock = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/object")
 
data = open('csv/Exemplary_customer_csv.csv')

lines = data.readlines()
number_of_lines = len(lines)-1
print "Anzahl Datensätze: ", number_of_lines
    
reader_data = open('csv/Exemplary_customer_csv.csv')
 
reader = csv.reader(reader_data,delimiter=',') #delimiter bezeichnet das Trennzeichen der CSV-Datei

next(reader)
for row in reader:
     
    country_id = sock.execute(dbname, uid, pwd, 'res.country', 'search', [('code', '=', row[15])]) 
      
    partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search', [('eq_customer_ref', '=', row[1])])
      
    default_account_id = sock.execute(dbname, uid, pwd, 'account.account', 'search', [('code', '=', '10000')])
    default_account_id = default_account_id[0]       
    default_tag_id = sock.execute(dbname, uid, pwd, 'res.partner.category', 'search', [('name', '=', row[17])])

      
    partner_data = {}
                     
    #Land
    if country_id:
        partner_data['country_id'] = country_id[0]
      
    #Ist Unternehmen
    if row[0] == 'WAHR':
        partner_data['is_company'] = True
          
    if row[0] == 'FALSCH':
        partner_data['is_company'] = False
      
    #Kundennummer 
    if row[1] != None and row[1] != "":
         partner_data['eq_customer_ref'] = row[1]   
           
    #Brief Begrüßung
    if row[2] != None and row[2] != "":
         partner_data['eq_letter_salutation'] = row[2]   
           
    #Vorname
    if row[4] != None and row[4] != "":
         partner_data['eq_firstname'] = row[4]
           
    #Name2
    if row[5] != None and row[5] != "":
         partner_data['eq_name2'] = row[5]
           
    #Name
    if row[3] != None:
         partner_data['name'] = row[3]
           
           
    if row[3] in [' ',''] and row[5] != ' ':
         partner_data['name'] = row[5]
         partner_data['eq_name2']  = False  
           
    #Funktion
    if row[6] != None and row[6] != "":
         partner_data['function'] = row[6]
      
    #Street
    if row[7] != None and row[7] != "":
         partner_data['street'] = row[7]
           
    #Hausnummer
    if row[8] != None and row[8] != "":
         partner_data['eq_house_no'] = row[8]
           
    #PLZ
    if row[9] != None and row[9] != "":
         partner_data['zip'] = row[9]
           
    #Ort
    if row[10] != None and row[10] != "":
         partner_data['city'] = row[10]
           
    #Telefon
    if row[11] != None and row[11] != "" and row[11] != '0':
         partner_data['phone'] = row[11]
           
    #Mobil
    if row[12] != None and row[12] != "":
         partner_data['mobil'] = row[12]
           
    #Fax
    if row[13] != None and row[13] != "" and row[13] != '0':
         partner_data['fax'] = row[13]
           
    #Email
    if row[14] != None and row[14] != "":
         partner_data['email'] = row[14]
          
#-----------------------------Debitorenkonten------------------------------------------------
  
    default_account_data = sock.execute(dbname, uid, pwd, 'account.account', 'read', default_account_id)
    account_data ={
                    'active': True,
                    'reconcile': True,
                    'code': partner_data['eq_customer_ref'],
                    'name': partner_data['name'],
                    'parent_id':default_account_data['parent_id'][0],
                    'type':default_account_data['type'],
                     'user_type':default_account_data['user_type'][0],
                   }
       
    account_id_search = sock.execute(dbname, uid, pwd, 'account.account', 'search', [('code', '=', partner_data['eq_customer_ref'])])
    account_id = False
    if len(account_id_search) == 0:
        account_id = sock.execute(dbname, uid, pwd, 'account.account', 'create', account_data)
    else:
        account_id = account_id_search[0]
    
    partner_data['property_account_receivable'] = account_id
 
#------------------------------------------------------------------------------------------------        
#-----------------------------Zahlungsbedingungen------------------------------------------------        
    payment_data ={
                    'name': row[16],
                    'active': True,
                    'note': row[16],
                      
                   }
    payment_name_mapping = {
                            'Sofortige Zahlung' : 'Immediate Payment',
                            '15 Tage' : '15 Days',
                            '30 Tage netto' :  '30 Net Days',
                            '30 Tage zum Monatsende' : '30 Days end of Month',
                            '30% Anzahlung, Rest in 30 Tagen' : '30% Advance End 30 Days',                            
                            } 
     
    Payment_Name = row[16] 
     
    if Payment_Name in payment_name_mapping:
        payment_id_search = sock.execute(dbname, uid, pwd, 'account.payment.term', 'search', [('name', '=', payment_name_mapping[row[16]])])
        if len(payment_id_search) == 0:
            payment_id = sock.execute(dbname, uid, pwd, 'account.payment.term', 'create', payment_data)
        else:
            payment_id = payment_id_search[0]
    else:
        payment_id = sock.execute(dbname, uid, pwd, 'account.payment.term', 'create', payment_data)
    
    partner_data['property_payment_term'] = payment_id
#-----------------------------------------------------------------------------------------    
   
#---------------------------Schlagwoerter--------------------------------------------------   
    Category_id = False
    category_name_mapping = {
                            'Beratungsleistungen' : 'Consultancy Services',
                            'Mitarbeiter' : 'Employee',
                            'Komponenten-Käufer' : 'Components-Buyer',                                                       
                            }
     
    Category_Name = row[17]
     
    if Category_Name in category_name_mapping:
        Category_id = sock.execute(dbname, uid, pwd, 'res.partner.category', 'search', [('name', '=', category_name_mapping[row[17]])])
        if len(Category_id) == 1:
            Category_id = Category_id[0]
        else: #Wenn der Tag nicht vorhanden ist, wird er erstellt und im Dictonary gespeichert.
            Category_id = sock.execute(dbname, uid, pwd, 'res.partner.category', 'create', {'name': row[17]})
    else:
        Category_id = sock.execute(dbname, uid, pwd, 'res.partner.category', 'create', {'name': row[17]})
     
     
         
    partner_data['category_id'] = [(6, 0, [Category_id])]
     
#------------------------------------------------------------------------------------------
  
    if len(partner_id) == 0:
        partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'create', partner_data)
        print str(i) + '/'+ str(number_of_lines) +' Kunde importiert:', partner_data['name']
        i= i+1
    else:
        partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'write', partner_id[0], partner_data)
        print str(i) + '/'+ str(number_of_lines) +' Kunde aktualisiert:', partner_data['name']
        i= i+1
         
print 'Fertig!'
