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



class sale_config(models.TransientModel):
    _inherit = 'sale.config.settings'
    
    eq_head_text_invoice = fields.Html(string="Invoice head text [equitania]",required=False, default="")
    eq_foot_text_invoice = fields.Html(string="Invoice foot text [equitania]",required=False, default="")
    
    # eq_head_text_invoice
    @api.multi
    def get_default_eq_head_text_invoice(self):
        result = self.env['ir.config_parameter'].get_param("eq.head.text.invoice")
        return {'eq_head_text_invoice': result}

    @api.multi
    def set_eq_head_text_invoice(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:                        
                config_parameters.set_param("eq.head.text.invoice", record.eq_head_text_invoice or '',)
    
    
    # eq_foot_text_invoice
    @api.multi
    def get_default_eq_foot_text_invoice(self):
        result = self.env['ir.config_parameter'].get_param("eq.foot.text.invoice")
        return {'eq_foot_text_invoice': result}

    @api.multi
    def set_eq_foot_text_invoice(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:                        
                config_parameters.set_param("eq.foot.text.invoice", record.eq_foot_text_invoice or '',)    