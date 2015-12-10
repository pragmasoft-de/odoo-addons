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

from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from datetime import datetime
        
class eq_stock_transfer_details(models.TransientModel):
    _inherit = 'stock.transfer_details'
    
    @api.one
    def do_detailed_transfer(self):
        for item in self.item_ids:
            if item.eq_line_finished:
                moves = self.env['stock.move'].search([('picking_id', '=', self.picking_id.id), ('product_id', '=', item.product_id.id), ('product_uom_qty', '>=', item.quantity)])
                if hasattr(item, 'eq_move_id'):
                    moves = item.eq_move_id
                for move in moves:
                    move.product_uom_qty = item.quantity
                    move.product_uos_qty = item.quantity * move.product_id.uos_coeff
                    
        processed_ids = []
        # Create new and update existing pack operations
        for lstits in [self.item_ids, self.packop_ids]:
            for prod in lstits:
                pack_datas = {
                    'product_id': prod.product_id.id,
                    'product_uom_id': prod.product_uom_id.id,
                    'product_qty': prod.quantity,
                    'package_id': prod.package_id.id,
                    'lot_id': prod.lot_id.id,
                    'location_id': prod.sourceloc_id.id,
                    'location_dest_id': prod.destinationloc_id.id,
                    'result_package_id': prod.result_package_id.id,
                    'date': prod.date if prod.date else datetime.now(),
                    'owner_id': prod.owner_id.id,
                }
                if prod.packop_id:
                    prod.packop_id.with_context(no_recompute=True).write(pack_datas)
                    processed_ids.append(prod.packop_id.id)
                    if prod.eq_move_id:
                        prod.packop_id.linked_move_operation_ids.write({'move_id': prod.eq_move_id.id})
                else:
                    pack_datas['picking_id'] = self.picking_id.id
                    packop_id = self.env['stock.pack.operation'].create(pack_datas)
                    if prod.eq_move_id:
                        prod.packop_id.linked_move_operation_ids.write({'move_id': prod.eq_move_id.id})
                    processed_ids.append(packop_id.id)
        # Delete the others
        packops = self.env['stock.pack.operation'].search(['&', ('picking_id', '=', self.picking_id.id), '!', ('id', 'in', processed_ids)])
        packops.unlink()

        # Execute the transfer of the picking
        self.picking_id.do_transfer()

        return True
    
    def _get_items_from_po(self, op, context={}):
        """
            Takes an pack operation and retuns a dict with values for stock.transfer_details_items
            @self: self
            @op: pack.operation object
            @return: dict with values for stock.transfer_details_items
        """
        item = {
            'packop_id': op.id,
            'product_id': op.product_id.id,
            'product_uom_id': op.product_uom_id.id,
            'quantity': op.product_qty,
            'package_id': op.package_id.id,
            'lot_id': op.lot_id.id,
            'sourceloc_id': op.location_id.id,
            'destinationloc_id': op.location_dest_id.id,
            'result_package_id': op.result_package_id.id,
            'date': op.date, 
            'owner_id': op.owner_id.id,
            'eq_move_id': op.eq_move_id.id,
            'eq_pos_no': op.eq_move_id.eq_pos_no,
            'eq_delivery_date': op.eq_move_id.date_expected,
        }
        return item
    
    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
        res = super(eq_stock_transfer_details, self).default_get(cr, uid, fields, context=context)
        picking_ids = context.get('active_ids', [])
        active_model = context.get('active_model')
        move_obj = self.pool.get('stock.move')

        if not picking_ids or len(picking_ids) != 1:
            # Partial Picking Processing may only be done for one picking at a time
            return res
        assert active_model in ('stock.picking'), 'Bad context propagation'
        picking_id, = picking_ids
        picking = self.pool.get('stock.picking').browse(cr, uid, picking_id, context=context)
        items = []
        packs = []
        used_moves = []
        if not picking.pack_operation_ids:
            picking.do_prepare_partial()
        for op in picking.pack_operation_ids:
            item = self._get_items_from_po(op, context=context)
            if op.product_id:
                items.append(item)
            elif op.package_id:
                packs.append(item)
            if len(op.eq_move_id.linked_move_operation_ids):
                op.eq_move_id.linked_move_operation_ids[0].operation_id = op.id
        res.update(item_ids=items)
        res.update(packop_ids=packs)
        return res    
        
class eq_stock_transfer_details_items(models.TransientModel):
    _inherit = 'stock.transfer_details_items'
    _order = 'eq_pos_no'
    
    eq_pos_no = fields.Integer('Position')
    eq_move_id = fields.Many2one('stock.move', 'Lagerbuchung')
    eq_delivery_date = fields.Datetime('Delivery Date')
    eq_line_finished = fields.Boolean('Finished')
        
class eq_stock_pack_operation(models.Model):
    _inherit = 'stock.pack.operation'
    
    eq_move_id = fields.Many2one('stock.move', 'Lagerbuchung')
    
    