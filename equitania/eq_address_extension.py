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
from openerp.tools.translate import _

class sale_order(osv.osv):
    _inherit = 'sale.order'
    
    def _compute_invoice_address(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for person in self.browse(cr, uid, ids):
            #if person.partner_invoice_id:
            if person.partner_invoice_id.street and person.partner_invoice_id.city:
                res[person.id] = person.partner_invoice_id.street + ', ' + person.partner_invoice_id.city
            elif person.partner_invoice_id.street:
                res[person.id] = person.partner_invoice_id.street
            elif person.partner_invoice_id.city:
                res[person.id] = person.partner_invoice_id.city
            else:
                res[person.id] = False
        return res
    
    def _compute_delivery_address(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for person in self.browse(cr, uid, ids):
            #if person.partner_shipping_id:
            if person.partner_shipping_id.street and person.partner_shipping_id.city:
                res[person.id] = person.partner_shipping_id.street + ', ' + person.partner_shipping_id.city
            elif person.partner_shipping_id.street:
                res[person.id] = person.partner_shipping_id.street
            elif person.partner_shipping_id.city:
                res[person.id] = person.partner_shipping_id.city
            else:
                res[person.id] = False
        return res  

    _columns = {
                'eq_pricelist_change': fields.boolean('Pricelist Default'),
                'eq_invoice_address': fields.function(_compute_invoice_address, string=" ", store=False, type="char"),
                'eq_delivery_address': fields.function(_compute_delivery_address, string=" ", store=False, type="char"),
                'client_order_ref': fields.char('Reference/Description', copy=True),
                }

sale_order()


class eq_sale_configuration_address(osv.TransientModel):
    _name = 'sale.config.settings'
    _inherit = _name
    
    def set_default_values_eq_address(self, cr, uid, ids, context=None):
        ir_values_obj = self.pool.get('ir.values')
        config = self.browse(cr, uid, ids[0], context)
        
        ir_values_obj.set_default(cr, uid, 'sale.order', 'default_show_address', config.default_show_address or False)
        ir_values_obj.set_default(cr, uid, 'sale.order', 'default_search_only_company', config.default_search_only_company or False)
            
                
    
    def get_default_values_eq_address(self, cr, uid, fields, context=None):
        ir_values_obj = self.pool.get('ir.values')
        notification = ir_values_obj.get_default(cr, uid, 'sale.order', 'default_show_address')
        only_company = ir_values_obj.get_default(cr, uid, 'sale.order', 'default_search_only_company')
        return {
                'default_show_address': notification,
                'default_search_only_company': only_company,
                }
    
    _columns = {
                'default_show_address': fields.boolean('Show street and city in the partner search of the Sale and Purchase Order [equitania]', help="This adds the street and the city to the results of the partner search of the Sale and Purchase Order."),
                'default_search_only_company': fields.boolean('Only Search for Companies [equitania]', help="Only Companies will be shown in the Customer search of the Sale and Purchase Order.")
                }