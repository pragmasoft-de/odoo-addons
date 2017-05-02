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

from openerp import models, fields, api, _
from openerp.osv import osv


class eq_stock_move(models.Model):
    _name = 'stock.move'
    _inherit = 'stock.move'
    
    @api.v7
    def create(self,cr, uid, vals, context=None):

        
        if vals.get('picking_id'):
            stock_picking_obj = self.pool.get('stock.picking')
            stock_picking_data = stock_picking_obj.browse(cr,uid,vals.get('picking_id'),context=None)
            
            """ If error occurs while creating shipments, stock move will not be created """
            if stock_picking_data.state =='cancel':
                raise osv.except_osv(_('Shipment Error!'), _('Got Error while creating shipments.'))
            
            if stock_picking_data.state =='done' and stock_picking_data.eq_is_symbol_transfer:
                try:
                    raise osv.except_osv(_('Shipment Error!'), _('Got Error while creating shipments.'))
                except:
                    pass

        return super(eq_stock_move, self).create(cr, uid, vals, context=None)
       