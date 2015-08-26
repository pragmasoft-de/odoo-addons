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

#import urllib2
from openerp.http import request

#New API, Remove Old API import if the New API is used. Otherwise you'll get an import error.
from openerp import models, fields, api, _

class eq_snom_res_users(models.Model):
    _inherit = 'res.users'
    
    eq_snom_ip_name = fields.Char(string='IP/Name', related='partner_id.eq_snom_ip_name')
    eq_snom_user = fields.Char(string='User', related='partner_id.eq_snom_user')
    eq_snom_password = fields.Char(string='Password', related='partner_id.eq_snom_password')
    eq_snom_prefix = fields.Char(string='Prefix', related='partner_id.eq_snom_prefix')
    
    @api.one
    def write(self, vals):
        admin = self.sudo()
        if self._uid == self.ids[0]:
            if 'eq_snom_ip_name' in vals:
                admin.partner_id.eq_snom_ip_name = vals['eq_snom_ip_name']
                vals.pop('eq_snom_ip_name', None)
            if 'eq_snom_user' in vals:
                admin.partner_id.eq_snom_user = vals['eq_snom_user']
                vals.pop('eq_snom_user', None)
            if 'eq_snom_password' in vals:
                admin.partner_id.eq_snom_password = vals['eq_snom_password']
                vals.pop('eq_snom_password', None)
            if 'eq_snom_prefix' in vals:
                admin.partner_id.eq_snom_prefix = vals['eq_snom_prefix']
                vals.pop('eq_snom_prefix', None)
        res = super(eq_snom_res_users, self).write(vals)
        return res

    
class eq_snom_call(models.TransientModel):
    _name = 'eq.snom.call'
    
    
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
            
            # execute client call and hand our url paramater over. We'll use that url in our javascript !     
            return {
                'type': 'ir.actions.client',
                'url': url,
                'tag': 'eq_snom.action',
            }
                                    
            """
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new',
            }
            """
            
                        
                
        
class eq_snom_res_partner(models.Model):
    _inherit = 'res.partner'           
    
    eq_snom_ip_name = fields.Char(string='IP/Name')
    eq_snom_user = fields.Char(string='User')
    eq_snom_password = fields.Char(string='Password')
    eq_snom_prefix = fields.Char(string='Prefix')            

    @api.multi
    def eq_call_phone_snom(self):        
        tmp = self.env['eq.snom.call']
        return tmp.start_call(self.phone)
        
    @api.multi
    def eq_call_mobile_snom(self):
        tmp = self.env['eq.snom.call']     
        return tmp.start_call(self.mobile)    
        
class eq_snom_crm_lead(models.Model):
    _inherit = 'crm.lead'                        

    @api.multi
    def eq_call_phone_snom(self):
        tmp = self.env['eq.snom.call']        
        return tmp.start_call(self.phone)
        
    @api.multi
    def eq_call_mobile_snom(self):
        tmp = self.env['eq.snom.call']     
        return tmp.start_call(self.mobile)
