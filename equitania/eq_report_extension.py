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
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT

#Adds fields to forms that are used in the reports. Contact person and Head text

class eq_report_extension_sale_settings(osv.osv_memory):
    _inherit = 'sale.config.settings'
    
    def set_default_sale_settings_eq(self, cr, uid, ids, context=None):
        ir_values = self.pool.get('ir.values')
        config = self.browse(cr, uid, ids[0], context)
        ir_values.set_default(cr, uid, 'sale.order', 'default_use_sales_person_as_contact', config.default_use_sales_person_as_contact)
        ir_values.set_default(cr, uid, 'sale.order', 'show_delivery_date', config.default_show_delivery_date)
        ir_values.set_default(cr, uid, 'sale.order', 'use_calendar_week', config.default_use_calendar_week)
            
        
    
    def get_default_use_sale_settings_eq(self, cr, uid, fields, context=None):
        ir_values = self.pool.get('ir.values')
        salesperson = ir_values.get_default(cr, uid, 'sale.order', 'default_use_sales_person_as_contact')
        show_delivery_date = ir_values.get_default(cr, uid, 'sale.order', 'show_delivery_date')
        use_calendar_week = ir_values.get_default(cr, uid, 'sale.order', 'use_calendar_week')
        return {
                'default_use_sales_person_as_contact': salesperson,
                'default_show_delivery_date': show_delivery_date,
                'default_use_calendar_week': use_calendar_week,
                }
    
    _columns = {
                'default_use_sales_person_as_contact': fields.boolean('Sale Person as Contact Person', help='Sets the Sale Person as the Contact Person in the Sale Order, only when creating.', default_model='sale.order'),
                'default_show_delivery_date': fields.boolean('Show the Delivery Date on the Sale Order [equitania]', help='The delivery date will be shown in the Sale Order', default_model='sale.order'),
                'default_use_calendar_week': fields.boolean('Show Calendar Week for Delivery Date [equitania]', help='The delivery date will be shown as a calendar week', default_model='sale.order'),
                }

class eq_report_extension_purchase_settings(osv.osv_memory):
    _inherit = 'purchase.config.settings'   
     
    def set_default_sale_settings_eq(self, cr, uid, ids, context=None):
        ir_values = self.pool.get('ir.values')
        config = self.browse(cr, uid, ids[0], context)
        ir_values.set_default(cr, uid, 'purchase.order', 'show_delivery_date', config.default_show_delivery_date)
        ir_values.set_default(cr, uid, 'purchase.order', 'use_calendar_week', config.default_use_calendar_week)
    
    def get_default_use_sale_settings_eq(self, cr, uid, fields, context=None):
        ir_values = self.pool.get('ir.values')
        show_delivery_date = ir_values.get_default(cr, uid, 'purchase.order', 'show_delivery_date')
        use_calendar_week = ir_values.get_default(cr, uid, 'purchase.order', 'use_calendar_week')
        return {
                'default_show_delivery_date': show_delivery_date,
                'default_use_calendar_week': use_calendar_week,
                }
    
    _columns = {
                'default_show_delivery_date': fields.boolean('Show the Delivery Date on the Purchase Order [equitania]', help='The delivery date will be shown in the Purchase Order', default_model='purchase.order'),
                'default_use_calendar_week': fields.boolean('Show Calendar Week for Delivery Date [equitania]', help='The delivery date will be shown as a calendar week ', default_model='purchase.order'),
                }
    
    
class eq_report_extension_sale_order(osv.osv):
    _inherit = "sale.order"
        
    _columns = {
                'eq_contact_person_id': fields.many2one('hr.employee', 'Contact Person', size=100),
                'eq_head_text': fields.text('Head Text'),
                'show_delivery_date': fields.boolean('Show Delivery Date'),
                'use_calendar_week': fields.boolean('Use Calendar Week for Delivery Date [equitania]'),
                }
    _defaults = {
                'eq_contact_person_id': lambda obj, cr, uid, context: obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])[0] if len(obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])) >= 1 else obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)]) or False,
                }
    

    def action_ship_create(self, cr, uid, ids, context=None):
        client_order_ref = {}
        for order in self.browse(cr, uid, ids, context):
            client_order_ref[order.name] = order.client_order_ref
        new_context = {'eq_ref_number': client_order_ref}
        return super(eq_report_extension_sale_order, self).action_ship_create(cr, uid, ids, context=new_context)
    
    def create(self, cr, uid, values, context=None):
        use_sale_person = self.pool.get('ir.values').get_default(cr, uid, 'sale.order', 'default_use_sales_person_as_contact')
        
        if use_sale_person and values.get('user_id', False) and not values.get('eq_contact_person_id', False):
            emp_search = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', values['user_id'])])
            values['eq_contact_person_id'] = emp_search[0] if len(emp_search) >= 1 else emp_search
        
        return super(eq_report_extension_sale_order, self).create(cr, uid, values, context)
    
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
         
        """Prepare the dict of values to create the new invoice for a
           sales order. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record order: sale.order record to invoice
           :param list(int) line: list of invoice line IDs that must be
                                  attached to the invoice
           :return: dict of value to create() the invoice
        """
        
        invoice_vals = super(eq_report_extension_sale_order, self)._prepare_invoice(cr, uid, order, lines, context)
        if context is None:
            context = {}
        journal_ids = self.pool.get('account.journal').search(cr, uid,
            [('type', '=', 'sale'), ('company_id', '=', order.company_id.id)],
            limit=1)
        if not journal_ids:
            raise osv.except_osv(_('Error!'),
                _('Please define sales journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
        invoice_vals = {
            'name': order.name,
            'origin': order.name or False,
            'type': 'out_invoice',
            'reference': order.client_order_ref or order.name,
            'account_id': order.partner_id.property_account_receivable.id,
            'partner_id': order.partner_invoice_id.id,
            'journal_id': journal_ids[0],
            'invoice_line': [(6, 0, lines)],
            'currency_id': order.pricelist_id.currency_id.id,
            'comment': order.note,
            'payment_term': order.payment_term and order.payment_term.id or False,
            'fiscal_position': order.fiscal_position.id or order.partner_id.property_account_position.id,
            'date_invoice': context.get('date_invoice', False),
            'company_id': order.company_id.id,
            'user_id': order.user_id and order.user_id.id or False,
            'section_id': order.section_id.id,
            'eq_contact_person_id': order.eq_contact_person_id.id,
            'eq_head_text': order.eq_head_text,
        }
        return invoice_vals
    
    #Method which creates an invoice out of the sale order. Sets the customer ref number
    def _make_invoice(self, cr, uid, order, lines, context=None):
        # get the invoice
        inv_obj = self.pool.get('account.invoice')
        # create the invoice
        inv_id = super(eq_report_extension_sale_order, self)._make_invoice(cr, uid, order, lines, context)
        # modify the invoice
        inv_obj.write(cr, uid, [inv_id], {'eq_ref_number': order.client_order_ref, 'eq_delivery_address': order.partner_shipping_id.id}, context)
        inv_obj.button_compute(cr, uid, [inv_id])
        return inv_id
    
    def action_invoice_create(self, cr, uid, ids, grouped=False, states=None, date_invoice = False, context=None):
        inv_id = super(eq_report_extension_sale_order, self).action_invoice_create(cr, uid, ids, grouped, states,date_invoice, context)
        order = self.browse(cr, uid, ids, context)
        for inv in inv_id if isinstance(inv_id, list) else [inv_id]:
            self.pool.get('account.invoice').write,(cr, uid, inv, {'eq_ref_number': order.origin, 'eq_delivery_address': order.partner_shipping_id.id})
        return inv_id

class eq_report_extension_sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    
    def _get_delivery_date(self, cr, uid, ids, field_name, arg, context):
        result = {}
        for order_line in self.browse(cr, uid, ids, context):
            if order_line.order_id.show_delivery_date and order_line.eq_delivery_date:
                delivery_date = datetime.strptime(order_line.eq_delivery_date, OE_DFORMAT)
                if order_line.order_id.use_calendar_week:
                    result[order_line.id] = 'KW ' + delivery_date.strftime('%V/%Y')
                else:
                    result[order_line.id] = delivery_date.strftime('%d.%m.%Y')
            else:
                result[order_line.id] = False
        
        return result

    _columns = {
                'get_delivery_date': fields.function(_get_delivery_date, string="Delivery", type='char', methode=True, store=False),
                'eq_delivery_date': fields.date('Delivery Date'),
                }
    
    def on_change_delivery_date(self, cr, uid, ids, date_order, eq_delivery_date, context={}):
        values = {}
        if date_order and eq_delivery_date:
            date_order = datetime.strptime(date_order.split(' ')[0], OE_DFORMAT)
            eq_delivery_date = datetime.strptime(eq_delivery_date, OE_DFORMAT)
            
            delay = (eq_delivery_date - date_order).days
            
            values = {'delay': delay}
        return {'value': values,}
    
    def on_change_delay(self, cr, uid, ids, date_order, delay, context={}):
        values = {}
        if date_order and delay:
            date_order = datetime.strptime(date_order.split(' ')[0], OE_DFORMAT)
            eq_delivery_date = date_order + timedelta(days=int(delay))
            values = {
                      'eq_delivery_date': eq_delivery_date
                      }
        return {'value': values,}
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        
        vals = super(eq_report_extension_sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty, uom, qty_uos, uos, name, partner_id, lang, update_tax, date_order, packaging, fiscal_position, flag, context)
        #Creates new dict for if not present and sets the customer language. The frozendict context can't be edited.
        context_new = {}
        if context:
            context_new = dict(context)
        context_new['lang'] = self.pool.get('res.partner').browse(cr, uid, partner_id, context).lang
        product_id = self.pool.get('product.product').browse(cr, uid, product, context_new)
        
        if product_id.description_sale:
            vals['value']['name'] = product_id.description_sale
        else:
            vals['value']['name'] = product_id.name
        vals['value']['delay'] = product_id.sale_delay
        return vals
    
class eq_report_extension_purchase_order(osv.osv):
    _inherit = "purchase.order"
    _columns = {
                'eq_contact_person_id': fields.many2one('hr.employee', 'Contact Person', size=100),
                'eq_head_text': fields.text('Head Text'),
                'show_delivery_date': fields.boolean('Show the Delivery Date'),
                'use_calendar_week': fields.boolean('Use Calendar Week for Delivery Date [equitania]'),
                }
    _defaults = {
                'eq_contact_person_id': lambda obj, cr, uid, context: obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])[0] if len(obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])) >= 1 else obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)]) or False
                }
    
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
            vals['value']['name'] = product.name
        return vals
    
    def _get_delivery_date(self, cr, uid, ids, field_name, arg, context):
        result = {}
        
        for purchase_line in self.browse(cr, uid, ids, context):
            if purchase_line.order_id.show_delivery_date and purchase_line.date_planned:
                delivery_date = datetime.strptime(purchase_line.date_planned, OE_DFORMAT)
                if purchase_line.order_id.use_calendar_week:
                    result[purchase_line.id] = 'KW ' + delivery_date.strftime('%V/%Y')
                else:
                    result[purchase_line.id] = delivery_date.strftime('%d.%m.%Y')
            else:
                result[purchase_line.id] = False
        
        return result

    _columns = {
                'get_delivery_date': fields.function(_get_delivery_date, string="Delivery", type='char', methode=True, store=False),
                }
    
class eq_report_extension_invoice(osv.osv):
    _inherit = "account.invoice"
    
    _columns = {
                'eq_contact_person_id': fields.many2one('hr.employee', 'Contact Person', size=100),
                'eq_head_text': fields.text('Head Text'),
                'eq_ref_number': fields.char('Sale Order Referenc', size=64),
                'eq_delivery_address': fields.many2one('res.partner', 'Delivery Address'),
                }
    _defaults = {
                'eq_contact_person_id': lambda obj, cr, uid, context: obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])[0] if len(obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])) >= 1 else obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)]) or False 
                }
    
class eq_report_extension_invoice(osv.osv):
    _inherit = "account.invoice.line"
    
    _columns = {
                'eq_delivery_date': fields.date('Delivery Date'),
                'eq_move_id': fields.many2one('stock.move'),
                }
    
        
class eq_report_extension_stock_picking(osv.osv):
    _inherit = "stock.picking"
    
    _columns = {
                'eq_ref_number': fields.char('Sale Order Referenc', size=64),
                }
    
    #Adds the customer ref number to the picking list. Gets data from context which is set in the method action_ship_create of the sale.order
    def create(self, cr, user, vals, context={}):
        if context.get('eq_ref_number', False):
            vals['eq_ref_number'] = context['eq_ref_number'].get(vals['origin'], False)
        return super(eq_report_extension_stock_picking, self).create(cr, user, vals, context)
    
    #Adds the customer ref number to the invoice (Create from picking list)
    def _create_invoice_from_picking(self, cr, uid, picking, vals, context=None):
        vals['eq_ref_number'] = picking.eq_ref_number
        vals['eq_delivery_address'] = picking.partner_id.id
        return super(eq_report_extension_stock_picking, self)._create_invoice_from_picking(cr, uid, picking, vals, context)
    
    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        res = super(eq_report_extension_stock_picking, self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move, context)
        res['name'] = move.picking_id.origin
        return res
    
class eq_compatibility_equitania_inox(osv.osv):
    _inherit = 'res.partner'
    _name = _inherit
    
    def _show_deb_cred_number(self, cr, uid, ids, name, arg, context={}):
        result = {}
        for partner in self.browse(cr, uid, ids, context):
            deb_cred = False
            if partner.eq_customer_ref and partner.eq_creditor_ref:
                deb_cred = partner.eq_customer_ref + ' / ' + partner.eq_creditor_ref
            elif partner.eq_customer_ref:
                deb_cred = partner.eq_customer_ref
            elif partner.eq_creditor_ref:
                deb_cred = partner.eq_creditor_ref
            result[partner.id] = deb_cred
            
        return result
        
    _columns = {
                'eq_deb_cred_number': fields.function(_show_deb_cred_number, type='char', store=False)
                }