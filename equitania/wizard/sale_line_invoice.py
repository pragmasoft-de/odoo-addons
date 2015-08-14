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


from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import workflow

class sale_order_line_make_invoice(osv.osv_memory):
    _inherit = "sale.order.line.make.invoice"

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        res = super(sale_order_line_make_invoice, self)._prepare_invoice(cr, uid, order, lines, context=context)
        res['eq_ref_number'] = order.client_order_ref
        res['name'] = order.name
        return res
    
class sale_advance_payment_inv(osv.osv_memory):
    _inherit = "sale.advance.payment.inv"
    
    def _prepare_advance_invoice_vals(self, cr, uid, ids, context=None):
        res = super(sale_advance_payment_inv, self)._prepare_advance_invoice_vals(cr, uid, ids, context=context)
        for re in res:
            order = self.pool.get('sale.order').browse(cr, uid, re[0])
            re[1]['eq_ref_number'] = order.client_order_ref
            re[1]['name'] = order.name
        return res