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
        same_move_id = stock_move_obj.search(cr, uid, [('price_unit', '=', res['price_unit']), ('product_id', '=', res['product_id']), ('picking_id', '=', res['picking_id'])])[0]
        same_move = stock_move_obj.browse(cr, uid, same_move_id).procurement_id.id
        res['procurement_id'] = same_move.procurement_id.id
        res['name'] = same_move.name
        return res