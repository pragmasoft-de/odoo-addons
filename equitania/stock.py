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
from openerp.tools.float_utils import float_compare, float_round

class stock_picking_extension(osv.osv):
    _inherit = ['stock.picking']
    
    _columns = {
        'eq_sale_order_id': fields.many2one('sale.order', 'SaleOrder'),
    }
    
    
    def create(self, cr, user, vals, context=None):
        """
            Extended version of create method. We're using this in process "Confirm an order" to be able to set linke between sale order and stock_picking.
            It's a quit simple solution to save sale_order_id defined as many2one field eq_sale_order_id.
            @cr: cursor
            @user: actual user
            @vals: values to be saved
            @context: context
            @return: defaul result
        """
        context = context or {}
        sale_order_obj = self.pool.get('sale.order')
        sale_order_ids = sale_order_obj.search(cr, user, [("name", "=", vals["origin"])])       # let's find linked sale_order to be able to save it's ID in our field
        if len(sale_order_ids) > 0:
            vals['eq_sale_order_id'] = sale_order_ids[0]                                        # ok, we've got it...save it
        
        return super(stock_picking_extension, self).create(cr, user, vals, context)
    
    
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
        if same_move.picking_id.picking_type_id.code == 'incoming':
            res['name'] = op.product_id.description_purchase
        if same_move.picking_id.picking_type_id.code == 'outgoing':
            res['name'] = op.product_id.description_sale
        return res
    
    def recompute_remaining_qty(self, cr, uid, picking, context=None):
        res = super(stock_picking_extension, self).recompute_remaining_qty(cr, uid, picking, context=context)
        #links the operation with the original move, becouse the recompute_remaining_qty method distorts it.
        for op in picking.pack_operation_ids:
            for link in op.linked_move_operation_ids:
                if op.eq_move_id:
                    self.pool.get('stock.move.operation.link').write(cr, uid, link.id, {'move_id': op.eq_move_id.id})
        return res
    
    @api.cr_uid_ids_context
    def do_transfer(self, cr, uid, picking_ids, context=None):
        pickings = self.browse(cr, uid, picking_ids, context)
        join_moves = self.pool.get('ir.values').get_default(cr, uid, 'stock.picking', 'default_eq_join_stock_moves', context)
        if join_moves:
            for picking in pickings:
                for pack_operation in picking.pack_operation_ids:
                    qty = 0
                    move_id = False
                    move_qty = 0
                    for link in pack_operation.linked_move_operation_ids:
                        if link.move_id:
                            if move_id != link.move_id.id:
                                qty += link.move_id.product_uom_qty
                                move_id = link.move_id.id
                                move_qty = link.move_id.product_uom_qty
                    if pack_operation.product_qty > qty:
                        packop_qty = pack_operation.product_qty - qty + move_qty
                        self.pool.get('stock.move').write(cr, uid, move_id, {'product_uom_qty': packop_qty, 'product_uos_qty': packop_qty * pack_operation.product_id.uos_coeff})
        for picking in pickings:
            if len(picking.move_lines[0].linked_move_operation_ids):
                picking.move_lines[0].linked_move_operation_ids[0].unlink()
        res = super(stock_picking_extension, self).do_transfer(cr, uid, picking_ids, context)
        return res
    
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
        picking_to_return = self.browse(cr, uid, ids)
        for move_to_return in picking_to_return.move_lines:
            #Reserves the quants from the original move
            if move_to_return.lot_ids and len(move_to_return.lot_ids) == move_to_return.product_qty and len(move_to_return.returned_move_ids) == 1:
                move_to_return.returned_move_ids[0].reserved_quant_ids = [quant.id for quant in move_to_return.quant_ids]
                move_to_return.returned_move_ids[0].lot_ids = [lot.id for lot in move_to_return.lot_ids]
        self.write(cr, uid, new_picking_id, {'invoice_state': 'none'}, context)
        #Do transfer for new picking
        transfer_obj = self.pool['stock.transfer_details']
        transfer_details_id = transfer_obj.create(cr, uid, {'picking_id': new_picking_id or False}, context=context)
        transfer_obj.do_detailed_transfer(cr, uid, [transfer_details_id], context)
        #Copy the picking
        new_picking_id = self.copy(cr, uid, ids[0], context)
        #Edit current, No invoice needed
        self.write(cr, uid, ids, {'invoice_state': 'none'}, context)
        #Edit new, Invoice needed
        self.write(cr, uid, new_picking_id, {'invoice_state': '2binvoiced'})
        #Return as view definition
        return self.reverse_picking_new_view(cr, uid, new_picking_id)

    @api.cr_uid_ids_context
    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        res = super(stock_picking_extension, self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move, context)
        if move.procurement_id:
            if move.procurement_id.sale_line_id:
                res['comment'] = move.procurement_id.sale_line_id.order_id.note
        return res

    @api.cr_uid_ids_context
    def change_date_done(self, cr, uid, ids, context={}):
        vals = {'eq_new_date_done': self.browse(cr, uid, ids[0]).date_done}
        date_done_change_id = self.pool.get('eq.date.done.change').create(cr, uid, vals)
        context['picking_id'] = ids
        return self.date_done_change_view(cr, uid, ids, date_done_change_id, context=context)
    
    @api.multi
    def date_done_change_view(self, date_done_change_id):
        view = self.env.ref('equitania.eq_date_done_form_view')

        return {
            'name': _('Change date done'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eq.date.done.change',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'no_destroy': True,
            'target': 'new',
            'res_id': date_done_change_id,
            'context': self.env.context,
        }
        
    def _prepare_pack_ops(self, cr, uid, picking, quants, forced_qties, context=None):
        """ returns a list of dict, ready to be used in create() of stock.pack.operation.

        :param picking: browse record (stock.picking)
        :param quants: browse record list (stock.quant). List of quants associated to the picking
        :param forced_qties: dictionary showing for each product (keys) its corresponding quantity (value) that is not covered by the quants associated to the picking
        """
        def _picking_putaway_apply(product):
            location = False
            # Search putaway strategy
            if product_putaway_strats.get(product.id):
                location = product_putaway_strats[product.id]
            else:
                location = self.pool.get('stock.location').get_putaway_strategy(cr, uid, picking.location_dest_id, product, context=context)
                product_putaway_strats[product.id] = location
            return location or picking.location_dest_id.id
        
        product_uom = {} # Determines UoM used in pack operations
        location_dest_id = None
        location_id = None
        for move in [x for x in picking.move_lines if x.state not in ('done', 'cancel')]:
            if not product_uom.get(move.product_id.id):
                product_uom[move.product_id.id] = move.product_id.uom_id
            if move.product_uom.id != move.product_id.uom_id.id and move.product_uom.factor > product_uom[move.product_id.id].factor:
                product_uom[move.product_id.id] = move.product_uom
            if not move.scrapped:
                if location_dest_id and move.location_dest_id.id != location_dest_id:
                    raise Warning(_('The destination location must be the same for all the moves of the picking.'))
                location_dest_id = move.location_dest_id.id
                if location_id and move.location_id.id != location_id:
                    raise Warning(_('The source location must be the same for all the moves of the picking.'))
                location_id = move.location_id.id
        
        pack_obj = self.pool.get("stock.quant.package")
        quant_obj = self.pool.get("stock.quant")
        vals = []
        qtys_grouped = {}
        #for each quant of the picking, find the suggested location
        quants_suggested_locations = {}
        product_putaway_strats = {}
        # Do the same for the forced quantities (in cases of force_assign or incomming shipment for example)
        for move in picking.move_lines:
            if move.product_uom_qty <= 0:
                continue
            suggested_location_id = _picking_putaway_apply(move.product_id)
            key = (move.product_id.id, False, False, picking.owner_id.id, picking.location_id.id, suggested_location_id, move.id)
            if qtys_grouped.get(key):
                qtys_grouped[key] += move.product_uom_qty
            else:
                qtys_grouped[key] = move.product_uom_qty

        # Create the necessary operations for the grouped quants and remaining qtys
        uom_obj = self.pool.get('product.uom')
        prevals = {}
        for key, qty in qtys_grouped.items():
            product = self.pool.get("product.product").browse(cr, uid, key[0], context=context)
            uom_id = product.uom_id.id
            qty_uom = qty
            if product_uom.get(key[0]):
                uom_id = product_uom[key[0]].id
                qty_uom = uom_obj._compute_qty(cr, uid, product.uom_id.id, qty, uom_id)
            val_dict = {
                'picking_id': picking.id,
                'product_qty': qty_uom,
                'product_id': key[0],
                'package_id': key[1],
                'lot_id': key[2],
                'owner_id': key[3],
                'location_id': key[4],
                'location_dest_id': key[5],
                'product_uom_id': uom_id,
                'eq_move_id': key[6]
            }
            if key[0] in prevals:
                prevals[key[0]].append(val_dict)
            else:
                prevals[key[0]] = [val_dict]
        # prevals var holds the operations in order to create them in the same order than the picking stock moves if possible
        processed_products = set()
        for move in [x for x in picking.move_lines if x.state not in ('done', 'cancel')]:
            if move.product_id.id not in processed_products:
                vals += prevals.get(move.product_id.id, [])
                processed_products.add(move.product_id.id)
        return vals

class stock_move_extension(osv.osv):
    _inherit = ['stock.move']
    
    _columns = {
        'name': fields.text('Description', required=True, select=True),
        }
    
    def _get_invoice_line_vals(self, cr, uid, move, partner, inv_type, context=None):
        
        res = super(stock_move_extension, self)._get_invoice_line_vals(cr, uid, move, partner, inv_type, context)
        
        res.update({'eq_move_id': move.id})
        
        if not move.procurement_id:
            fpos = partner.property_account_position or False
            res['invoice_line_tax_id'] = [(6,0,self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, move.product_id.taxes_id))]
        
        return res
        