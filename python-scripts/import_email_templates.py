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
import xmlrpclib, os
from datetime import datetime, timedelta

username = "admin"
pwd = "odoo"
dbname = "testmyodoo"
baseurl = "http://localhost:8069"

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

mypath = os.getcwd()
print mypath

#############1. Sales Order - Send by Email_en #############
############################################################
template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Sales Order - Send by Email")])
template_name_de = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Verkaufsauftrag")])

sale_order_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search',[("model","=", "sale.order")])
sale_order_xml_id = sock.execute(dbname, uid, pwd, 'ir.actions.report.xml', 'search',[("model","=", "sale.order")])

if template_name == [] and template_name_de == []:
    email_temp_file = open(mypath + "/email_templates/sales_order_send_by_email_en.txt","r")
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
        'report_template': sale_order_xml_id[0],
        'report_name': "SO_${(object.name or '').replace('/','_')}${object.state == 'draft' and 'draft' or ''}",
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
    
    
    email_temp_file = open(mypath + "/email_templates/sales_order_send_by_email_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Verkaufsauftrag',
         'eq_email_template_version': version_number,
        'model_id': sale_order_model_id[0],
        'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Angebot' or 'Auftrag'} (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_invoice_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': sale_order_xml_id[0],
        'report_name': "Verkaufsauftrag_${(object.name or '').replace('/','_')}${object.state == 'draft' and 'draft' or ''}",
        'auto_delete': True,
                            }     
          
    sock.execute(dbname, uid, pwd, 'email.template', 'write',template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Sales Order - Send by Email_de"


#############3. Sales Order - Send by Email (Portal)_en #############
#####################################################################
# 
# template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Sales Order - Send by Email (Portal)")])
# 
# if template_name == []:
# 
#     email_temp_file = open(mypath + "/email_templates/sales_order_send_by_email_portal_en.txt","r")
#     body_html = email_temp_file.read()
#     
#     
#     Email_Template_en = {
#         'name': 'Sales Order - Send by Email (Portal)',
#         'eq_email_template_version': version_number,
#         'model_id': sale_order_model_id[0],
#         'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Quotation' or 'Order'} (Ref ${object.name or 'n/a' })", 
#         'body_html': body_html,
#         'email_from': "${(object.user_id.email or '')|safe}",
#         'partner_to': '${object.partner_invoice_id.id}',
#         'lang': '${object.partner_id.lang}',
#         'report_template': sale_order_xml_id[0],
#         'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
#         'auto_delete': True,
#                             }     
#        
#     template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})               
#     print "Email-Template erstellt: Sales Order - Send by Email (Portal)_en"
#     
#     ir_model_data ={
#         'module': 'portal_sale',
#         'name':'email_template_edi_sale',
#         'model':'email.template',
#         'res_id': template_id,
#                 }
#     
#     identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)
#     
##############4. Sales Order - Send by Email (Portal)_de #############
######################################################################
#     
#     email_temp_file = open(mypath + "/email_templates/sales_order_send_by_email_portal_de.txt","r")
#     
#     body_html = email_temp_file.read()
#     
#     
#     Email_Template_de = {
#         'name': 'Sales Order - Send by Email (Portal)',
#         'eq_email_template_version': version_number,
#         'model_id': sale_order_model_id[0],
#         'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Angebot' or 'Auftrag'} (Ref ${object.name or 'n/a' })", 
#         'body_html': body_html,
#         'email_from': "${(object.user_id.email or '')|safe}",
#         'partner_to': '${object.partner_invoice_id.id}',
#         'lang': '${object.partner_id.lang}',
#         'report_template': sale_order_xml_id[0],
#         'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
#         'auto_delete': True,
#                             }     
#           
#     sock.execute(dbname, uid, pwd, 'email.template', 'write',template_id, Email_Template_de,{'lang':'de_DE'})            
#     print "Email-Template erstellt: Sales Order - Send by Email (Portal)_de"
#
#
#############5. Sales Order - Send by Email (Online Quote)_en #############
###########################################################################
# 
# template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Sales Order - Send by Email (Online Quote)")])
# 
# if template_name == []:
# 
# 
#     email_temp_file = open(mypath + "/email_templates/sales_order_send_by_email_online_quote_en.txt","r")
#     body_html = email_temp_file.read()
#     
#     
#     Email_Template_en = {
#         'name': 'Sales Order - Send by Email (Online Quote)',
#         'eq_email_template_version': version_number,
#         'model_id': sale_order_model_id[0],
#         'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Quotation' or 'Order'} (Ref ${object.name or 'n/a' })", 
#         'body_html': body_html,
#         'email_from': "${(object.user_id.email or '')|safe}",
#         'partner_to': '${object.partner_invoice_id.id}',
#         'lang': '${object.partner_id.lang}',
#         'report_template': sale_order_xml_id[0],
#         'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
#         'auto_delete': True,
#                             }     
#           
#     template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
#     print "Email-Template erstellt: Sales Order - Send by Email (Online Quote)_en"
#     
#     ir_model_data ={
#         'module': 'website_quote',
#         'name':'email_template_edi_sale',
#         'model':'email.template',
#         'res_id': template_id,
#                 }
#     
#     identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)
#     
##############6. Sales Order - Send by Email (Online Quote)_de #############
############################################################################
#     
#     
#     email_temp_file = open(mypath + "/email_templates/sales_order_send_by_email_online_quote_de.txt","r")
#     body_html = email_temp_file.read()
#     
#     
#     Email_Template_de = {
#         'name': 'Sales Order - Send by Email (Online Quote)',
#         'eq_email_template_version': version_number,
#         'model_id': sale_order_model_id[0],
#         'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Angebot' or 'Auftrag'} (Ref ${object.name or 'n/a' })", 
#         'body_html': body_html,
#         'email_from': "${(object.user_id.email or '')|safe}",
#         'partner_to': '${object.partner_invoice_id.id}',
#         'lang': '${object.partner_id.lang}',
#         'report_template': sale_order_xml_id[0],
#         'report_name': "${(object.name or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
#         'auto_delete': True,
#                             }     
#           
#     template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
#     print "Email-Template erstellt: Sales Order - Send by Email (Online Quote)_de"
#
#
#############7. Invoice - Send by Email en ################################
###########################################################################


invoice_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search',[("model","=", "account.invoice")])
invoice_xml_id = sock.execute(dbname, uid, pwd, 'ir.actions.report.xml', 'search',[("model","=", "account.invoice")])

template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Invoice - Send by Email")])
template_name_de = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Rechnung")])

if template_name == [] and template_name_de == []:

    email_temp_file = open(mypath + "/email_templates/invoice_send_by_email_en.txt","r")
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
        'report_name': "Invoice_${(object.number or '').replace('/','_')}${object.state == 'draft' and 'draft' or ''}",
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
    
    
    email_temp_file = open(mypath + "/email_templates/invoice_send_by_email_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Rechnung',
        'eq_email_template_version': version_number,
        'model_id': invoice_model_id[0],
        'subject': "${object.company_id.name|safe} Rechnung (Ref ${object.number or 'n/a'})", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or object.company_id.email or 'noreply@localhost')|safe}",
        'partner_to': '${object.partner_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': invoice_xml_id[0],
        'report_name': "Rechnung_${(object.number or '').replace('/','_')}${object.state == 'draft' and 'draft' or ''}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Invoice - Send by Email_de"


#############9. Invoice - Send by Email (Portal) en ################################
###########################################################################
# 
# template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Invoice - Send by Email (Portal)")])
# 
# if template_name == []:
# 
#     email_temp_file = open(mypath + "/email_templates/invoice_send_by_email_portal_en.txt","r")
#     body_html = email_temp_file.read()
#     
#     
#     Email_Template_en = {
#         'name': 'Invoice - Send by Email (Portal)',
#         'eq_email_template_version': version_number,
#         'model_id': invoice_model_id[0],
#         'subject': "${object.company_id.name} Invoice (Ref ${object.number or 'n/a'})", 
#         'body_html': body_html,
#         'email_from': "${(object.user_id.email or object.company_id.email or 'noreply@localhost')|safe}",
#         'partner_to': '${object.partner_id.id}',
#         'lang': '${object.partner_id.lang}',
#         'report_template': invoice_xml_id[0],
#         'report_name': "Invoice_${(object.number or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
#         'auto_delete': True,
#                             }     
#           
#     template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
#     print "Email-Template erstellt: Invoice - Send by Email (Portal)_en"
#     
#     ir_model_data ={
#         'module': 'portal_sale',
#         'name':'email_template_edi_invoice',
#         'model':'email.template',
#         'res_id': template_id,
#                 }
#     identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)
#     
#     
##############10. Invoice - Send by Email (Portal) de ################################
#####################################################################################
#     
#     
#     email_temp_file = open(mypath + "/email_templates/invoice_send_by_email_de.txt","r")
#     body_html = email_temp_file.read()
#     
#     
#     Email_Template_de = {
#         'name': 'Invoice - Send by Email (Portal)',
#         'eq_email_template_version': version_number,
#         'model_id': invoice_model_id[0],
#         'subject': "${object.company_id.name|safe} Rechnung (Ref ${object.number or 'n/a'})", 
#         'body_html': body_html,
#         'email_from': "${(object.user_id.email or object.company_id.email or 'noreply@localhost')|safe}",
#         'partner_to': '${object.partner_id.id}',
#         'lang': '${object.partner_id.lang}',
#         'report_template': invoice_xml_id[0],
#         'report_name': "Invoice_${(object.number or '').replace('/','_')}_${object.state == 'draft' and 'draft' or ''}",
#         'auto_delete': True,
#                             }     
#           
#     template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
#     print "Email-Template erstellt: Invoice - Send by Email (Portal)_de"
#     
#     
#############11. RFQ - Send by Email en ###################################
###########################################################################


rfq_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search',[("model","=", "purchase.order")])
rfq_xml_id = sock.execute(dbname, uid, pwd, 'ir.actions.report.xml', 'search',[("report_file","=", "purchase.report_purchasequotation")])

template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","RFQ - Send by Email")])
template_name_de = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Angebotsanfrage")])

if template_name == [] and template_name_de == []:

    email_temp_file = open(mypath + "/email_templates/rfq_send_by_email_en.txt","r")
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
    
    
    email_temp_file = open(mypath + "/email_templates/rfq_send_by_email_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Angebotsanfrage',
        'eq_email_template_version': version_number,
        'model_id': rfq_model_id[0],
        'subject': "${object.company_id.name|safe} Bestellung (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': rfq_xml_id[0],
        'report_name': "Angebotsanfrage_${(object.name or '').replace('/','_')}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: RFQ - Send by Email_de"


#############13. Purchase Order - Send by Email en ###################################
######################################################################################

purchase_xml_id = sock.execute(dbname, uid, pwd, 'ir.actions.report.xml', 'search',[("model","=", "purchase.order")])

template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Purchase Order - Send by Email")])
template_name_de = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Bestellung")])

if template_name == [] and template_name_de == []:

    email_temp_file = open(mypath + "/email_templates/purchase_order_send_by_email_en.txt","r")
    body_html = email_temp_file.read()
    
    Email_Template_en = {
        'name': 'Purchase Order - Send by Email',
        'eq_email_template_version': version_number,
        'model_id': rfq_model_id[0],
        'subject': "${object.company_id.name} Order (Ref ${object.name or 'n/a' })", 
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
    
    
    email_temp_file = open(mypath + "/email_templates/purchase_order_send_by_email_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Bestellung',
        'eq_email_template_version': version_number,
        'model_id': rfq_model_id[0],
        'subject': "${object.company_id.name} Bestellung (Ref ${object.name or 'n/a' })", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': purchase_xml_id[0],
        'report_name': "Bestellung_${(object.name or '').replace('/','_')}",
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Purchase Order - Send by Email_de"    


#############15. Lead/Opportunity Mass Mail en ################################
###############################################################################

# email_temp_file = open(mypath + "/email_templates/lead_opportunity_mass_mail_en.txt","r")
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


#############16. Lead/Opportunity Mass Mail de ################################
###############################################################################


# email_temp_file = open(mypath + "/email_templates/lead_opportunity_mass_mail_de.txt","r")
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


#############17. Odoo Enterprise Connection_en #############################
###########################################################################

# email_temp_file = open(mypath + "/email_templates/odoo_enterprise_connection_en.txt","r")
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


#############18. Odoo Enterprise Connection_de #############################
###########################################################################


# email_temp_file = open(mypath + "/email_templates/odoo_enterprise_connection_de.txt","r")
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

#############19. Password Reset en ###################################################
######################################################################################


password_reset_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search',[("model","=", "res.users")])
template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Reset Password")])
template_name_de = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Passwort zurücksetzen")])

if template_name == [] and template_name_de == []:

    email_temp_file = open(mypath + "/email_templates/reset_password_en.txt","r")
    body_html = email_temp_file.read()
    
    Email_Template_en = {
        'name': 'Reset Password',
        'eq_email_template_version': version_number,
        'model_id': password_reset_model_id[0],
        'subject': "Reset Password", 
        'body_html': body_html,
        'email_from': "${object.company_id.name} <${(object.company_id.email or user.email)|safe}>",
        'email_to': '${object.email|safe}',
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
    print "Email-Template erstellt: Password Reset_en"
    
    ir_model_data ={
        'module': 'auth_signup',
        'name':'reset_password_email',
        'model':'email.template',
        'res_id': template_id,
                }
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data) 
    
    
##############20. Passwort Reset de ###################################################
#######################################################################################
    
    
    email_temp_file = open(mypath + "/email_templates/reset_password_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Passwort zurücksetzen',
        'eq_email_template_version': version_number,
        'model_id': password_reset_model_id[0],
        'subject': "Passwort zurücksetzen", 
        'body_html': body_html,
        'email_from': "${object.company_id.name} <${(object.company_id.email or user.email)|safe}>",
        'email_to': '${object.email|safe}',
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
                            }        
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Reset Password_de" 
    
#############21. Bestellung eingegangen en ###################################################
######################################################################################


template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Order received")])
template_name_de = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Bestellung eingegangen")])

if template_name == [] and template_name_de == []:

    email_temp_file = open(mypath + "/email_templates/bestellung_eingegangen_en.txt","r")
    body_html = email_temp_file.read()
    
    Email_Template_en = {
        'name': 'Order received',
        'eq_email_template_version': version_number,
        'model_id': sale_order_model_id[0],
        'subject': "Order received", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
    print "Email-Template erstellt: Bestellung eingegangen_en"
    
    ir_model_data ={
        'module': 'eq_website_customerportal',
        'name':'email_template_sale_notification',
        'model':'email.template',
        'res_id': template_id,
                }
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)
    
    
##############22. Bestellung eingegangen de ###################################################
#######################################################################################
    
    
    email_temp_file = open(mypath + "/email_templates/bestellung_eingegangen_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Bestellung eingegangen',
        'eq_email_template_version': version_number,
        'model_id': sale_order_model_id[0],
        'subject': "Bestellung eingegangen", 
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
                            }        
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Bestellung eingegangen_de" 
    
#############23. Reminder to User en ###################################################
########################################################################################

reminder_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search',[("model","=", "crm.lead")])
template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Reminder to User")])
template_name_de = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Erinnerung an Interessent")])

if template_name == [] and template_name_de == []:

    email_temp_file = open(mypath + "/email_templates/reminder_to_user_en.txt","r")
    body_html = email_temp_file.read()
    
    Email_Template_en = {
        'name': 'Reminder to User',
        'eq_email_template_version': version_number,
        'model_id': reminder_model_id[0],
        'subject': "Reminder to User: ${object.id} from ${object.partner_id != False and object.partner_id.name or object.contact_name}",
        'body_html': body_html,
        'email_from': "admin@example.com",
        'email_to':"${(object.user_id != False and object.user_id.email)|safe}",
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
    print "Email-Template erstellt: Reminder to User_en"
    
    ir_model_data ={
        'module': 'crm',
        'name':'email_template_opportunity_reminder_mail',
        'model':'email.template',
        'res_id': template_id,
                }
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)
    
    
##############24. Reminder to User de ###################################################
#########################################################################################
    
    
    email_temp_file = open(mypath + "/email_templates/reminder_to_user_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Erinnerung an Interessent',
        'eq_email_template_version': version_number,
        'model_id': reminder_model_id[0],
        'subject': "Erinnerung an Interessent: ${object.id} from ${object.partner_id != False and object.partner_id.name or object.contact_name}", 
        'body_html': body_html,
        'email_from': "admin@example.com",
        'email_to':"${(object.user_id != False and object.user_id.email)|safe}",
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
                            }        
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Reminder to User_de" 
    
#############25. Meeting Invitation en ###################################################
########################################################################################

meeting_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search',[("model","=", "calendar.attendee")])
template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Meeting Invitation")])
template_name_de = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Terminanfrage")])

if template_name == [] and template_name_de == []:

    email_temp_file = open(mypath + "/email_templates/meeting_invitation_en.txt","r")
    body_html = email_temp_file.read()
    
    Email_Template_en = {
        'name': 'Meeting Invitation',
        'eq_email_template_version': version_number,
        'model_id': meeting_model_id[0],
        'subject': "${object.event_id.name}",
        'body_html': body_html,
        'email_from': "${object.event_id.user_id.email or ''}",
        'email_to':"${('' if object.partner_id and object.partner_id.email and object.partner_id.email==object.email else object.email|safe)}",
        'partner_to':"${object.partner_id and object.partner_id.email and object.partner_id.email==object.email and object.partner_id.id or False }",
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
    print "Email-Template erstellt: Meeting Invitation_en"
    
    ir_model_data ={
        'module': 'calendar',
        'name':'calendar_template_meeting_invitation',
        'model':'email.template',
        'res_id': template_id,
                }
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)
    
    
##############26. Meeting Invitation de ###################################################
#########################################################################################
    
    
    email_temp_file = open(mypath + "/email_templates/meeting_invitation_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Terminanfrage',
        'eq_email_template_version': version_number,
        'model_id': meeting_model_id[0],
        'subject': "${object.event_id.name}", 
        'body_html': body_html,
        'email_from': "${object.event_id.user_id.email or ''}",
        'email_to':"${('' if object.partner_id and object.partner_id.email and object.partner_id.email==object.email else object.email|safe)}",
        'partner_to':"${object.partner_id and object.partner_id.email and object.partner_id.email==object.email and object.partner_id.id or False }",
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
                            }        
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Meeting Invitation_de" 
    
#############27. Meeting Invitation Reminder en ###################################################
########################################################################################

meeting_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search',[("model","=", "calendar.attendee")])
template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Meeting Invitation - Reminder")])
template_name_de = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Terminerinnerung")])

if template_name == [] and template_name_de == []:

    email_temp_file = open(mypath + "/email_templates/meeting_invitation_reminder_en.txt","r")
    body_html = email_temp_file.read()
    
    Email_Template_en = {
        'name': 'Meeting Invitation - Reminder',
        'eq_email_template_version': version_number,
        'model_id': meeting_model_id[0],
        'subject': "${object.event_id.name} - Reminder",
        'body_html': body_html,
        'email_from': "${object.event_id.user_id.email or ''}",
        'email_to':"${('' if object.partner_id and object.partner_id.email and object.partner_id.email==object.email else object.email|safe)}",
        'partner_to':"${object.partner_id and object.partner_id.email and object.partner_id.email==object.email and object.partner_id.id or False }",
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
    print "Email-Template erstellt: Meeting Invitation Reminder_en"
    
    ir_model_data ={
        'module': 'calendar',
        'name':'calendar_template_meeting_reminder',
        'model':'email.template',
        'res_id': template_id,
                }
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)
    
    
##############28. Meeting Invitation Reminder de ###################################################
#########################################################################################
    
    
    email_temp_file = open(mypath + "/email_templates/meeting_invitation_reminder_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Terminerinnerung',
        'eq_email_template_version': version_number,
        'model_id': meeting_model_id[0],
        'subject': "${object.event_id.name} - Erinnerung", 
        'body_html': body_html,
        'email_from': "${object.event_id.user_id.email or ''}",
        'email_to':"${('' if object.partner_id and object.partner_id.email and object.partner_id.email==object.email else object.email|safe)}",
        'partner_to':"${object.partner_id and object.partner_id.email and object.partner_id.email==object.email and object.partner_id.id or False }",
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
                            }        
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Meeting Invitation Reminder_de" 

#############29. Meeting Invitation Change Date en ###################################################
########################################################################################

meeting_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search',[("model","=", "calendar.attendee")])
template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Meeting Invitation - Change Date")])
template_name_de = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name","=","Terminänderung")])

if template_name == []and template_name_de == []:

    email_temp_file = open(mypath + "/email_templates/meeting_invitation_change_date_en.txt","r")
    body_html = email_temp_file.read()
    
    Email_Template_en = {
        'name': 'Meeting Invitation - Change Date',
        'eq_email_template_version': version_number,
        'model_id': meeting_model_id[0],
        'subject': "${object.event_id.name} - Change Date",
        'body_html': body_html,
        'email_from': "${object.event_id.user_id.email or ''}",
        'email_to':"${('' if object.partner_id and object.partner_id.email and object.partner_id.email==object.email else object.email|safe)}",
        'partner_to':"${object.partner_id and object.partner_id.email and object.partner_id.email==object.email and object.partner_id.id or False }",
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
                            }     
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})            
    print "Email-Template erstellt: Meeting Invitation Change Date_en"
    
    ir_model_data ={
        'module': 'calendar',
        'name':'calendar_template_meeting_changedate',
        'model':'email.template',
        'res_id': template_id,
                }
    identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)
    
    
##############30. Meeting Invitation Change Date de ###################################################
#########################################################################################
    
    
    email_temp_file = open(mypath + "/email_templates/meeting_invitation_change_date_de.txt","r")
    body_html = email_temp_file.read()
    
    
    Email_Template_de = {
        'name': 'Terminänderung',
        'eq_email_template_version': version_number,
        'model_id': meeting_model_id[0],
        'subject': "${object.event_id.name} - Datum wurde aktualisiert", 
        'body_html': body_html,
        'email_from': "${object.event_id.user_id.email or ''}",
        'email_to':"${('' if object.partner_id and object.partner_id.email and object.partner_id.email==object.email else object.email|safe)}",
        'partner_to':"${object.partner_id and object.partner_id.email and object.partner_id.email==object.email and object.partner_id.id or False }",
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
                            }        
          
    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang':'de_DE'})            
    print "Email-Template erstellt: Meeting Invitation Change Date_de"

#############31. Bestellbestätigung eq en ###################################################
########################################################################################

bestell_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search', [("model", "=", "sale.order")])
template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search',[("name", "=", "Order - Confirmation")])
template_name_de = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name", "=", "Bestellbestätigung")])

if template_name == [] and template_name_de == []:
    email_temp_file = open(mypath + "/email_templates/bestellbestaetigung_eq_en.txt", "r")
    body_html = email_temp_file.read()

    Email_Template_en = {
        'name': 'Order - Confirmation',
        'eq_email_template_version': version_number,
        'model_id': bestell_model_id[0],
        'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Order' or 'Order'} (Ref ${object.name or 'n/a' })",
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_invoice_id.id}',
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
    }

    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})
    print "Email-Template erstellt: Order - Confirmation_en"


    # ir_model_data = {
    #     'module': 'calendar',
    #     'name': 'calendar_template_meeting_changedate',
    #     'model': 'email.template',
    #     'res_id': template_id,
    # }
    # identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)

    ##############32. Bestellbestätigung eq de ###################################################
    #########################################################################################


    email_temp_file = open(mypath + "/email_templates/bestellbestaetigung_eq_de.txt", "r")
    body_html = email_temp_file.read()

    Email_Template_de = {
        'name': 'Bestellbestätigung',
        'eq_email_template_version': version_number,
        'model_id': bestell_model_id[0],
        'subject': "${object.company_id.name|safe} ${object.state in ('draft', 'sent') and 'Auftrag' or 'Auftrag'} (Ref ${object.name or 'n/a' })",
        'body_html': body_html,
        'email_from': "${(object.user_id.email or '')|safe}",
        'partner_to': '${object.partner_invoice_id.id}',
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
    }

    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang': 'de_DE'})
    print "Email-Template erstellt: Order - Confirmation_de"

#############33. Neuregistrierung eq en ###################################################
########################################################################################

bestell_model_id = sock.execute(dbname, uid, pwd, 'ir.model', 'search', [("model", "=", "res.partner")])
template_name = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name", "=", "New Registration")])
template_name_de = sock.execute(dbname, uid, pwd, 'email.template', 'search', [("name", "=", "Neuregistrierung")])

if template_name == [] and template_name_de == []:
    email_temp_file = open(mypath + "/email_templates/registration_info_en.txt", "r")
    body_html = email_temp_file.read()

    Email_Template_en = {
        'name': 'New registration',
        'eq_email_template_version': version_number,
        'model_id': bestell_model_id[0],
        'subject': "New registration in your shop",
        'body_html': body_html,
        'email_from': "${(object.company_id.email or '')|safe}",
        'partner_to': '',
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
    }

    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'create', Email_Template_en, {})
    print "Email-Template erstellt: Neuregistrierung_en"


##############34. Neuregistrierung eq de ###################################################
#########################################################################################


    email_temp_file = open(mypath + "/email_templates/registration_info_de.txt", "r")
    body_html = email_temp_file.read()

    Email_Template_de = {
        'name': 'Neuregistrierung',
        'eq_email_template_version': version_number,
        'model_id': bestell_model_id[0],
        'subject': "Neuregistrierung im Shop",
        'body_html': body_html,
        'email_from': "${(object.company_id.email or '')|safe}",
        'partner_to': '',
        'lang': '${object.partner_id.lang}',
        'auto_delete': True,
    }

    template_id = sock.execute(dbname, uid, pwd, 'email.template', 'write', template_id, Email_Template_de,{'lang': 'de_DE'})
    print "Email-Template erstellt: Neuregistrierung_de"

    # ir_model_data = {
    #     'module': 'calendar',
    #     'name': 'calendar_template_meeting_changedate',
    #     'model': 'email.template',
    #     'res_id': template_id,
    # }
    # identificator_id = sock.execute(dbname, uid, pwd, 'ir.model.data', 'create', ir_model_data)

print "Email-Template Import ist beendet!"