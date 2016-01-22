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
    
    def _compute_invoice_address(self, cr, uid, ids, field_name, arg, context):
        """ Generate address infos for sale order """
        
        res = {}
        for person in self.browse(cr, uid, ids):
            zip = ""
            if person.partner_shipping_id.zip:
                zip = person.partner_shipping_id.zip
                
            if person.partner_invoice_id.street and person.partner_invoice_id.city:
                if person.partner_invoice_id.eq_house_no:
                    res[person.id] = person.partner_invoice_id.street + ' ' + person.partner_invoice_id.eq_house_no + ', @ZIP ' + person.partner_invoice_id.city
                else:                                
                    res[person.id] = person.partner_invoice_id.street + ', @ZIP ' + person.partner_invoice_id.city
            elif person.partner_invoice_id.street:
                if person.partner_invoice_id.eq_house_no:
                    res[person.id] = person.partner_invoice_id.street + ' ' + person.partner_invoice_id.eq_house_no
                else:
                    res[person.id] = person.partner_invoice_id.street
            elif person.partner_invoice_id.city:
                res[person.id] = person.partner_invoice_id.city
            else:
                res[person.id] = False
                
            if res[person.id] is not False:
                result = res[person.id]
                result = result.replace("@ZIP", zip)
                res[person.id] = result
            
        return res
    
    def _compute_delivery_address(self, cr, uid, ids, field_name, arg, context):
        """ Generate address infos for sale order """
        
        res = {}
        
        for person in self.browse(cr, uid, ids):
            zip = ""
            if person.partner_shipping_id.zip:
                zip = person.partner_shipping_id.zip
                
            if person.partner_shipping_id.street and person.partner_shipping_id.city:
                if person.partner_shipping_id.eq_house_no:
                    res[person.id] = person.partner_shipping_id.street + ' ' + person.partner_shipping_id.eq_house_no + ', @ZIP ' + person.partner_shipping_id.city
                else:
                    res[person.id] = person.partner_shipping_id.street + ', @ZIP ' + person.partner_shipping_id.city
            elif person.partner_shipping_id.street:
                if person.partner_shipping_id.eq_house_no:                
                    res[person.id] = person.partner_shipping_id.street + ' ' + person.partner_shipping_id.eq_house_no
                else:
                    res[person.id] = person.partner_shipping_id.street
            elif person.partner_shipping_id.city:
                res[person.id] = person.partner_shipping_id.city
            else:
                res[person.id] = False
                
            if res[person.id] is not False:
                result = res[person.id]
                result = result.replace("@ZIP", zip)
                res[person.id] = result

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
        original_values = super(eq_sale_order, self).onchange_partner_id(cr, uid, ids, partner_id, context=context)
        
        if partner_id:
            partner = self.pool.get('res.partner')
            customer = partner.browse(cr, uid, partner_id, context=context)   
            original_values['value']['client_order_ref'] = customer.eq_foreign_ref
        
        return original_values 
    
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

    _columns = {
                'eq_pricelist_change': fields.boolean('Pricelist Default'),
                'eq_invoice_address': fields.function(_compute_invoice_address, string=" ", store=False, type="char"),
                'eq_delivery_address': fields.function(_compute_delivery_address, string=" ", store=False, type="char"),
                'client_order_ref': fields.char('Reference/Description', copy=True),
                'eq_street_house_no': fields.function(_compute_street_house_no, string=" ", store=False, type="char"),
                'eq_zip_city': fields.function(_compute_zip_city, string=" ", store=False, type="char"),
                'eq_country': fields.function(_compute_country, string=" ", store=False, type="char"), 
                
                'eq_contact_person_id': fields.many2one('hr.employee', 'Contact Person Sale', size=100),
                'eq_head_text': fields.html('Head Text'),
                'note': fields.html('Terms and conditions'),
                'show_delivery_date': fields.boolean('Show Delivery Date'),
                'use_calendar_week': fields.boolean('Use Calendar Week for Delivery Date [equitania]'),                           
                }
    
    _defaults = {
                'eq_contact_person_id': lambda obj, cr, uid, context: obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])[0] if len(obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])) >= 1 else obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)]) or False,
                }
sale_order()


class eq_report_extension_sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    SEQUENCE_VALUE = 10
    
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
        
        # set product name only after first change of quantity - it's our workaround for refresh problem after each change of quantity
        if name is False:                   # name is set, don't reset it again !           
            if not eq_use_internal_descriptionion and product_id.description_sale:
                vals['value']['name'] = product_id.description_sale
            elif eq_use_internal_descriptionion and product_id.description:
                vals['value']['name'] = product_id.product_tmpl_id.description
            else:
                vals['value']['name'] = ' '
        
        vals['value']['delay'] = product_id.sale_delay
        return vals
    
    
    def default_get(self, cr, uid, ids, context=None):
        res =  super(eq_report_extension_sale_order_line, self).default_get(cr, uid, ids, context=context)
        
        # small bugfix for our exceltool
        next_sequence = self.SEQUENCE_VALUE
        if context is not None:        
            if context:
                context_keys = context.keys()
                next_sequence = self.SEQUENCE_VALUE
                if 'ref_ids' in context_keys:
                    if len(context.get('ref_ids')) > 0:
                        next_sequence = (len(context.get('ref_ids')) + 1) * self.SEQUENCE_VALUE
        
        res.update({'sequence': next_sequence})
        return res