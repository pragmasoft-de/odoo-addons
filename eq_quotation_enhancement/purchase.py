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
import datetime
import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class eq_purchase_order(models.Model):
    _inherit = 'purchase.order'
   
    template_id = fields.Many2one(comodel_name='sale.quote.template', string='Quote Template', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    
     
    
    def original_onchange_template_id(self, quote_template, partner=False, fiscal_position=False, order_lines = []):
        if not quote_template:
            return True

        #=======================================================================
        # if context is None:
        #     context = {}
        # context = dict(context, lang=self.env['res.partner'].browse(partner).lang)
        #=======================================================================
        
        #Adds the positons and doesn't replace them
        #lines = [(5,)]
        lines = []#order_lines
        
        purchase_order_line_obj = self.env['purchase.order.line']
        for line in quote_template.quote_line:
            res = purchase_order_line_obj.product_id_change(False, line.product_id.id, line.product_uom_qty, line.product_uom_id.id,
                partner, time.strftime(DEFAULT_SERVER_DATETIME_FORMAT), fiscal_position, self.minimum_planned_date, line.name, False, 'draft')
            
            data = res.get('value', {})
            if 'tax_id' in data:
                data['tax_id'] = [(6, 0, data['tax_id'])]
            data.update({
                'name': line.name,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'product_uom_qty': line.product_uom_qty,
                'product_id': line.product_id.id,
                'product_uom': line.product_uom_id.id,
                'website_description': line.website_description,
                'state': 'draft',
            })
            lines.append((0, 0, data))
        options = []
        for option in quote_template.options:
            options.append((0, 0, {
                'product_id': option.product_id.id,
                'name': option.name,
                'quantity': option.quantity,
                'uom_id': option.uom_id.id,
                'price_unit': option.price_unit,
                'discount': option.discount,
                'website_description': option.website_description,
            }))
        date = False
        if quote_template.number_of_days > 0:
            date = (datetime.datetime.now() + datetime.timedelta(quote_template.number_of_days)).strftime("%Y-%m-%d")
        data = {'order_line': lines, 'website_description': quote_template.website_description, 'note': quote_template.note, 'options': options, 'validity_date': date}
        return {'value': data}
    
    @api.onchange('template_id')
    def onchange_template_id(self):
        partner_id = False
        if (self.partner_id):
            partner_id = self.partner_id.id
        if (self.template_id):
            res = self.original_onchange_template_id(self.template_id, partner_id, self.fiscal_position, self.order_line)
            self.eq_head_text = self.template_id.eq_header_text
            self.notes = self.template_id.note
            
            if (res and 'value' in res and 'order_line' in res['value'] and res['value']['order_line']):
                purchase_order_line_obj = self.env['purchase.order.line']
                lines = res['value']['order_line']                
                self.order_line = lines                        