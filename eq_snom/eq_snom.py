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
from openerp.http import request
#from main import eq_snom_controller

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

    def start_call(self, phone_number):
        #Get current user    
        res_user_obj = self.env['res.users'].sudo()
        res_user = res_user_obj.search([('id', '=', self._uid)])
        
        if (res_user.eq_snom_ip_name) and (phone_number):
            #Format the phone number            
            if (res_user.eq_snom_prefix):
                phone_number = res_user.eq_snom_prefix + phone_number
            phone_number_formatted = phone_number.replace('+','00')
            phone_number_formatted = ''.join(i for i in phone_number_formatted if i in "0123456789")                        
            
            #Build URL
            if (res_user.eq_snom_user) and (res_user.eq_snom_password):
                url = request.httprequest.host_url + "snom/call?url=http://" + res_user.eq_snom_user + ":" + res_user.eq_snom_password + "@" + res_user.eq_snom_ip_name + "/command.htm?number=" + phone_number_formatted
            else:    
                url = request.httprequest.host_url + "snom/call?url=http://" + res_user.eq_snom_ip_name + "/command.htm?number=" + phone_number_formatted                          
                          
            #url_response = urllib2.urlopen(url).read()
            
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new',
            }
                        
            #print "------------------ called url: ", url_response               

    @api.multi
    def eq_call_phone_snom(self):        
        return self.start_call(self.phone)
        
    @api.multi
    def eq_call_mobile_snom(self):
        return self.start_call(self.mobile)    
        
  