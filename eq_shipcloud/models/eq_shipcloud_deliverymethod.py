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


class eq_shipcloud_deliverymethod(models.Model):

    _name = "eq.shipcloud.deliverymethod"
    _description = "Shiplcoud Delivery method"
    
    _rec_name = "eq_sc_carrier"
    
    
    @api.depends('eq_sc_carrier')
    def eq_get_default_service(self):
        if self.eq_sc_carrier:
            service_id = self.env['eq.shipcloud.service'].search([('eq_shipcloud_carrier','=',self.eq_sc_carrier),('eq_default','=',True)])
            
            if service_id.ids:
                self.eq_sc_service_id = service_id.ids[0]
        
    
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
    
    
    eq_sc_carrier = fields.Selection(string='Carrier', selection='eq_get_carrier')
    eq_sc_service_id = fields.Many2one('eq.shipcloud.service',string='Service',help='Shipcloud Service',compute="eq_get_default_service",readonly=False,store=True)
    eq_deliverymethod_id = fields.Many2one('delivery.carrier',string="Delivery method",help="Shipcloud delivery method")
    eq_create_shipping_label = fields.Boolean(string="Create shipping Label",help="Determines if a shipping label should be created at the carrier (this means you will be charged).")