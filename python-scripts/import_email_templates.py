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

username = "user"
pwd = "pw"
dbname = "dbname"
baseurl = "localhost:8069"

version_number = 1

print "Email-Template Import wird gestartet..."

sock_common = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/common")

uid = sock_common.login(dbname, username, pwd)

sock = xmlrpclib.ServerProxy(baseurl + "/xmlrpc/object")

list_id = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("eq_email_template_version","=",0)])
#list_id = sock.execute(dbname, uid, pwd, 'email.template', 'search', ["|",("eq_email_template_version","=",0),("eq_email_template_version","<",version_number)])

dict = sock.execute(dbname, uid, pwd, 'email.template', 'read', list_id,['display_name'])

for i in dict:
    print 'Template "' + i['display_name'] + '" wurde geloescht'
    

    
#list_id = sock.execute(dbname, uid, pwd, 'email.template', 'search', [])
sock.execute(dbname, uid, pwd, 'email.template', 'unlink', list_id)


#############1. Sales Order - Send by Email_en #############
############################################################
template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Sales Order - Send by Email")])

sale_order_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search',[("model","=", "sale.order")])
sale_order_xml_id = sock.execute(dbname, uid, pwd, 'ir.actions.report.xml', 'search',[("model","=", "sale.order")])

if template_name == []:

    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Sales Order - Send by Email_en.txt","r")
    body_html = email_temp_file.read()
    

    Email_Template_en = {
        'name': 'Sales Order - Send by Email',
        'eq_email_template_version': version_number,
        'model_id': sale_order_model_id[0],
        'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Quotation' or 'Order'} (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_invoice_id.id}',
        'lang': '${object.partner_id.lang}',
       
        'auto_delete': True,
                            }     
       
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en,{})               
    print "Email-Template erstellt: Sales Order - Send by Email_en"
    
    ir_model_data ={
        'module': 'sale',
        'name':'email_template_edi_sale',
        'model':'email.template',
        'res_id': template_id,
                }
    
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)
    
    
#################2. Sales Order - Send by Email_de #############
################################################################
    
    
    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Sales Order - Send by Email_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Sales Order - Send by Email',
         'eq_email_template_version': version_number,
        'model_id': sale_order_model_id[0],
        'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Angebot' or 'Auftrag'} (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_invoice_id.id}',
        'lang': '${object.partner_id.lang}',
        
        'auto_delete': True,
                            }     
          
    sock.execute(dbname, uid, pwd, 'email.template', 'write',template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Sales Order - Send by Email_de"


#############3. Sales Order - Send by Email (Portal)_en #############
#####################################################################

template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Sales Order - Send by Email (Portal)")])

if template_name == []:

    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Sales Order - Send by Email (Portal)_en.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_en = {
        'name': 'Sales Order - Send by Email (Portal)',
        'eq_email_template_version': version_number,
        'model_id': sale_order_model_id[0],
        'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Quotation' or 'Order'} (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_invoice_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': sale_order_xml_id[0],
        'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
        'auto_delete': True,
                            }     
       
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})               
    print "Email-Template erstellt: Sales Order - Send by Email (Portal)_en"
    
    ir_model_data ={
        'module': 'portal_sale',
        'name':'email_template_edi_sale',
        'model':'email.template',
        'res_id': template_id,
                }
    
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)
    
##############4. Sales Order - Send by Email (Portal)_de #############
######################################################################
    
    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Sales Order - Send by Email (Portal)_de.txt","r")
    
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Sales Order - Send by Email (Portal)',
        'eq_email_template_version': version_number,
        'model_id': sale_order_model_id[0],
        'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Angebot' or 'Auftrag'} (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_invoice_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': sale_order_xml_id[0],
        'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
        'auto_delete': True,
                            }     
          
    sock.execute(dbname, uid, pwd, 'email.template', 'write',template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Sales Order - Send by Email (Portal)_de"


#############5. Sales Order - Send by Email (Online Quote)_en #############
###########################################################################

template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Sales Order - Send by Email (Online Quote)")])

if template_name == []:


    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Sales Order - Send by Email (Online Quote)_en.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_en = {
        'name': 'Sales Order - Send by Email (Online Quote)',
        'eq_email_template_version': version_number,
        'model_id': sale_order_model_id[0],
        'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Quotation' or 'Order'} (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_invoice_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': sale_order_xml_id[0],
        'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
    print "Email-Template erstellt: Sales Order - Send by Email (Online Quote)_en"
    
    ir_model_data ={
        'module': 'website_quote',
        'name':'email_template_edi_sale',
        'model':'email.template',
        'res_id': template_id,
                }
    
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)
    
##############6. Sales Order - Send by Email (Online Quote)_de #############
############################################################################
    
    
    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Sales Order - Send by Email (Online Quote)_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Sales Order - Send by Email (Online Quote)',
        'eq_email_template_version': version_number,
        'model_id': sale_order_model_id[0],
        'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Angebot' or 'Auftrag'} (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_invoice_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': sale_order_xml_id[0],
        'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Sales Order - Send by Email (Online Quote)_de"


#############7. Invoice - Send by Email en ################################
###########################################################################


invoice_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search',[("model","=", "account.invoice")])
invoice_xml_id = sock.execute(dbname, uid, pwd, 'ir.actions.report.xml', 'search',[("model","=", "account.invoice")])

template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Invoice - Send by Email")])

if template_name == []:

    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Invoice - Send by Email_en.txt","r")
    body_html = email_temp_file.read()
    
    Email_Template_en = {
        'name': 'Invoice - Send by Email',
        'eq_email_template_version': version_number,
        'model_id': invoice_model_id[0],
        'subject': "${object.company_id.name} Invoice (Ref ${object.number or 'n/a'})", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or object.company_id.email or 'noreply@localhost')|safe}",
        'partner_to': '${object.partner_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': invoice_xml_id[0],
        'report_name': "Invoice_${(object.number or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
    print "Email-Template erstellt: Invoice - Send by Email_en"
    
    ir_model_data ={
        'module': 'account',
        'name':'email_template_edi_invoice',
        'model':'email.template',
        'res_id': template_id,
                }
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data) 
    
    
##############8. Invoice - Send by Email de ################################
############################################################################
    
    
    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Invoice - Send by Email_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Invoice - Send by Email',
        'eq_email_template_version': version_number,
        'model_id': invoice_model_id[0],
        'subject': "${object.company_id.name|safe} Rechnung (Ref ${object.number or 'n/a'})", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or object.company_id.email or 'noreply@localhost')|safe}",
        'partner_to': '${object.partner_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': invoice_xml_id[0],
        'report_name': "Invoice_${(object.number or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Invoice - Send by Email_de"


#############9. Invoice - Send by Email (Portal) en ################################
###########################################################################

template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Invoice - Send by Email (Portal)")])

if template_name == []:

    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Invoice - Send by Email (Portal)_en.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_en = {
        'name': 'Invoice - Send by Email (Portal)',
        'eq_email_template_version': version_number,
        'model_id': invoice_model_id[0],
        'subject': "${object.company_id.name} Invoice (Ref ${object.number or 'n/a'})", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or object.company_id.email or 'noreply@localhost')|safe}",
        'partner_to': '${object.partner_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': invoice_xml_id[0],
        'report_name': "Invoice_${(object.number or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
    print "Email-Template erstellt: Invoice - Send by Email (Portal)_en"
    
    ir_model_data ={
        'module': 'portal_sale',
        'name':'email_template_edi_invoice',
        'model':'email.template',
        'res_id': template_id,
                }
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)
    
    
##############10. Invoice - Send by Email (Portal) de ################################
#####################################################################################
    
    
    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Invoice - Send by Email_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Invoice - Send by Email (Portal)',
        'eq_email_template_version': version_number,
        'model_id': invoice_model_id[0],
        'subject': "${object.company_id.name|safe} Rechnung (Ref ${object.number or 'n/a'})", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or object.company_id.email or 'noreply@localhost')|safe}",
        'partner_to': '${object.partner_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': invoice_xml_id[0],
        'report_name': "Invoice_${(object.number or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Invoice - Send by Email (Portal)_de"
    
    
#############11. RFQ - Send by Email en ###################################
###########################################################################


rfq_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search',[("model","=", "purchase.order")])
rfq_xml_id = sock.execute(dbname, uid, pwd, 'ir.actions.report.xml', 'search',[("report_file","=", "purchase.report_purchasequotation")])

template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","RFQ - Send by Email")])

if template_name == []:

    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/RFQ - Send by Email_en.txt","r")
    body_html = email_temp_file.read()
    
    Email_Template_en = {
        'name': 'RFQ - Send by Email',
        'eq_email_template_version': version_number,
        'model_id': rfq_model_id[0],
        'subject': "${object.company_id.name|safe} Order (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': rfq_xml_id[0],
        'report_name': "RFQ_${(object.name or '').replace('/','_')}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
    print "Email-Template erstellt: RFQ - Send by Email_en"
    
    ir_model_data ={
        'module': 'purchase',
        'name':'email_template_edi_purchase',
        'model':'email.template',
        'res_id': template_id,
                }
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data) 
    
    
##############12. RFQ - Send by Email de ###################################
############################################################################
    
    
    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/RFQ - Send by Email_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'RFQ - Send by Email',
        'eq_email_template_version': version_number,
        'model_id': rfq_model_id[0],
        'subject': "${object.company_id.name|safe} Bestellung (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': rfq_xml_id[0],
        'report_name': "RFQ_${(object.name or '').replace('/','_')}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: RFQ - Send by Email_de"


#############13. Purchase Order - Send by Email en ###################################
######################################################################################



purchase_xml_id = sock.execute(dbname, uid, pwd, 'ir.actions.report.xml', 'search',[("model","=", "purchase.order")])

template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Purchase Order - Send by Email")])

if template_name == []:

    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Purchase Order - Send by Email_en.txt","r")
    body_html = email_temp_file.read()
    
    Email_Template_en = {
        'name': 'Purchase Order - Send by Email',
        'eq_email_template_version': version_number,
        'model_id': rfq_model_id[0],
        'subject': "${object.company_id.name} Auftrag (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': purchase_xml_id[0],
        'report_name': "PO_${(object.name or '').replace('/','_')}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
    print "Email-Template erstellt: Purchase Order - Send by Email_en"
    
    ir_model_data ={
        'module': 'purchase',
        'name':'email_template_edi_purchase_done',
        'model':'email.template',
        'res_id': template_id,
                }
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data) 
    
    
##############14. Purchase Order - Send by Email de ###################################
#######################################################################################
    
    
    email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Purchase Order - Send by Email_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Purchase Order - Send by Email',
        'eq_email_template_version': version_number,
        'model_id': rfq_model_id[0],
        'subject': "${object.company_id.name} Auftrag (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': purchase_xml_id[0],
        'report_name': "PO_${(object.name or '').replace('/','_')}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Purchase Order - Send by Email_de"    

#############11. Lead/Opportunity Mass Mail en ################################
###########################################################################


# email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Lead Opportunity Mass Mail_en.txt","r")
# body_html = email_temp_file.read()
# 
# massmail_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search',[("model","=", "crm.lead.forward.to.partner")])
# massmail_xml_id = sock.execute(dbname, uid, pwd, 'ir.actions.report.xml', 'search',[("model","=", "crm.lead.forward.to.partner")])
# 
# Email_Template_en = {
#     'name': 'Lead/Opportunity Mass Mail',
#     'model_id': massmail_model_id[0],
#     'subject': "Fwd: Lead: ${ctx['partner_id'].name}", 
#     'body_html': body_html,
#     'email_from': "${(user.email or '')|safe}",
#     'email_to': "${ctx['partner_id'].email|safe}",
#     'auto_delete': True,
#                         }     
#       
# template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
# print "Email-Template erstellt: Lead/Opportunity Mass Mail en"


#############12. Lead/Opportunity Mass Mail de ################################
###########################################################################


# email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Lead Opportunity Mass Mail_de.txt","r")
# body_html = email_temp_file.read()
# 
# 
# Email_Template_de = {
#     'name': 'Lead/Opportunity Mass Mail',
#     'model_id': massmail_model_id[0],
#     'subject': "Fwd: Lead: ${ctx['partner_id'].name}", 
#     'body_html': body_html,
#     'email_from': "${(user.email or '')|safe}",
#     'email_to': "${ctx['partner_id'].email|safe}",
#     'auto_delete': True,
#                         }     
#       
# template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
# print "Email-Template erstellt:  Lead/Opportunity Mass Mail_de"


#############7. Odoo Enterprise Connection_en #############################
###########################################################################

# email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Odoo Enterprise Connection_en.txt","r")
# body_html = email_temp_file.read()
# 
# 
# Email_Template_en = {
#     'name': 'Odoo Enterprise Connection',
#     'model_id': int(92),
#     'subject': '${object.company_id.name} invitation to connect on Odoo', 
#     'body_html': body_html,
#     'email_from': '${object.company_id.name} <${(object.company_id.email or user.email)|safe}>',
#     'email_to' : '${object.email|safe}',
#     'lang': '${object.partner_id.lang}',
#     'auto_delete': True,
#                         }     
#       
# template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
# print "Email-Template erstellt: Odoo Enterprise Connection_en"


#############8. Odoo Enterprise Connection_de #############################
###########################################################################


# email_temp_file = open("/home/odoo/git/odoo-addons/equitania/email_templates/Odoo Enterprise Connection_de.txt","r")
# body_html = email_temp_file.read()
# 
# 
# Email_Template_de = {
#     'name': 'Odoo Enterprise Connection',
#     'model_id': int(92),
#     'subject': '${object.company_id.name} Einladung zur Registrierung auf unserem System', 
#     'body_html': body_html,
#     'email_from': '${object.company_id.name} <${(object.company_id.email or user.email)|safe}>',
#     'email_to' : '${object.email|safe}',
#     'lang': '${object.partner_id.lang}',
#     'auto_delete': True,
#                         }     
#       
# template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
# print "Email-Template erstellt: Odoo Enterprise Connection_de"

print "Email-Template Import wird beendet..."