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
from openerp.tools.translate import _


class eq_res_users_new_api(models.Model):
    _inherit = 'res.users'    
        

    """
        This is our implementation of extenstion of res_uses in new api.
        We'll also migrate implementation of res_users from old api to new api 
    """
        
    """
    @api.model    
    def create(self, vals):
                
        # default call - create new user and save automaticaly created new partner_id            
        new_user =  super(eq_res_users_new_api, self).create(vals)
            
        # check if we can find at least one record in res_partner with same email as user provided
        if 'email' in vals:
            print "-----------------------  yes, it's here"
            print "------ vals['email']: ", vals['email']
            
            partner = self.env['res.partner'].search([('email', '=', vals['email']), ('customer', '=', True)])                                                        
            wrong_partner_id = new_user.partner_id.id
            
            # yes, we have an existing partner, so there's no need to use new created one. just use existing partner and delete new one
            if partner.id is not False:                                        
                new_user.partner_id = partner.id                                                    # set existing partner
                                        
                wrong_partner = self.env['res.partner'].search([('id', '=', wrong_partner_id)])     # get new + automaticaly generated partner and delete him - we don't need him
                wrong_partner.unlink() 
        else:
            print "------------------------- no --------"
                     
        return new_user
    """