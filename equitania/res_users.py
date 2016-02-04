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
from openerp.osv import osv
from openerp import SUPERUSER_ID

class eq_res_users(models.Model):
    _inherit = 'res.users'

    
    eq_employee_id = fields.Many2one('hr.employee', 'Employee', copy=False)
    eq_custom01 = fields.Char(size=64) # field added from eq_company_custom_fields.py            

    
    @api.model    
    def create(self, vals):
        """
            Extension of default create method
            @vals: values to be set
            @return: new created res.user
        """
        
        # default call - create new user and save automaticaly created new partner_id            
        new_user =  super(eq_res_users, self).create(vals)
        
        # check if we can find at least one record in res_partner with same email as user provided
        if new_user.login : #fixed the issue for users
            partner = self.env['res.partner'].search([('email', '=',new_user.login), ('customer', '=', True)])
            if len(partner) > 1:
                existing_partner_id = partner[0].id         # it's a tuple
            else:
                existing_partner_id = partner.id            # it's a single record
                
                                                                    
            new_generated_partner_id = new_user.partner_id.id   # save id of new & automaticaly generated partner_id
            
            # yes, we have an existing partner, so there's no need to use new created one. just use existing partner and delete new one
            if existing_partner_id is not False:
                if existing_partner_id != new_generated_partner_id:     # ok, it's call from backend ILLINGEN - deleted new generated record"                            
                    new_user.partner_id = existing_partner_id                                                        
                    wrong_partner = self.env['res.partner'].search([('id', '=', new_generated_partner_id)])     # get new + automaticaly generated partner and delete him - we don't need him
                    wrong_partner.unlink() 
        
        return new_user