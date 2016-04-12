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

#from openerp.osv import fields, osv, orm
from openerp import models, fields, api, _

class eq_lead(models.Model):
    """
        Extended version of crm.lead class - we will save referred by information
    """    
    
    _inherit = 'crm.lead'
    
    eq_lead_referred_id = fields.Many2one('eq.lead.referred', 'Referred By ID')
    eq_lead_referred_name = fields.Char(string='Referred By', store=True, related='eq_lead_referred_id.eq_description')


class eq_lead_referred(models.Model):
    """
        Our own definition of reffered class - will contain only simple description
    """
    
    _name = "eq.lead.referred"
    _rec_name = "eq_description"
    
    eq_description  = fields.Char('Description')


class eq_res_partner_ref(models.Model):
    """
        Extend version of res.partner with small modification of write.
        Our goal is to schow dropdownlist with "Referred by" only if customer flag is TRUE
    """
    
    _inherit = 'res.partner'
    
    eq_lead_referred_id = fields.Many2one('eq.lead.referred', 'Referred By')
    
    @api.multi
    def write(self, vals):                
        """
            Override of write function - save customer flag also for each contact
            @vals: values to be set
            @return: super call            
        """
        res_partner_obj = self.env['res.partner'].sudo()
        
        if "customer" in vals:            
            res_partners = res_partner_obj.search([('parent_id', '=', self._ids[0])])
            if res_partners:
                for partner in res_partners:
                    partner.customer = vals["customer"]            
                        
        return super(eq_res_partner_ref, self).write(vals)    