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
from openerp import SUPERUSER_ID, api

class stock_picking_extension(osv.osv):
    _inherit = ['stock.picking']
    
    def _prepare_values_extra_move(self, cr, uid, op, product, remaining_qty, context=None):
        """
        Calculates and sets the UOS for the move line.
        """
        res = super(stock_picking_extension, self)._prepare_values_extra_move(cr, uid, op, product, remaining_qty, context)
        
        res['product_uos'] = op.product_id.uos_id.id
        res['product_uos_qty'] = res['product_uom_qty'] * op.product_id.uos_coeff
        res['partner_id'] = op.picking_id.partner_id.id
        res['group_id'] = op.picking_id.group_id.id
        
        stock_move_obj = self.pool.get('stock.move')
        same_move_id = False
        if 'price_unit' in res:
            same_move_id = stock_move_obj.search(cr, uid, [('price_unit', '>=', res['price_unit'] - 0.01), ('price_unit', '<=', res['price_unit'] + 0.01), ('product_id', '=', res['product_id']), ('picking_id', '=', res['picking_id'])])
        else:
            same_move_id = stock_move_obj.search(cr, uid, [('picking_id', '=', res['picking_id'])])
            if len(same_move_id) > 1:
                same_move_id = same_move_id[0]
        same_move = stock_move_obj.browse(cr, uid, same_move_id)
        res['procurement_id'] = same_move.procurement_id.id
        res['name'] = same_move.name
        return res
    
    
    @api.cr_uid_ids_context
    def do_transfer(self, cr, uid, picking_ids, context=None):
        join_moves = self.pool.get('ir.values').get_default(cr, uid, 'stock.picking', 'default_eq_join_stock_moves', context)
        if join_moves:
            for picking in self.browse(cr, uid, picking_ids, context):
                for pack_operation in picking.pack_operation_ids:
                    for move in picking.move_lines:
                        if pack_operation.product_id.id == move.product_id.id and pack_operation.product_qty > move.product_uom_qty:
                            self.pool.get('stock.move').write(cr, uid, move.id, {'product_uom_qty': pack_operation.product_qty, 'product_qty': pack_operation.product_qty * pack_operation.product_id.uos_coeff})
            print 'doit!'
        return super(stock_picking_extension, self).do_transfer(cr, uid, picking_ids, context)

class stock_move_extension(osv.osv):
    _inherit = ['stock.move']
    def _get_invoice_line_vals(self, cr, uid, move, partner, inv_type, context=None):
        
        res = super(stock_move_extension, self)._get_invoice_line_vals(cr, uid, move, partner, inv_type, context)
        
        res.update({'eq_move_id': move.id})
        
        return res