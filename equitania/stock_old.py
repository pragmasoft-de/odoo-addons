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

        
class eq_report_extension_stock_picking(osv.osv):
    _inherit = "stock.picking"
    
    _columns = {
                'eq_ref_number': fields.char('Sale Order Referenc', size=64),
                }
    
    #Adds the customer ref number to the picking list. Gets data from context which is set in the method action_ship_create of the sale.order
    def create(self, cr, user, vals, context={}):
        if context:
            if context.get('eq_ref_number', False):
                vals['eq_ref_number'] = context['eq_ref_number'].get(vals['origin'], False)
        return super(eq_report_extension_stock_picking, self).create(cr, user, vals, context)
    
    #Adds the customer ref number to the invoice (Create from picking list)
    def _create_invoice_from_picking(self, cr, uid, picking, vals, context=None):    
        vals['eq_ref_number'] = picking.eq_ref_number
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
                
        vals['eq_head_text'] = head_text
        vals['comment'] = comment
                
        
        #picking.move_lines[0].purchase_line_id[0].order_id.eq_head_text
        #picking.move_lines[0].procurement_id.sale_line_id.order_id
        
        
        return super(eq_report_extension_stock_picking, self)._create_invoice_from_picking(cr, uid, picking, vals, context)
    
    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        res = super(eq_report_extension_stock_picking, self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move, context)
        res['name'] = move.picking_id.origin
        return res