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
                    qty = 0
                    move_id = False
                    move_qty = 0
                    for link in pack_operation.linked_move_operation_ids:
                        qty += link.move_id.product_uom_qty
                        move_id = link.move_id.id
                        move_qty = link.move_id.product_uom_qty
                    if pack_operation.product_qty > qty:
                        packop_qty = pack_operation.product_qty - qty + move_qty
                        self.pool.get('stock.move').write(cr, uid, move_id, {'product_uom_qty': packop_qty, 'product_uos_qty': packop_qty * pack_operation.product_id.uos_coeff})
            print 'doit!'
        return super(stock_picking_extension, self).do_transfer(cr, uid, picking_ids, context)
    
    @api.multi
    def reverse_picking_new_view(self):
        view = self.env.ref('stock.view_picking_form')

        return {
            'name': _('Delivery'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'current',
            'res_id': self.ids[0],
            'context': self.env.context,
        }
    
    @api.cr_uid_ids_context
    def reverse_picking(self, cr, uid, ids, context=None):
        rp_vals = {
                   'move_dest_exists': False,
                   'invoice_state': 'none',
                   }
        #Add active model. Otherwise it throws an error when the return picking is created. (Bad context propagation)
        context['active_model'] = 'stock.picking'
        context['active_id'] = ids[0]
        context['active_ids'] = ids
        #Creates the return picking
        return_picking_obj = self.pool.get('stock.return.picking')
        return_picking_id = return_picking_obj.create(cr, uid, rp_vals, context=context)
        new_picking_id, pick_type_id = return_picking_obj._create_returns(cr, uid, [return_picking_id], context=context)
        self.write(cr, uid, new_picking_id, {'invoice_state': 'none'}, context)
        #Do transfer for new picking
        transfer_obj = self.pool['stock.transfer_details']
        transfer_details_id = transfer_obj.create(cr, uid, {'picking_id': new_picking_id or False}, context=context)
        transfer_obj.do_detailed_transfer(cr, uid, [transfer_details_id], context)
        #Copy the picking
        new_picking_id = self.copy(cr, uid, ids[0], context)
        #Edit current and return picking, No invoice needed
        self.write(cr, uid, ids, {'invoice_state': 'none'}, context)
        transfer_obj.write(cr, uid, new_picking_id, {'invoice_state': 'none'})
        #Return as view definition
        return self.reverse_picking_new_view(cr, uid, new_picking_id)

    @api.cr_uid_ids_context
    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        res = super(stock_picking_extension, self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move, context)
        if move.procurement_id:
            if move.procurement_id.sale_line_id:
                res['comment'] = move.procurement_id.sale_line_id.order_id.note
        return res

class stock_move_extension(osv.osv):
    _inherit = ['stock.move']
    def _get_invoice_line_vals(self, cr, uid, move, partner, inv_type, context=None):
        
        res = super(stock_move_extension, self)._get_invoice_line_vals(cr, uid, move, partner, inv_type, context)
        
        res.update({'eq_move_id': move.id})
        
        return res