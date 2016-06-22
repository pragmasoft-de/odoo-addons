# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
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

from openerp import models, fields, api
from openerp import tools

class EQ_Address_Search(models.Model):
    _name = "eq.address.search"
    _auto=False
    _order = 'name'
    
    eq_partner_id = fields.Many2one('res.partner', string="Partner")
    eq_crm_lead_id = fields.Many2one('crm.lead', string="Lead")
    #res_partner = fields.Boolean('Partner')
    name = fields.Char(string="Name")
    contact_name = fields.Char(string="Contact name")
    city = fields.Char(string="City")
    phone = fields.Char(string="Phone")
    zip = fields.Char(size=24, string="Zip")
    country_id = fields.Many2one('res.country', string="Country")
    is_company = fields.Boolean('Company')
    parent_id = fields.Many2one('res.partner', string="Related Company")
    customer = fields.Boolean('Customer')
    supplier = fields.Boolean('Supplier')
    lead = fields.Boolean('Lead')
    categories = fields.Char(string="Categories")
    #Todo: Feld für Suche TelNr
    phone_search = fields.Char(string="Phone")
    
    #TODO JOIN
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'eq_address_search')
        cr.execute("""
        CREATE OR REPLACE VIEW eq_address_search AS (      
            
            SELECT ROW_NUMBER() OVER(ORDER BY coalesce(eq_partner_id, eq_crm_lead_id)) id,* 
            FROM (
                SELECT p.name, '' as contact_name, p.id as eq_partner_id, cast(c.id as int) as eq_crm_lead_id, p.city, p.phone, p.zip, p.country_id, p.is_company, p.parent_id, p.customer, p.supplier, cast(c.id as bool) as lead,
                (select string_agg(cat.name, ', ') from res_partner_res_partner_category_rel rel
                left outer join res_partner_category cat on rel.category_id = cat.id
                where rel.partner_id = p.id) as categories,
                regexp_replace(regexp_replace(trim(coalesce(p.phone,'')),'\+','00','g'),'[^0-9]','','g') as phone_search
                FROM res_partner p 
                LEFT OUTER JOIN crm_lead c on c.partner_id = p.id
                WHERE is_company
                and p.id not in (select partner_id from res_users where coalesce(partner_id,0)>0)
                
                UNION  
                
                SELECT p.display_name as name, p.name as contact_name, p.id as eq_partner_id, cast(c.id as int) as eq_crm_lead_id, p.city, p.phone, p.zip, p.country_id, p.is_company, p.parent_id, p.customer, p.supplier, cast(c.id as bool) as lead,
                (select string_agg(cat.name, ', ') from res_partner_res_partner_category_rel rel
                left outer join res_partner_category cat on rel.category_id = cat.id
                where rel.partner_id = p.id) as categories,
                regexp_replace(regexp_replace(trim(coalesce(p.phone,'')),'\+','00','g'),'[^0-9]','','g') as phone_search
                FROM res_partner p
                LEFT OUTER JOIN crm_lead c on c.partner_id = p.id
                WHERE not is_company
                and p.id not in (select partner_id from res_users where coalesce(partner_id,0)>0)
                
                UNION 
                
                SELECT coalesce(NULLIF(c.partner_name,''), c.name) as name, c.contact_name, null as eq_partner_id, c.id as eq_crm_lead_id, c.city, c.phone, c.zip, c.country_id, p.is_company, p.parent_id, false as customer, false as supplier, true as lead,
                (select string_agg(cat.name, ', ') from crm_lead_category_rel rel
                left outer join crm_case_categ cat on rel.category_id = cat.id
                where rel.lead_id = c.id) as categories,
                regexp_replace(regexp_replace(trim(coalesce(c.phone,'')),'\+','00','g'),'[^0-9]','','g') as phone_search
                FROM crm_lead  c
                left outer join res_partner p on p.id = c.partner_id
                WHERE coalesce(partner_id,0) = 0
                --and coalesce(p.id,0) not in (select partner_id from res_users where coalesce(partner_id,0)>0)
            ) a
       )
        """)