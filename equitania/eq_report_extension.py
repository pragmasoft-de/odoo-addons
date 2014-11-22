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

#Adds fields to forms that are used in the reports. Contact person and Head text

class eq_report_extension_sale_settings(osv.osv_memory):
    _inherit = 'sale.config.settings'
    
    def set_default_use_sale_person(self, cr, uid, ids, context=None):
        ir_values = self.pool.get('ir.values')
        config = self.browse(cr, uid, ids[0], context)
        ir_values.set_default(cr, uid, 'sale.order', 'default_use_sales_person_as_contact', config.default_use_sales_person_as_contact and config.default_use_sales_person_as_contact.id or False)
    
    def get_default_use_sale_person(self, cr, uid, fields, context=None):
        salesperson = self.pool.get('ir.values').get_default(cr, uid, 'sale.order', 'default_use_sales_person_as_contact')
        return {
                'default_use_sales_person_as_contact': salesperson,
                }
    
    _columns = {
                'default_use_sales_person_as_contact': fields.boolean('Sale Person as Contact Person', help='Sets the Sale Person as the Contact Person in the Sale Order, only when creating.', default_model='sale.order'),
                }

class eq_report_extension_sale_order(osv.osv):
    _inherit = "sale.order"
    _columns = {
                'eq_contact_person_id': fields.many2one('hr.employee', 'Contact Person', size=100),
                'eq_head_text': fields.text('Head Text'),
                }
    _defaults = {
                'eq_contact_person_id': lambda obj, cr, uid, context: obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])[0] if len(obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])) >= 1 else obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)]) or False 
                }
    
    def create(self, cr, uid, values, context=None):
        use_sale_person = self.pool.get('ir.values').get_default(cr, uid, 'sale.order', 'default_use_sales_person_as_contact')
        
        if use_sale_person or False and values.get('user_id', False):
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
        if context is None:
            context = {}
        journal_ids = self.pool.get('account.journal').search(cr, uid,
            [('type', '=', 'sale'), ('company_id', '=', order.company_id.id)],
            limit=1)
        if not journal_ids:
            raise osv.except_osv(_('Error!'),
                _('Please define sales journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
        invoice_vals = {
            'name': order.client_order_ref or '',
            'origin': order.name,
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
    
    #Method which creates an invoice out of the sale order.
    def _make_invoice(self, cr, uid, order, lines, context=None):
        # get the invoice
        inv_obj = self.pool.get('account.invoice')
        # create the invoice
        inv_id = super(eq_report_extension_sale_order, self)._make_invoice(cr, uid, order, lines, context)
        # modify the invoice
        inv_obj.write(cr, uid, [inv_id], {'eq_customer_ref': order.origin}, context)
        inv_obj.button_compute(cr, uid, [inv_id])
        return inv_id
    
    def action_invoice_create(self, cr, uid, ids, grouped=False, states=None, date_invoice = False, context=None):
        inv_id = super(eq_report_extension_sale_order, self).action_invoice_create(cr, uid, ids, grouped, states,date_invoice, context)
        for inv in inv_id if isinstance(inv_id, list) else [inv_id]:
            self.pool.get('account.invoice').write,(cr, uid, inv, {'eq_ref_number': self.browse(cr, uid, ids, context).origin})
        return inv_id
        
    
class eq_report_extension_purchase_order(osv.osv):
    _inherit = "purchase.order"
    _columns = {
                'eq_contact_person_id': fields.many2one('hr.employee', 'Contact Person', size=100),
                'eq_head_text': fields.text('Head Text'),
                }
    _defaults = {
                'eq_contact_person_id': lambda obj, cr, uid, context: obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])[0] if len(obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])) >= 1 else obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)]) or False 
                }
    
class eq_report_extension_invoice(osv.osv):
    _inherit = "account.invoice"
    
    _columns = {
                'eq_contact_person_id': fields.many2one('hr.employee', 'Contact Person', size=100),
                'eq_head_text': fields.text('Head Text'),
                'eq_ref_number': fields.char('Reference Number', size=64),
                }
    _defaults = {
                'eq_contact_person_id': lambda obj, cr, uid, context: obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])[0] if len(obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])) >= 1 else obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)]) or False 
                }
    
        
class eq_report_extension_stock_picking(osv.osv):
    _inherit = "stock.picking"
    
    _columns = {
                'eq_ref_number': fields.char('Reference Number', size=64),
                }