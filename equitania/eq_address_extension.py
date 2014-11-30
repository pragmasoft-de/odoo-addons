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
            res[person.id] = person.partner_invoice_id.street + ', ' + person.partner_invoice_id.city
        return res
    
    def _compute_delivery_address(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for person in self.browse(cr, uid, ids):
            res[person.id] = person.partner_shipping_id.street + ', ' + person.partner_shipping_id.city
        return res  

    _columns = {
        'eq_pricelist_change': fields.boolean('Pricelist Default'),
        'eq_invoice_address': fields.function(_compute_invoice_address, string=" ", sotre=False, type="char"),
        'eq_delivery_address': fields.function(_compute_delivery_address, string=" ", sotre=False, type="char"),
        }

sale_order()

class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'  
    
    _columns = {
                }

    #Extends the standard name_search method, which is used by the many2one field. Adds a backslash plus the address type
    #at the end of the name.
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        res = super(res_partner, self).name_search(cr, uid, name, args, operator, context, limit)
        if context is None:
            context = {}
        if context.has_key('active_model'):
            partner_ids = [r[0] for r in res]
            new_res = []
            show_address = self.pool.get('ir.values').get_default(cr, uid, 'sale.order', 'default_show_address')

            for partner_id in self.browse(cr, uid, partner_ids):
                company_name = partner_id.parent_id and partner_id.parent_id.name + ' ; ' or ''
                street = partner_id.street if partner_id.street else ''
                city = partner_id.city if partner_id.city else ''
                if partner_id.is_company:
                    eq_customer_ref = '[' + str(partner_id.eq_customer_ref) + '] ' if partner_id.eq_customer_ref else ''
                    new_res.append((partner_id.id, eq_customer_ref + company_name + partner_id.name + ' / ' + _('Company') + ' // ' + street + ', ' + city))
                else:
                    type = partner_id.type
                    if partner_id.type == 'contact':
                        type = _('contact')
                    elif partner_id.type == 'invoice':
                        type = _('invoice')
                    elif partner_id.type == 'delivery':
                        type = _('delivery')
                    elif partner_id.type == 'default':
                        type = _('default')
                    elif partner_id.type == 'other':
                        type = _('other')
                    if show_address:
                        new_res.append((partner_id.id, "%s %s %s %s" % ( company_name, (partner_id.title.name if partner_id.title else ''), (partner_id.eq_firstname if partner_id.eq_firstname else ''), partner_id.name + ' / ' + type + ' // ' + street + ', ' + city)))
                    else:
                        new_res.append((partner_id.id, "%s %s %s %s" % ( company_name, (partner_id.title.name if partner_id.title else ''), (partner_id.eq_firstname if partner_id.eq_firstname else ''), partner_id.name + ' / ' + type)))
            return new_res
        return res

res_partner()

class eq_sale_configuration_address(osv.TransientModel):
    _name = 'sale.config.settings'
    _inherit = _name
    
    def set_default_values_eq(self, cr, uid, ids, context=None):
        ir_values = self.pool.get('ir.values')
        config = self.browse(cr, uid, ids[0], context)
        if config.group_sale_delivery_address:
            ir_values.set_default(cr, uid, 'sale.order', 'default_show_address', config.default_show_address or False)
        else:
            ir_values.set_default(cr, uid, 'sale.order', 'default_show_address', False)
            
                
    
    def get_default_values_eq(self, cr, uid, fields, context=None):
        notification = self.pool.get('ir.values').get_default(cr, uid, 'sale.order', 'default_show_address')
        return {
                'default_show_address': notification,
                }
    
    _columns = {
                'default_show_address': fields.boolean('Show street and city in the partner search of the saleorder', help="This adds the street and the city to the results of the partner search of the sale order"),
                }
