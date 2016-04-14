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


from openerp import models, fields, api, _


class eq_product_select_case_section_wiz(models.TransientModel):
    _name = 'eq.product.select.case.section.wiz'
    
    crm_case_section_id = fields.Many2one('crm.case.section', 'Sales Team')
    
    @api.multi
    def change_to_leads(self):
        if not self._context['active_ids']:
            return
        partner_ids = self._context['active_ids']
        partner_obj = self.env['res.partner']
        selected_partners = self.env['res.partner'].browse(self.env.context['active_ids'])
        for partner in selected_partners:
            self.change_partner_to_lead(partner, self.crm_case_section_id.id)
        
    
    def change_partner_to_lead(self, partner, section_id):
        crm_lead_obj = self.env['crm.lead']
        
        lead_values = {
                       'name': partner.name,
                       'partner_id' : partner.id,
                       'email_from' : partner.email,
                       'phone' : partner.phone,
                       'fax' : partner.fax,
                       'mobile' : partner.mobile,
                       'section_id' : section_id,                       
                       'street' : partner.street,
                       'eq_house_no' : partner.eq_house_no,
                       'zip' : partner.zip,
                       'city' : partner.city,
                       'eq_citypart' : partner.eq_citypart,
                       'function' : partner.function,
                       'birthdate' : partner.eq_birthday,
                       'firstname' : partner.eq_firstname,
                       }
        
        if partner.country_id:
            lead_values['country_id'] = partner.country_id.id
            
        if partner.state_id:
            lead_values['state_id'] = partner.state_id.id
            
        if partner.parent_id:
            lead_values['partner_name'] = partner.parent_id.name
            
        if not partner.is_company:
            lead_values['lastname'] = partner.name
            if partner.eq_firstname:
                lead_values['name'] = partner.eq_firstname + ' ' + partner.name
                
            if partner.title:
                lead_values['title'] = partner.title.id
        
        return crm_lead_obj.create(lead_values)
        
        