# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
#
#
#    Adaptation of the module intero_hhw
#    Copyright (C) 2014 Intero Technologies GmbH(<http://intero-technologies.de>).
#
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
from datetime import datetime
from openerp import tools

#je nach Modul
fistname_column = 'eq_firstname'
surname_column = 'name'
birthday_column = 'eq_birthday'

#####Erweiterung aus intero_hhw übernommen: Erstellung des Kontaktes für Lead (mit Vor- und Nachname)
class eq_crm_lead(models.Model):
    _inherit = 'crm.lead'
    
    _order = "date_action,priority desc,id desc"
    
    firstname = fields.Char('Firstname')
    lastname = fields.Char('Lastname')
    category_ids = fields.Many2many(
        'res.partner.category', string='Tags')
    website = fields.Char('Website')
    birthdate = fields.Date('Birthdate')
    
    
    def _convert_opportunity_data(self, cr, uid, lead, customer, section_id=False, context=None):
        res = super(eq_crm_lead, self)._convert_opportunity_data(cr, uid, lead, customer, section_id=False, context=None)
        res[birthday_column] = lead.birthdate
        #res['messaging'] = lead.messaging
        res['website'] = lead.website
        return res
    
    
    def _create_lead_partner(self, cr, uid, lead, context=None):
        partner_id = False
        if lead.partner_name and (lead.lastname or lead.firstname):
            partner_id = self._lead_create_contact(cr, uid, lead, lead.partner_name, False, True, context=context)
            partner_id = self._lead_create_contact(cr, uid, lead, lead.firstname, lead.lastname, False, partner_id, context=context)
        elif lead.partner_name and not lead.lastname:
            partner_id = self._lead_create_contact(cr, uid, lead, lead.partner_name, False, True, context=context)
        elif not lead.partner_name and lead.lastname:
            partner_id = self._lead_create_contact(cr, uid, lead, lead.firstname, lead.lastname, False, context=context)
        elif lead.email_from and self.pool.get('res.partner')._parse_partner_name(lead.email_from, context=context)[0]:
            contact_name = self.pool.get('res.partner')._parse_partner_name(lead.email_from, context=context)[0]
            partner_id = self._lead_create_contact(cr, uid, lead, False, contact_name, False, context=context)
        else:
            raise Warning(
                _('No customer name defined. Please fill one of the following fields: Company Name, Contact Name or Email ("Name <email@address>")')
            )
        return partner_id
    
    def _lead_create_contact(self, cr, uid, lead, firstname, lastname, is_company, parent_id=False, context=None):
        partner = self.pool.get('res.partner')
        vals = {'name': firstname if is_company else '%s %s' % (firstname, lastname),
            'user_id': lead.user_id.id,
            'comment': lead.description,
            'section_id': lead.section_id.id or False,
            'parent_id': parent_id,
            'phone': lead.phone,
            'mobile': lead.mobile,
            'email': tools.email_split(lead.email_from) and tools.email_split(lead.email_from)[0] or False,
            'fax': lead.fax,
            'title': lead.title and lead.title.id or False,
            'function': lead.function,
            'street': lead.street,
            'street2': lead.street2,
            'zip': lead.zip,
            'city': lead.city,
            'country_id': lead.country_id and lead.country_id.id or False,
            'state_id': lead.state_id and lead.state_id.id or False,
            'is_company': is_company,
            'type': 'contact'
        }
        if not is_company:
            vals[fistname_column] = firstname
            vals[surname_column] = lastname
        partner = partner.create(cr, uid, vals, context=context)
        partner_pool = self.pool.get('res.partner')
        partner = partner_pool.browse(cr, uid, partner, context=context)
        partner.write({'category_id':[(6, 0, [x.id for x in lead.category_ids])],
                       birthday_column:lead.birthdate,
                       #'messaging':lead.messaging,
                       'website':lead.website,
                       })
        return partner.id
    
#####Erweiterung aus intero_hhw übernommen
class crm_make_sale(models.TransientModel):
    _inherit = 'crm.make.sale'
    _name = 'crm.make.sale'

    take_over = fields.Boolean('Take Over Data', default=True)
    partner_id = fields.Many2one('res.partner', 'Customer', required=False, domain=[('customer', '=', True)])
    
    create_customer = fields.Boolean('Create New Customer', default=True)
    
    def makeOrder(self, cr, uid, ids, context=None):
        make_sale = self.pool.get('crm.make.sale').browse(cr, uid, ids)
        crm_lead_obj = self.pool.get('crm.lead')
        if make_sale and make_sale.create_customer:
            if context.get('active_ids'):
                lead = context and context.get('active_ids', []) or []
                if lead:
                    lead = crm_lead_obj.browse(cr, uid, lead[0], context)
                    partner_id = crm_lead_obj._create_lead_partner(cr, uid, lead, context)
                    self.pool['res.partner'].write(cr, uid, partner_id, {'section_id': lead.section_id and lead.section_id.id or False})
                    if partner_id:
                        lead.write({'partner_id': partner_id})
                        make_sale.write({'partner_id': partner_id})
        value = super(crm_make_sale, self).makeOrder(cr, uid, ids,
                                                     context=context)

        

        if 'active_ids' in context:
            crm_case_stage_obj = self.pool.get('crm.case.stage')

            crm_case_id = crm_case_stage_obj.search(cr, uid,
                                                    [('name', '=',
                                                      'Negotiation')], limit=1)
            if crm_case_id:
                crm_lead = crm_lead_obj.browse(cr, uid,
                                               context.get('active_ids'))
                for lead in crm_lead:
                    vals = {
                        'stage_id': crm_case_id[0],
                        'sale_order_ids': [(4, value.get('res_id'))]
                    }
                    crm_lead_obj.write(cr, uid, lead.id, vals)

        if make_sale and make_sale[0].take_over:
            if value.get('res_id') and isinstance(value.get('res_id'), int):
                sale_obj = self.pool.get('sale.order')
                vals = {
                    'campaign_id': crm_lead.campaign_id.id,
                    'medium_id': crm_lead.medium_id.id,
                    'categ_ids': [(6, 0,
                                   [x.id for x in crm_lead.category_ids])]
                }
                sale_obj.write(cr, uid, value.get('res_id'), vals)

        return value