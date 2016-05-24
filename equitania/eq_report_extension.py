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
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import openerp.addons.decimal_precision as dp
from openerp.tools.float_utils import float_compare, float_round
import time

#Adds fields to forms that are used in the reports. Contact person and Head text

class eq_report_extension_sale_settings(osv.osv_memory):
    _inherit = 'sale.config.settings'
    
    def set_default_sale_settings_eq(self, cr, uid, ids, context=None):
        ir_values = self.pool.get('ir.values')
        config = self.browse(cr, uid, ids[0], context)
        ir_values.set_default(cr, uid, 'sale.order', 'default_use_sales_person_as_contact', config.default_use_sales_person_as_contact)
        ir_values.set_default(cr, uid, 'sale.order', 'show_delivery_date', config.default_show_delivery_date)
        ir_values.set_default(cr, uid, 'sale.order', 'use_calendar_week', config.default_use_calendar_week)
        ir_values.set_default(cr, uid, 'sale.order.line', 'eq_use_internal_description', config.default_eq_use_internal_description)
        ir_values.set_default(cr, uid, 'sale.order', 'default_use_manual_position_numbering', config.default_use_manual_position_numbering)    
        
    
    def get_default_use_sale_settings_eq(self, cr, uid, fields, context=None):
        ir_values = self.pool.get('ir.values')
        salesperson = ir_values.get_default(cr, uid, 'sale.order', 'default_use_sales_person_as_contact')
        show_delivery_date = ir_values.get_default(cr, uid, 'sale.order', 'show_delivery_date')
        use_calendar_week = ir_values.get_default(cr, uid, 'sale.order', 'use_calendar_week')
        eq_use_internal_description = ir_values.get_default(cr, uid, 'sale.order.line', 'eq_use_internal_description')
        use_manual_numbering = ir_values.get_default(cr, uid, 'sale.order', 'default_use_manual_position_numbering')
        return {
                'default_use_sales_person_as_contact': salesperson,
                'default_show_delivery_date': show_delivery_date,
                'default_use_calendar_week': use_calendar_week,
                'default_eq_use_internal_description': eq_use_internal_description,
                'default_use_manual_position_numbering': use_manual_numbering,
                }
    
    _columns = {
                'default_use_sales_person_as_contact': fields.boolean('Sale Person as Contact Person', help='Sets the Sale Person as the Contact Person in the Sale Order, only when creating.', default_model='sale.order'),
                'default_show_delivery_date': fields.boolean('Show the Delivery Date on the Sale Order [equitania]', help='The delivery date will be shown in the Sale Order', default_model='sale.order'),
                'default_use_calendar_week': fields.boolean('Show Calendar Week for Delivery Date [equitania]', help='The delivery date will be shown as a calendar week', default_model='sale.order'),
                'default_eq_use_internal_description': fields.boolean('Use internal description for sale orders [equitania]', help='The internal description will be used for sale orders not the sale description', default_model='sale.order.line'),
                'default_use_manual_position_numbering': fields.boolean('Set position numbers manually [equitania]', help='Activate to set position numbers for an order line.', default_model='sale.order'),
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
                'eq_contact_person_id': fields.many2one('hr.employee', 'Contact Person Sale', size=100),
                'eq_head_text': fields.html('Head Text'),
                'note': fields.html('Terms and conditions'),
                'show_delivery_date': fields.boolean('Show Delivery Date'),
                'use_calendar_week': fields.boolean('Use Calendar Week for Delivery Date [equitania]'),
                'eq_use_page_break_after_header': fields.boolean(string='Page break after header text'),
                }
    _defaults = {
                'eq_contact_person_id': lambda obj, cr, uid, context: obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])[0] if len(obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])) >= 1 else obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)]) or False,
                }
    
    
    #Method that is executed by the workflow
    def action_ship_create(self, cr, uid, ids, context=None):
        client_order_ref = {}
        for order in self.browse(cr, uid, ids, context):
            client_order_ref[order.name] = order.client_order_ref
        new_context = {'eq_ref_number': client_order_ref}
        return super(eq_report_extension_sale_order, self).action_ship_create(cr, uid, ids, context=new_context)
    
        """
    def action_view_invoice(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context):
            sql = "select invoice_id from sale_order_invoice_rel where order_id = " + str(order.id)
            cr.execute(sql)
            invoice_ids = cr.fetchall()
            for invoice_id in invoice_ids:
                print "invoice_id", invoice_id
                positions_ids =  self.pool.get('account.invoice.line').browse(cr, uid, invoice_id, context)
                for position in positions_ids:
                    if position.eq_pos_no == 0:
                        sale_order_line_obj = self.pool.get('sale.order.line')                     
                        print "order.id", order.id
                        print "position.product_id.id", position.product_id.id
                                          
                        #order_position_id = sale_order_line_obj.search(cr, uid, [('order_id', '=', order.id), ('product_id', '=', position.product_id.id)])
                        #order_position =  sale_order_line_obj.browse(cr, uid, order_position_id, context)
                        #print order_position
                        
                        #print "--- pos ---", order_position[0].sequence 
                        #move.eq_pos_no = order_position[0].sequence        # workaround
            
            
            #rel_id =  self.pool.get('sale.order.invoice.rel').browse(cr, uid, order.id, context)
            #print rel_id.order_id
            #print rel_id.invoice_id

        return super(eq_report_extension_sale_order, self).action_view_invoice(cr, uid, ids, context)
    """

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
            'eq_use_page_break_after_header': order.eq_use_page_break_after_header,
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
                if order_line.order_id.partner_id.eq_delivery_date_type_sale:
                    if order_line.order_id.partner_id.eq_delivery_date_type_sale == 'cw':
                        result[order_line.id] = 'KW ' + delivery_date.strftime('%V/%Y')
                    elif order_line.order_id.partner_id.eq_delivery_date_type_sale == 'date':
                        result[order_line.id] = delivery_date.strftime('%d.%m.%Y')                        
                else:
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
                'eq_use_internal_description': fields.boolean('Use internal description for sale orders'),
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
        """
            Default product_id_change handler
        """
        vals = super(eq_report_extension_sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty, uom, qty_uos, uos, name, partner_id, lang, update_tax, date_order, packaging, fiscal_position, flag, context)
        
        #Creates new dict for if not present and sets the customer language. The frozendict context can't be edited.
        context_new = {}
        if context:
            context_new = dict(context)
        
        context_new['lang'] = self.pool.get('res.partner').browse(cr, uid, partner_id, context).lang
        product_id = self.pool.get('product.product').browse(cr, uid, product, context_new)
        eq_use_internal_descriptionion = self.pool.get('ir.values').get_default(cr, uid, 'sale.order.line', 'eq_use_internal_description')
        
        vals['value']['product_uos_qty'] = qty * product_id.uos_coeff
        
        attributes = product_id.attribute_value_ids
        #print"product_attribute",product_id.attribute_value_ids.name 
        
        
        
        # set product name only after first change of quantity - it's our workaround for refresh problem after each change of quantity
        
        if vals.get("value", False):
            vals['value'].pop('name', None)
            
        if context != None and not context.get('uom_qty_change', False) and not context.get('uos_qty_change', False):
        
            attribute_values = ''
            attribute_list = [rec.name for rec in attributes]
            attribute_string = ", ".join(attribute_list)
            
                
                
        #if name is False:                   # name is set, don't reset it again !           
            if not eq_use_internal_descriptionion and product_id.description_sale:
                vals['value']['name'] = product_id.description_sale + "\n" + attribute_string
            elif eq_use_internal_descriptionion and product_id.description:
                vals['value']['name'] = product_id.product_tmpl_id.description  + "\n" + attribute_string
            else:
                vals['value']['name'] = ' '
        
        vals['value']['delay'] = product_id.sale_delay
        return vals
    
class eq_report_extension_purchase_order(osv.osv):
    _inherit = "purchase.order"
    _columns = {
                'eq_contact_person_id': fields.many2one('hr.employee', 'Contact Person', size=100),
                'eq_head_text': fields.html('Head Text'),
                #'note': fields.html('Terms and conditions'),#hinzugefügt 16.12.; Ticket 1861
                'show_delivery_date': fields.boolean('Show the Delivery Date'),
                'use_calendar_week': fields.boolean('Use Calendar Week for Delivery Date [equitania]'),
                'notes': fields.html('Terms and conditions'),
                'eq_use_page_break_after_header': fields.boolean(string='Page break after header text'),
                }
    _defaults = {
                'eq_contact_person_id': lambda obj, cr, uid, context: obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])[0] if len(obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])) >= 1 else obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)]) or False
                }
    
    
    #16.12.2015
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
    
class eq_report_extension_invoice(osv.osv):
    _inherit = "account.invoice"
    
    _columns = {
                'eq_contact_person_id': fields.many2one('hr.employee', 'Contact Person', size=100),
                'eq_head_text': fields.html('Head Text'),
                'eq_ref_number': fields.char('Sale Order Referenc', size=64),
                'eq_delivery_address': fields.many2one('res.partner', 'Delivery Address'),
                'comment': fields.html('Additional Information'),
                'eq_use_page_break_after_header': fields.boolean(string='Page break after header text'),
                }
    _defaults = {
                'eq_contact_person_id': lambda obj, cr, uid, context: obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])[0] if len(obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])) >= 1 else obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)]) or False,
                'eq_head_text': lambda obj, cr, uid, context: obj.pool.get('ir.config_parameter').get_param(cr, uid, "eq.head.text.invoice"),
                'comment': lambda obj, cr, uid, context: obj.pool.get('ir.config_parameter').get_param(cr, uid, "eq.foot.text.invoice"), 
                }
    
class eq_report_extension_invoice(osv.osv):
    """
     Small extension of standard functionality.
     - added new field eq_pos_no as a container for sequence no from contract (AB). we'll use this information as pos on delivery note and invoice 
    """
    
    _inherit = "account.invoice.line"
    
    _order = "sequence"
    
    _columns = {
                'eq_delivery_date': fields.date('Delivery Date'),
                'eq_move_id': fields.many2one('stock.move'),
                'eq_pos_no' : fields.integer('Seq')
                }
    
    def create(self, cr, user, vals, context={}):    
        """
            let's get original sequence no from deliverynote and save it for every position on delivery note
            @cr: cursor
            @use: actual user
            @vals: alle values to be saved
            @context: context
        """
        if vals.get('eq_move_id'):
            move_id = vals["eq_move_id"] 
            
            # get corresponding sequence no for our positions
            result_id = self.pool.get('stock.move').browse(cr, user, move_id, context)    
            
            # save sequence into our new field    
            vals["eq_pos_no"] = result_id.eq_pos_no
            
            #neu: Sequenz für Invoiceline
            vals["sequence"] = result_id.eq_pos_no

        # use standard save functionality and save it
        return super(eq_report_extension_invoice, self).create(cr, user, vals, context)
    
        
class eq_report_extension_stock_picking(osv.osv):
    _inherit = "stock.picking"
    
    _columns = {
                'eq_ref_number': fields.char('Sale Order Referenc', size=64),
                }
    
    def get_setting(self, cr, uid, settingName):
        """
            Get value of actual setting
            @cr:
            @uid:
            @settingName:
            @return:
        """
        result = self.pool.get('ir.config_parameter').get_param(cr, uid, settingName)
        if result == "":
            return None            
        return result
    
    
    #Adds the customer ref number to the picking list. Gets data from context which is set in the method action_ship_create of the sale.order
    def create(self, cr, user, vals, context={}):
        if context:
            if context.get('eq_ref_number', False):
                vals['eq_ref_number'] = context['eq_ref_number'].get(vals['origin'], False)
        return super(eq_report_extension_stock_picking, self).create(cr, user, vals, context)
    
    #Adds the customer ref number to the invoice (Create from picking list)
    def _create_invoice_from_picking(self, cr, uid, picking, vals, context=None):    
        #vals['eq_ref_number'] = picking.eq_ref_number
        vals['eq_delivery_address'] = picking.partner_id.id
        
        head_text = ''
        comment = ''
        if (picking.move_lines):
            if (picking.move_lines[0].procurement_id and picking.move_lines[0].procurement_id.sale_line_id):
                head_text = picking.move_lines[0].procurement_id.sale_line_id.order_id.eq_head_text
                comment = picking.move_lines[0].procurement_id.sale_line_id.order_id.note
            elif (picking.move_lines[0].purchase_line_id):
                head_text = picking.move_lines[0].purchase_line_id[0].order_id.eq_head_text
                comment = picking.move_lines[0].purchase_line_id[0].order_id.notes
        
        # Original version implemented by Artur
        """
        vals['eq_head_text'] = head_text
        vals['comment'] = comment
        """
        
        # New version implemented by Sody
        head = self.get_setting(cr, uid, "eq.head.text.invoice")
        if head is not None:
            vals['eq_head_text'] = head
        
        foot = self.get_setting(cr, uid, "eq.foot.text.invoice")
        if foot is not None:
            vals['comment'] = foot
                
        #picking.move_lines[0].purchase_line_id[0].order_id.eq_head_text
        #picking.move_lines[0].procurement_id.sale_line_id.order_id
        
        
        return super(eq_report_extension_stock_picking, self)._create_invoice_from_picking(cr, uid, picking, vals, context)
    
    
    def _invoice_create_line(self, cr, uid, moves, journal_id, inv_type='out_invoice', context=None):
        invoice_obj = self.pool.get('account.invoice')
        
        invoice_ids = super(eq_report_extension_stock_picking, self)._invoice_create_line(cr, uid, moves, journal_id, inv_type=inv_type, context=context)
        invoices = invoice_obj.browse(cr, uid, invoice_ids, context=context)
        
        for invoice in invoices:
            ref_numbers = set([x.eq_move_id.picking_id.eq_ref_number for x in invoice.invoice_line if x.eq_move_id and x.eq_move_id.picking_id.eq_ref_number])
            invoice_obj.write(cr, uid, invoice.id, {'eq_ref_number': ", ".join(ref_numbers)})
        return invoice_ids
    
    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        res = super(eq_report_extension_stock_picking, self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move, context)
        res['name'] = move.picking_id.origin
        return res
    
    
    
class eq_stock_move_extension(osv.osv):
    """
     Small extension of standard functionality.
     - added new field eq_pos_no as a container for sequence no from sale order (AB). we'll use this information as pos on delivery note and invoice 
    """
    
    _inherit = "stock.move"
        
    _order = "eq_pos_no"
    
    _columns = {
                'eq_pos_no' : fields.integer('Seq')
                }
    
    def create(self, cr, uid, vals, context={}):        
        """
            let's get original sequence no from contract and save it for every position on delivery note
            @cr: cursor
            @use: actual user
            @vals: alle values to be saved
            @context: context
        """
        if vals.get('procurement_id', False):
            procurement = self.pool.get('procurement.order').browse(cr, uid, vals["procurement_id"], context)
                    
            if hasattr(procurement, 'sale_line_id'):
                # save sequence into our new field
                vals["eq_pos_no"] = procurement.sale_line_id.sequence
        
        # use standard save functionality and save it
        return super(eq_stock_move_extension, self).create(cr, uid, vals, context)
    
    def action_done(self, cr, uid, ids, context=None):
        """ Process completely the moves given as ids and if all moves are done, it will finish the picking.
        """
        
        context = context or {}
        picking_obj = self.pool.get("stock.picking")
        quant_obj = self.pool.get("stock.quant")
        todo = [move.id for move in self.browse(cr, uid, ids, context=context) if move.state == "draft"]
        if todo:
            ids = self.action_confirm(cr, uid, todo, context=context)
        pickings = set()
        procurement_ids = []
        #Search operations that are linked to the moves
        operations = set()
        move_qty = {}
        for move in self.browse(cr, uid, ids, context=context):
            move_qty[move.id] = move.product_qty
            for link in move.linked_move_operation_ids:
                operations.add(link.operation_id)

        #Sort operations according to entire packages first, then package + lot, package only, lot only
        operations = list(operations)
        operations.sort(key=lambda x: ((x.package_id and not x.product_id) and -4 or 0) + (x.package_id and -2 or 0) + (x.lot_id and -1 or 0))

        for ops in operations:
            if ops.picking_id:
                pickings.add(ops.picking_id.id)
            main_domain = [('qty', '>', 0)]
            for record in ops.linked_move_operation_ids:
                move = record.move_id
                self.check_tracking(cr, uid, move, not ops.product_id and ops.package_id.id or ops.lot_id.id, context=context)
                prefered_domain = [('reservation_id', '=', move.id)]
                fallback_domain = [('reservation_id', '=', False)]
                fallback_domain2 = ['&', ('reservation_id', '!=', move.id), ('reservation_id', '!=', False)]
                prefered_domain_list = [prefered_domain] + [fallback_domain] + [fallback_domain2]
                dom = main_domain + self.pool.get('stock.move.operation.link').get_specific_domain(cr, uid, record, context=context)
                quants = quant_obj.quants_get_prefered_domain(cr, uid, ops.location_id, move.product_id, record.qty, domain=dom, prefered_domain_list=prefered_domain_list,
                                                          restrict_lot_id=move.restrict_lot_id.id, restrict_partner_id=move.restrict_partner_id.id, context=context)
                if ops.product_id:
                    #If a product is given, the result is always put immediately in the result package (if it is False, they are without package)
                    quant_dest_package_id  = ops.result_package_id.id
                    ctx = context
                else:
                    # When a pack is moved entirely, the quants should not be written anything for the destination package
                    quant_dest_package_id = False
                    ctx = context.copy()
                    ctx['entire_pack'] = True
                quant_obj.quants_move(cr, uid, quants, move, ops.location_dest_id, location_from=ops.location_id, lot_id=ops.lot_id.id, owner_id=ops.owner_id.id, src_package_id=ops.package_id.id, dest_package_id=quant_dest_package_id, context=ctx)

                # Handle pack in pack
                if not ops.product_id and ops.package_id and ops.result_package_id.id != ops.package_id.parent_id.id:
                    self.pool.get('stock.quant.package').write(cr, SUPERUSER_ID, [ops.package_id.id], {'parent_id': ops.result_package_id.id}, context=context)
                if not move_qty.get(move.id):
                    continue
                    #old raise osv.except_osv(_("Error"), _("The roundings of your Unit of Measures %s on the move vs. %s on the product don't allow to do these operations or you are not transferring the picking at once. ") % (move.product_uom.name, move.product_id.uom_id.name))
                move_qty[move.id] -= record.qty
        #Check for remaining qtys and unreserve/check move_dest_id in
        move_dest_ids = set()
        for move in self.browse(cr, uid, ids, context=context):
            move_qty_cmp = float_compare(move_qty[move.id], 0, precision_rounding=move.product_id.uom_id.rounding)
            if move_qty_cmp > 0:  # (=In case no pack operations in picking)
                main_domain = [('qty', '>', 0)]
                prefered_domain = [('reservation_id', '=', move.id)]
                fallback_domain = [('reservation_id', '=', False)]
                fallback_domain2 = ['&', ('reservation_id', '!=', move.id), ('reservation_id', '!=', False)]
                prefered_domain_list = [prefered_domain] + [fallback_domain] + [fallback_domain2]
                self.check_tracking(cr, uid, move, move.restrict_lot_id.id, context=context)
                qty = move_qty[move.id]
                quants = quant_obj.quants_get_prefered_domain(cr, uid, move.location_id, move.product_id, qty, domain=main_domain, prefered_domain_list=prefered_domain_list, restrict_lot_id=move.restrict_lot_id.id, restrict_partner_id=move.restrict_partner_id.id, context=context)
                quant_obj.quants_move(cr, uid, quants, move, move.location_dest_id, lot_id=move.restrict_lot_id.id, owner_id=move.restrict_partner_id.id, context=context)

            # If the move has a destination, add it to the list to reserve
            if move.move_dest_id and move.move_dest_id.state in ('waiting', 'confirmed'):
                move_dest_ids.add(move.move_dest_id.id)

            if move.procurement_id:
                procurement_ids.append(move.procurement_id.id)

            #unreserve the quants and make them available for other operations/moves
            quant_obj.quants_unreserve(cr, uid, move, context=context)
        procurement_ids = list(set(procurement_ids))
        # Check the packages have been placed in the correct locations
        self._check_package_from_moves(cr, uid, ids, context=context)
        #set the move as done
        self.write(cr, uid, ids, {'state': 'done', 'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)}, context=context)
        self.pool.get('procurement.order').check(cr, uid, procurement_ids, context=context)
        #assign destination moves
        if move_dest_ids:
            self.action_assign(cr, uid, list(move_dest_ids), context=context)
        #check picking state to set the date_done is needed
        done_picking = []
        for picking in picking_obj.browse(cr, uid, list(pickings), context=context):
            if picking.state == 'done' and not picking.date_done:
                done_picking.append(picking.id)
        if done_picking:
            picking_obj.write(cr, uid, done_picking, {'date_done': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)}, context=context)
        return True
    
class eq_compatibility_equitania_inox(osv.osv):
    _inherit = 'res.partner'
    _name = _inherit
    
    def _show_deb_cred_number(self, cr, uid, ids, name, arg, context={}):
        result = {}
        for partner in self.browse(cr, uid, ids, context):
            deb_cred = False
            if partner.eq_customer_ref != 'False' and partner.eq_customer_ref and partner.eq_creditor_ref != 'False' and partner.eq_creditor_ref:
                deb_cred = partner.eq_customer_ref + ' / ' + partner.eq_creditor_ref
            elif partner.eq_customer_ref != 'False' and partner.eq_customer_ref:
                deb_cred = partner.eq_customer_ref
            elif partner.eq_creditor_ref != 'False' and partner.eq_creditor_ref:
                deb_cred = partner.eq_creditor_ref
            result[partner.id] = deb_cred
            
        return result
        
    _columns = {
                'eq_deb_cred_number': fields.function(_show_deb_cred_number, type='char', store=False)
                }
