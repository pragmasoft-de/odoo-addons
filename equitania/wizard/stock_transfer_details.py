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
                for move in moves:
                    move.product_uom_qty = item.quantity
        res = super(eq_stock_transfer_details, self).do_detailed_transfer()
        return res
        
class eq_stock_transfer_details_items(models.TransientModel):
    _inherit = 'stock.transfer_details_items'
    
    eq_line_finished = fields.Boolean('Finished')
    