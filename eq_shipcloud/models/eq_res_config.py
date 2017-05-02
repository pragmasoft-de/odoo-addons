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
import requests
from openerp.osv import osv

class eq_shipdefault_logistic_unit(models.Model):
    
    _name = 'eq.shipdefault.logistic.unit'
    
    _rec_name = 'eq_def_logistic_unit'
    
    eq_def_logistic_unit = fields.Many2one("product.ul", string="Default Logistic Unit")
    eq_description = fields.Text('Description')
    
    

class eq_shipcloud_config(models.TransientModel):
    _name = 'eq.shipcloud.config'
    _inherit = 'res.config.settings'
    
    eq_shipcloud_apikey = fields.Char(string="API key")
    eq_shipcloud_sandbox_apikey = fields.Char(string="Sandbox API key")
    eq_is_sandbox_apikey = fields.Boolean("Use sandbox API Key")
    eq_shipcloud_service_url = fields.Char(string ="Service URL", required=True)
    eq_def_logistic_unit = fields.Many2one("product.ul", string="Default Logistic Unit", required=True)
    
    """ Shipcloud API key get function """
    @api.multi
    def get_default_eq_shipcloud_apikey(self):
        key = self.env['ir.config_parameter'].get_param("eq.shipcloud.apikey")
        return {'eq_shipcloud_apikey': key}
    
    
    """ Shipcloud API key set function """    
    @api.multi
    def set_eq_shipcloud_apikey(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
#             checking, whether the provided key is valid or not
            if record.eq_shipcloud_apikey:
                is_valid = requests.get('https://api.shipcloud.io/v1/carriers', data=None,auth=(record.eq_shipcloud_apikey, ''))
                if not is_valid.status_code == 200:
                    raise osv.except_osv(_('Error!'), _('You provided API key is not valid.'))
            config_parameters.set_param("eq.shipcloud.apikey", record.eq_shipcloud_apikey or '',)
            
    
    """ Shipcloud sandbox API key get function """              
    @api.multi
    def get_default_eq_shipcloud_sandbox_apikey(self):
        key = self.env['ir.config_parameter'].get_param("eq.shipcloud.sandbox.apikey")
        return {'eq_shipcloud_sandbox_apikey': key}
    

    """ Shipcloud sandbox API key set function """ 
    @api.multi
    def set_eq_shipcloud_sandbox_apikey(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
#             checking, whether the provided key is valid or not
            if record.eq_shipcloud_sandbox_apikey:
                is_valid = requests.get('https://api.shipcloud.io/v1/carriers', data=None,auth=(record.eq_shipcloud_sandbox_apikey, ''))
                if not is_valid.status_code == 200:
                    raise osv.except_osv(_('Error!'), _('You provided Sandbox API key is not valid.'))
            config_parameters.set_param("eq.shipcloud.sandbox.apikey", record.eq_shipcloud_sandbox_apikey or '',)
    

    """ Shipcloud service URL get function """ 
    @api.multi
    def get_default_eq_shipcloud_service_url(self):
        key = self.env['ir.config_parameter'].get_param("eq.shipcloud.service.url")
        return {'eq_shipcloud_service_url': key or 'https://api.shipcloud.io'}
    
    
    """ Shipcloud service URL set function """ 
    @api.multi
    def set_eq_shipcloud_service_url(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config_parameters.set_param("eq.shipcloud.service.url", record.eq_shipcloud_service_url or '',)
            
    
    @api.multi
    def get_default_eq_is_sandbox_apikey(self):
        res = self.env['ir.config_parameter'].get_param("eq.is.sandbox.apikey")
        if res == 'True':
            return {'eq_is_sandbox_apikey': True}
        return {'eq_is_sandbox_apikey': False}
    
    
    @api.multi
    def set_eq_is_sandbox_apikey(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config_parameters.set_param("eq.is.sandbox.apikey", str(record.eq_is_sandbox_apikey),)
            
          
    """ Shipcloud Default logistic unit """        
    @api.multi
    def get_default_eq_def_logistic_unit(self):
        logistic_data = self.env['eq.shipdefault.logistic.unit'].search([])[0]

        return {'eq_def_logistic_unit': logistic_data.eq_def_logistic_unit.id}
    
        
    """ Shipcloud Default logistic unit"""   
    @api.multi
    def set_eq_def_logistic_unit(self):
        logistic_data_id = self.env['eq.shipdefault.logistic.unit'].search([])[0]
        logistic_data_id.write({'eq_def_logistic_unit': self.eq_def_logistic_unit.id})
        