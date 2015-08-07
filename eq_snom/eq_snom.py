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

import urllib2

#New API, Remove Old API import if the New API is used. Otherwise you'll get an import error.
from openerp import models, fields, api, _

class eq_snom_res_users(models.Model):
    _inherit = 'res.users'
    
    eq_snom_ip_name = fields.Char(string='IP/Name')
    eq_snom_user = fields.Char(string='User')
    eq_snom_password = fields.Char(string='Password')
    eq_snom_prefix = fields.Char(string='Prefix')
        
class eq_snom_res_users(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def eq_call_snom(self):
        """ Execute HTTP GET after button click """
        
        res_user_obj = self.env['res.users'].sudo()
        res_user = res_user_obj.search([('id', '=', self._uid)])
        phone_number = res_user.eq_snom_prefix + self.phone.replace('+','00')
        phone_number = ''.join(i for i in phone_number if i in "0123456789")
        if (res_user.eq_snom_user) and (res_user.eq_snom_password):
            url = "http://" + res_user.eq_snom_user + ":" + res_user.eq_snom_password + "@" + res_user.eq_snom_ip_name + "/command.htm?number=" + phone_number
        else:    
            url = "http://" + res_user.eq_snom_ip_name + "/command.htm?number=" + phone_number              
        #url_response = urllib2.urlopen(url).read()
        #print "------------------ url_response: ", url_response
        
        print "------------------ ip/name: ", url       
        
  