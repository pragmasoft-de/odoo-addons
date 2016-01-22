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
import openerp.addons.decimal_precision as dp

class purchase_order(osv.osv):
    _inherit = 'purchase.order'
        
    def _compute_street_house_no(self, cr, uid, ids, field_name, arg, context):
        """ Generate street and house no info for purchase order """
                
        res = {}
        for person in self.browse(cr, uid, ids):
            if person.partner_id.street and person.partner_id.eq_house_no:                
                    res[person.id] = person.partner_id.street + ' ' + person.partner_id.eq_house_no
            elif person.partner_id.street:                                
                    res[person.id] = person.partner_id.street
            else:
                res[person.id] = False
                
        return res
        
    def _compute_zip_city(self, cr, uid, ids, field_name, arg, context):
        """ Generate zip and city info for purchase order """
                
        res = {}
        for person in self.browse(cr, uid, ids):
            if person.partner_id.zip and person.partner_id.city:                
                    res[person.id] = person.partner_id.zip + ' ' + person.partner_id.city
            elif person.partner_id.zip:                                
                    res[person.id] = person.partner_id.zip
            elif person.partner_id.city:                                
                    res[person.id] = person.partner_id.city
            else:
                res[person.id] = False
                
        return res
    
    def _compute_country(self, cr, uid, ids, field_name, arg, context):
        """ Generate country info for purchase order """
        res = {}
        for person in self.browse(cr, uid, ids, context):
            if person.partner_id.country_id:
                    res[person.id] = person.partner_id.country_id.name           
            else:
                res[person.id] = False
                
        return res
    
    
    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        """
            Extension of standard function onchange_partner_id(...) which adds eq_foreign_ref as partner_ref  to result values
            
            @cr: cursor
            @uid: user id
            @ids: ids
            @partner_id: partner id
            @context: context
            @return: original values together with eq_foreign_ref stored in partner_ref
        """        
        original_values = super(eq_purchase_order, self).onchange_partner_id(cr, uid, ids, partner_id, context=context)
        if partner_id:
            partner = self.pool.get('res.partner')
            supplier = partner.browse(cr, uid, partner_id, context=context)            
            original_values['value']['partner_ref'] = supplier.eq_foreign_ref
        
        return original_values
    
    
    def _prepare_invoice(self, cr, uid, order, line_ids, context=None):
        """Prepare the dict of values to create the new invoice for a
           purchase order. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record order: purchase.order record to invoice
           :param list(int) line_ids: list of invoice line IDs that must be
                                      attached to the invoice
           :return: dict of value to create() the invoice
        """
        
        invoice_vals = super(eq_report_extension_purchase_order, self)._prepare_invoice(cr, uid, order, line_ids, context)
        
        #=======================================================================
        # journal_ids = self.pool['account.journal'].search(
        #                     cr, uid, [('type', '=', 'purchase'),
        #                               ('company_id', '=', order.company_id.id)],
        #                     limit=1)
        # if not journal_ids:
        #     raise osv.except_osv(
        #         _('Error!'),
        #         _('Define purchase journal for this company: "%s" (id:%d).') % \
        #             (order.company_id.name, order.company_id.id))
        #=======================================================================
        
        invoice_vals['eq_contact_person_id'] = order.eq_contact_person_id.id
        invoice_vals['eq_head_text'] = order.eq_head_text
        invoice_vals['comment'] = order.notes
        
        return invoice_vals
    
    #16.12.2015
    def action_invoice_create(self, cr, uid, ids, context=None):
        """Generates invoice for given ids of purchase orders and links that invoice ID to purchase order.
        :param ids: list of ids of purchase orders.
        :return: ID of created invoice.
        :rtype: int
        """
        #TODO
        return super(eq_report_extension_purchase_order, self).action_invoice_create(cr, uid, ids, context)
    
    
    _columns = {
                'eq_street_house_no': fields.function(_compute_street_house_no, string=" ", store=False, type="char"),
                'eq_zip_city': fields.function(_compute_zip_city, string=" ", store=False, type="char"),
                'eq_country': fields.function(_compute_country, string=" ", store=False, type="char"),
                'eq_contact_person_id': fields.many2one('hr.employee', 'Contact Person', size=100),
                'eq_head_text': fields.html('Head Text'),
                'show_delivery_date': fields.boolean('Show the Delivery Date'),
                'use_calendar_week': fields.boolean('Use Calendar Week for Delivery Date [equitania]'),
                'notes': fields.html('Terms and conditions'),
                }
    
    _defaults = {
               'eq_contact_person_id': lambda obj, cr, uid, context: obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])[0] if len(obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])) >= 1 else obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)]) or False
                }

purchase_order()


class eq_report_extension_purchase_order_line(osv.osv):
    _inherit = "purchase.order.line"

    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, state='draft', context=None):
        
        vals = super(eq_report_extension_purchase_order_line, self).onchange_product_id(cr, uid, ids, pricelist_id, product_id, qty, uom_id, partner_id, date_order, fiscal_position_id, date_planned, name, price_unit, state, context)
        #Creates new dict for if not present and sets the customer language. The frozendict context can't be edited.
        context_new = {}
        if context:
            context_new = dict(context)
        context_new['lang'] = self.pool.get('res.partner').browse(cr, uid, partner_id, context).lang
        product = self.pool.get('product.product').browse(cr, uid, product_id, context_new)
        if product.description_purchase:
            vals['value']['name'] = product.description_purchase
        else:
            vals['value']['name'] = ' '
        return vals
    
    def _get_delivery_date(self, cr, uid, ids, field_name, arg, context):
        result = {}
        
        for purchase_line in self.browse(cr, uid, ids, context):
            if purchase_line.order_id.show_delivery_date and purchase_line.date_planned:
                delivery_date = datetime.strptime(purchase_line.date_planned, OE_DFORMAT)
                if purchase_line.order_id.partner_id.eq_delivery_date_type_purchase:
                    if purchase_line.order_id.partner_id.eq_delivery_date_type_purchase == 'cw':
                        result[purchase_line.id] = 'KW ' + delivery_date.strftime('%V/%Y')
                    else:
                        purchase_line.order_id.partner_id.eq_delivery_date_type_purchase == 'date'
                        result[purchase_line.id] = delivery_date.strftime('%d.%m.%Y')                    
                else:
                    if purchase_line.order_id.use_calendar_week:
                        result[purchase_line.id] = 'KW ' + delivery_date.strftime('%V/%Y')
                    else:
                        result[purchase_line.id] = delivery_date.strftime('%d.%m.%Y')
            else:
                result[purchase_line.id] = False
        
        return result

    _columns = {
                'get_delivery_date': fields.function(_get_delivery_date, string="Delivery", type='char', methode=True, store=False),
                'price_unit': fields.float('Unit Price', required=True, digits_compute= dp.get_precision('Product Price Purchase')),
                'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Quantity Purchase'), required=True),
                }