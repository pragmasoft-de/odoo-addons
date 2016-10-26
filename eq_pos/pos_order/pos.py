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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc, tools
import time
from openerp.tools import float_is_zero

from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing
from base64 import b64encode
from reportlab.graphics import renderPM
from reportlab.lib import units
from passlib.context import CryptContext

import logging
_logger = logging.getLogger(__name__)

class pos_order(osv.osv):
    _inherit = "pos.order"
    _columns = {
        'parent_return_order': fields.char('Return Order ID', size=64),
        'return_seq': fields.integer('Return Sequence'),
        'return_process': fields.boolean('Return Process'),
        'back_order': fields.char('Back Order', size=256, default=False, copy=False),
        
        'gift_coupon_amt': fields.float('Gift Coupon Amt', readonly=True),
        'bonus_discount': fields.float('Bonus Discount', readonly=True)
    }
    
    def check_connection(self, cr, uid, context=None):
        return True
    
    def check_pwd(self, cr, uid, id, password, context=None):
        cr.execute('SELECT password_crypt FROM res_users WHERE id=%s AND active', (id,))
        encrypted = None
        if cr.rowcount:
            encrypted = cr.fetchone()[0]
        if encrypted:
            valid_pass, replacement = self._crypt_context(cr, uid, id)\
                    .verify_and_update(password, encrypted)
            if valid_pass:
                return True
        return False
    
    def _crypt_context(self, cr, uid, id, context=None):
        return CryptContext(['pbkdf2_sha512', 'md5_crypt'],deprecated=['md5_crypt'])
    
    def _order_fields(self, cr, uid, ui_order, context=None):
        return {
            'name':                 ui_order['name'],
            'user_id':              ui_order['user_id'] or False,
            'session_id':           ui_order['pos_session_id'],
            'lines':                ui_order['lines'],
            'pos_reference':        ui_order['name'],
            'partner_id':           ui_order['partner_id'] or False,
            'return_order':         ui_order.get('return_order', ''),
            'back_order':           ui_order.get('back_order',''),
            'parent_return_order':  ui_order.get('parent_return_order',''),
            'return_seq':           ui_order.get('return_seq',''),
            
            'gift_coupon_amt':      ui_order.get('gift_coupon_amt') or 0.0,
            'bonus_discount':       ui_order.get('bonus_discount') or 0.0
        }
        
    def _process_order(self, cr, uid, order, context=None):
        order_id = self.create(cr, uid, self._order_fields(cr, uid, order, context=context),context)
        
        gift_coupon_amt = context.get('gift_amount', 0.0)
        bonus_discount = context.get('bonus_amt', 0.0)

        for payments in order['statement_ids']:
            if order.get('parent_return_order', ''):
                payments[2]['amount'] = -payments[2]['amount'] or 0.0
            self.add_payment(cr, uid, order_id, self._payment_fields(cr, uid, payments[2], context=context), context=context)

        if gift_coupon_amt:
            #coupon_journal = self.pool.get('account.journal').search(cr, uid, [('code', '=', 'CPNJ')])            # old version
            coupon_journal = self.pool.get('account.journal').search(cr, uid, ['|', ('code', '=', 'CPNJ'), ('code', '=', 'GuEin')])            # old version                    
            if coupon_journal:
                ctx = context.copy()
                ctx.update({'gift_coupon_amt': True})
                self.add_payment(cr, uid, order_id, {
                    'amount': gift_coupon_amt,
                    'payment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'payment_name': _('Discount'),
                    'journal': coupon_journal[0],
#                        'statement_id': payment['statement_id']    All payment journals will be same if we remove this comment.,
                }, context=ctx)
                
        if bonus_discount:
            bonus_discount_journal = self.pool.get('account.journal').search(cr, uid, [('code', '=', 'BNSJ')])
            if bonus_discount_journal:
                ctx = context.copy()
                ctx.update({'bonus_discount': True})
                self.add_payment(cr, uid, order_id, {
                    'amount': bonus_discount,
                    'payment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'payment_name': _('Discount'),
                    'journal': bonus_discount_journal[0],
#                        'statement_id': payment['statement_id']    All payment journals will be same if we remove this comment.,
                }, context=ctx)

        session = self.pool.get('pos.session').browse(cr, uid, order['pos_session_id'], context=context)
        if session.sequence_number <= order['sequence_number']:
            session.write({'sequence_number': order['sequence_number'] + 1})
            session.refresh()

        if not order.get('parent_return_order', '') and not float_is_zero(order['amount_return'], self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')):
            cash_journal = session.cash_journal_id
            if not cash_journal:
                cash_journal_ids = filter(lambda st: st.journal_id.type=='cash', session.statement_ids)
                if not len(cash_journal_ids):
                    raise osv.except_osv( _('error!'),
                        _("No cash statement found for this session. Unable to record returned cash."))
                cash_journal = cash_journal_ids[0].journal_id
            self.add_payment(cr, uid, order_id, {
                'amount': -order['amount_return'],
                'payment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'payment_name': _('return'),
                'journal': cash_journal.id,
            }, context=context)
        
        if order.get('parent_return_order', '') and not float_is_zero(order['amount_return'], self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')):
            cash_journal = session.cash_journal_id
            if not cash_journal:
                cash_journal_ids = filter(lambda st: st.journal_id.type=='cash', session.statement_ids)
                if not len(cash_journal_ids):
                    raise osv.except_osv( _('error!'),
                        _("No cash statement found for this session. Unable to record returned cash."))
                cash_journal = cash_journal_ids[0].journal_id
            self.add_payment(cr, uid, order_id, {
                'amount': order['amount_return'],
                'payment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'payment_name': _('return'),
                'journal': cash_journal.id,
            }, context=context)
        
        return order_id
    
    def create_from_ui(self, cr, uid, orders, context=None):
        # Keep only new orders
        submitted_references = [o['data']['name'] for o in orders]
        existing_order_ids = self.search(cr, uid, [('pos_reference', 'in', submitted_references)], context=context)
        existing_orders = self.read(cr, uid, existing_order_ids, ['pos_reference'], context=context)
        existing_references = set([o['pos_reference'] for o in existing_orders])
        orders_to_save = [o for o in orders if o['data']['name'] not in existing_references]

        order_ids = []
        
        gift_coupon_amt = 0.0
        bonus_discount = 0.0

        for tmp_order in orders_to_save:
            to_invoice = tmp_order['to_invoice']
            order = tmp_order['data']
            
            if context.get('gift_amount'):
                gift_coupon_amt = context.get('gift_amount')
                order.update({'gift_coupon_amt': gift_coupon_amt})
            if context.get('bonus_amt'):
                bonus_discount = context.get('bonus_amt')
                order.update({'bonus_discount': bonus_discount})
                
            order_id = self._process_order(cr, uid, order, context=context)
            if order_id:
                if order.get('parent_return_order'):
                    pos_line_obj = self.pool.get('pos.order.line')
                    for line in order.get('lines'):
                        if line[2].get('return_process'):
                            ret_prod = pos_line_obj.search(cr, uid, [('order_id', '=', order.get('parent_return_order')),
                                                            ('product_id', '=', line[2].get('product_id')), 
                                                            ('return_qty', '>', 0)])
                            return_qty = pos_line_obj.browse(cr, uid, ret_prod).return_qty
                            if return_qty > 0 and line[2].get('qty') <= return_qty:
                                return_qty = return_qty + line[2].get('qty')
                                pos_line_obj.write(cr, uid, ret_prod, {'return_qty':return_qty});
            order_ids.append(order_id)

            try:
                self.signal_workflow(cr, uid, [order_id], 'paid')
            except Exception, e:
                _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))

            if to_invoice:
                self.action_invoice(cr, uid, [order_id], context)
                order_obj = self.browse(cr, uid, order_id, context)
                self.pool['account.invoice'].signal_workflow(cr, uid, [order_obj.invoice_id.id], 'invoice_open')

        return order_ids
    
    def get_barcode(self, cr, uid, value, width, barWidth = 0.05 * units.inch, fontSize = 30, humanReadable = True):
        barcode = createBarcodeDrawing('EAN13', value = value, barWidth = barWidth, fontSize = fontSize, humanReadable = humanReadable)
        drawing_width = width
        barcode_scale = drawing_width / barcode.width
        drawing_height = barcode.height * barcode_scale
        
        drawing = Drawing(drawing_width, drawing_height)
        drawing.scale(barcode_scale, barcode_scale)
        drawing.add(barcode, name='barcode')
        barcode_encode = b64encode(renderPM.drawToString(drawing, fmt = 'PNG'))
        barcode_str = 'data:image/png;base64,' + barcode_encode
        return barcode_str


pos_order()

class pos_order_line(osv.osv):
    _inherit = "pos.order.line"
    _columns = {
        'return_qty': fields.integer('Return QTY', size=64),
        'changed_text' : fields.char('Changed Text')
    }
pos_order_line()

class account_journal(osv.osv):
    _inherit = "account.journal"
    _columns = {
        'pos_front_display': fields.boolean('Display in POS Front')
    }
    _defaults = {
        'pos_front_display': False,
    }
account_journal()

