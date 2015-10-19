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

from openerp.osv import fields, osv, orm
import datetime
import time

class eq_sale_quote_template_extension(osv.osv):
    _inherit = 'sale.quote.template'
    
    _columns = {
                'note': fields.html('Terms and conditions'),
                'eq_header_text': fields.html('Header text'),
                }
        
class eq_sale_order_quote_template_extension(osv.osv):
    _inherit = 'sale.order'
    
    def original_onchange_template_id(self, cr, uid, ids, template_id, partner=False, fiscal_position=False, order_line=[], context=None):
        if not template_id:
            return True

        if context is None:
            context = {}
        context = dict(context, lang=self.pool.get('res.partner').browse(cr, uid, partner, context).lang)
        
        #Adds the positons and doesn't replace them
        #lines = [(5,)]
        lines = order_line
        quote_template = self.pool.get('sale.quote.template').browse(cr, uid, template_id, context=context)
        for line in quote_template.quote_line:
            res = self.pool.get('sale.order.line').product_id_change(cr, uid, False,
                False, line.product_id.id, line.product_uom_qty, line.product_uom_id.id, line.product_uom_qty,
                line.product_uom_id.id, line.name, partner, False, True, time.strftime('%Y-%m-%d'),
                False, fiscal_position, True, context)
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

    
    def onchange_template_id(self, cr, uid, ids, template_id, partner=False, fiscal_position=False, order_line=[], context=None):
        if not partner:
            template_id = False
        res = self.original_onchange_template_id(cr, uid, ids, template_id, partner, fiscal_position, order_line, context=context)
        if template_id:
            res['value']['eq_head_text'] = self.pool.get('sale.quote.template').browse(cr, uid, template_id).eq_header_text
        return res
    
    def onchange_partner_id(self, cr, uid, ids, partner_id, template_id=False, context=None):
        res = super(eq_sale_order_quote_template_extension, self).onchange_partner_id(cr, uid, ids, partner_id, context=context)
        if partner_id:
            res2 = self.onchange_template_id(cr, uid, ids, template_id, partner_id, False, [], context)
            if type(res2) is not bool:
                res['value'].update(res2['value'])
        return res
