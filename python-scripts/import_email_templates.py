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
from datetime import datetime, timedelta

username = "admin"
pwd = "odoo2015"
dbname = "dbname"
baseurl = "http://localhost:8069"

sock_common = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/common")

uid = sock_common.login(dbname, username, pwd)

sock = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/object")

list_id = sock.execute(dbname, uid, pwd, 'email.template', 'search', [])
sock.execute(dbname, uid, pwd, 'email.template', 'unlink', list_id)


#############1. Sales Order - Send by Email_en #############
############################################################


email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Sales Order - Send by Email_en.txt","r")
body_html = email_temp_file.read()


Email_Template_en = {
    'name': 'Sales Order - Send by Email',
    'model_id': int(555),
    'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Quotation' or 'Order'} (Ref ${object.name or 'n/a' })", 
    'body_html': body_html,
    'email_from': "${(object.user_id.email or '')|safe}",
    'partner_to': '${object.partner_invoice_id.id}',
    'lang': '${object.partner_id.lang}',
    'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
    'auto_delete': True,
                        }     
   
template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en,{})               
print "Email-Template erstellt: Sales Order - Send by Email_en"


#############2. Sales Order - Send by Email_de #############
############################################################


email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Sales Order - Send by Email_de.txt","r")
body_html = email_temp_file.read()


Email_Template_de = {
    'name': 'Sales Order - Send by Email',
    'model_id': int(555),
    'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Angebot' or 'Auftrag'} (Ref ${object.name or 'n/a' })", 
    'body_html': body_html,
    'email_from': "${(object.user_id.email or '')|safe}",
    'partner_to': '${object.partner_invoice_id.id}',
    'lang': '${object.partner_id.lang}',
    'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
    'auto_delete': True,
                        }     
      
sock.execute(dbname, uid, pwd, 'email.template', 'write',template_id, Email_Template_de,{'lang':'de_DE'})            
print "Email-Template erstellt: Sales Order - Send by Email_de"


#############3. Sales Order - Send by Email (Portal)_en #############
#####################################################################


email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Sales Order - Send by Email (Portal)_en.txt","r")
body_html = email_temp_file.read()


Email_Template_en = {
    'name': 'Sales Order - Send by Email (Portal)',
    'model_id': int(555),
    'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Quotation' or 'Order'} (Ref ${object.name or 'n/a' })", 
    'body_html': body_html,
    'email_from': "${(object.user_id.email or '')|safe}",
    'partner_to': '${object.partner_invoice_id.id}',
    'lang': '${object.partner_id.lang}',
    'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
    'auto_delete': True,
                        }     
   
template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})               
print "Email-Template erstellt: Sales Order - Send by Email (Portal)_en"


#############4. Sales Order - Send by Email (Portal)_de #############
#####################################################################

email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Sales Order - Send by Email (Portal)_de.txt","r")
body_html = email_temp_file.read()


Email_Template_de = {
    'name': 'Sales Order - Send by Email (Portal)',
    'model_id': int(555),
    'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Angebot' or 'Auftrag'} (Ref ${object.name or 'n/a' })", 
    'body_html': body_html,
    'email_from': "${(object.user_id.email or '')|safe}",
    'partner_to': '${object.partner_invoice_id.id}',
    'lang': '${object.partner_id.lang}',
    'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
    'auto_delete': True,
                        }     
      
sock.execute(dbname, uid, pwd, 'email.template', 'write',template_id, Email_Template_de,{'lang':'de_DE'})            
print "Email-Template erstellt: Sales Order - Send by Email (Portal)_de"


#############5. Sales Order - Send by Email (Online Quote)_en #############
###########################################################################


email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Sales Order - Send by Email (Online Quote)_en.txt","r")
body_html = email_temp_file.read()


Email_Template_en = {
    'name': 'Sales Order - Send by Email (Online Quote)',
    'model_id': int(555),
    'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Quotation' or 'Order'} (Ref ${object.name or 'n/a' })", 
    'body_html': body_html,
    'email_from': "${(object.user_id.email or '')|safe}",
    'partner_to': '${object.partner_invoice_id.id}',
    'lang': '${object.partner_id.lang}',
    'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
    'auto_delete': True,
                        }     
      
template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
print "Email-Template erstellt: Sales Order - Send by Email (Online Quote)_en"


#############6. Sales Order - Send by Email (Online Quote)_de #############
###########################################################################


email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Sales Order - Send by Email (Online Quote)_de.txt","r")
body_html = email_temp_file.read()


Email_Template_de = {
    'name': 'Sales Order - Send by Email (Online Quote)',
    'model_id': int(555),
    'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Angebot' or 'Auftrag'} (Ref ${object.name or 'n/a' })", 
    'body_html': body_html,
    'email_from': "${(object.user_id.email or '')|safe}",
    'partner_to': '${object.partner_invoice_id.id}',
    'lang': '${object.partner_id.lang}',
    'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
    'auto_delete': True,
                        }     
      
template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
print "Email-Template erstellt: Sales Order - Send by Email (Online Quote)_de"


#############7. Odoo Enterprise Connection_en #############################
###########################################################################

email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Odoo Enterprise Connection_en.txt","r")
body_html = email_temp_file.read()


Email_Template_en = {
    'name': 'Odoo Enterprise Connection',
    'model_id': int(92),
    'subject': '${object.company_id.name} invitation to connect on Odoo', 
    'body_html': body_html,
    'email_from': '${object.company_id.name} <${(object.company_id.email or user.email)|safe}>',
    'email_to' : '${object.email|safe}',
    'lang': '${object.partner_id.lang}',
    'auto_delete': True,
                        }     
      
template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
print "Email-Template erstellt: Odoo Enterprise Connection_en"


#############8. Odoo Enterprise Connection_de #############################
###########################################################################


email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Odoo Enterprise Connection_de.txt","r")
body_html = email_temp_file.read()


Email_Template_de = {
    'name': 'Odoo Enterprise Connection',
    'model_id': int(92),
    'subject': '${object.company_id.name} Einladung zur Registrierung auf unserem System', 
    'body_html': body_html,
    'email_from': '${object.company_id.name} <${(object.company_id.email or user.email)|safe}>',
    'email_to' : '${object.email|safe}',
    'lang': '${object.partner_id.lang}',
    'auto_delete': True,
                        }     
      
template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
print "Email-Template erstellt: Odoo Enterprise Connection_de"