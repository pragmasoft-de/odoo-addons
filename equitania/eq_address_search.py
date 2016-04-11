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
    
    eq_partner_id = fields.Many2one('res.partner', string="Partner")
    eq_crm_lead_id = fields.Many2one('crm.lead', string="Lead")
    res_partner = fields.Boolean('Partner')
    name = fields.Char(string="Name")
    city = fields.Char(string="City")
    phone = fields.Char(string="Phone")
    zip = fields.Char(size=24, string="Zip")
    
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'eq_address_search')
        cr.execute("""
        CREATE OR REPLACE VIEW eq_address_search AS (            
            select name, id as eq_partner_id, null as eq_crm_lead_id, true as res_partner, city, phone, zip from res_partner
            union 
            select name, null as eq_partner_id, id as eq_crm_lead_id, false as res_partner, city, phone, zip from crm_lead
        )
        """)