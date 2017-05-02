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
import requests
import logging
_logger = logging.getLogger(__name__)



class eq_shipcloud_service(models.Model):

    _name = "eq.shipcloud.service"
    _description = "Shiplcoud Carrier/service"
    
    _rec_name = "eq_name"
    
    
    @api.model
    def create(self,values):
        if values.has_key('eq_default'):
            
            service_id = self.search([('eq_shipcloud_carrier','=',values.get('eq_shipcloud_carrier')),('eq_default','=',True)])
            if len(service_id.ids) > 1 or len(service_id.ids) ==1 and values.get('eq_default') == True:
                raise osv.except_osv(_('Error!'), _('Carrier can have only one default service.'))
            
        return super(eq_shipcloud_service, self).create(values)
    
    
    @api.multi
    def write(self, vals):
        if vals.has_key('eq_default'):
            
            service_id = self.search([('eq_shipcloud_carrier','=',self.eq_shipcloud_carrier),('eq_default','=',True)])
            if len(service_id.ids) > 1 or len(service_id.ids) == 1 and vals.get('eq_default') == True:
                raise osv.except_osv(_('Error!'), _('Carrier can have only one default service.'))
        
        return super(eq_shipcloud_service, self).write(vals)
    
    
    @api.model
    def eq_get_carrier(self):
        
        config_obj = self.env['ir.config_parameter']
        if config_obj.get_param("eq.is.sandbox.apikey",False) == 'True':
            api_key = config_obj.get_param("eq.shipcloud.sandbox.apikey",False)
        else:
            api_key = config_obj.get_param("eq.shipcloud.apikey",False)
            
        url = config_obj.get_param("eq.shipcloud.service.url",False) or None
        
        if type(api_key) is bool:
            res = requests.get('https://api.shipcloud.io/v1/carriers', data=None,auth=('0750b5da599ac83dd0edf77cf95b7675', ''))
        else:
            res = requests.get(url+'/v1/carriers', data=None,auth=(api_key, ''))            
        
        return [(datas.get('name'), datas.get('display_name')) for datas in res.json()]
    
    
    eq_name =  fields.Char(string="Service",copy=False,help= "The service that should be used for the shipment")
    eq_shipcloud_carrier = fields.Selection(string='Carrier', selection='eq_get_carrier')
    eq_default = fields.Boolean("Is Default",copy=False,help="The default service for the selected carrier.")
    eq_comments = fields.Text("Description")
  