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

class eq_stock_config_settings(osv.osv_memory):
    _inherit = 'stock.config.settings'
    
    def set_default_sale_settings_eq(self, cr, uid, ids, context=None):
        ir_values = self.pool.get('ir.values')
        config = self.browse(cr, uid, ids[0], context)
        ir_values.set_default(cr, uid, 'stock.picking', 'default_eq_join_stock_moves', config.default_eq_join_stock_moves)
        
    def get_default_use_sale_settings_eq(self, cr, uid, fields, context=None):
        ir_values = self.pool.get('ir.values')
        join_stock_moves = ir_values.get_default(cr, uid, 'stock.picking', 'default_eq_join_stock_moves')
        return {
                'default_eq_join_stock_moves': join_stock_moves,
                }
    
    _columns = {
                'default_eq_join_stock_moves': fields.boolean('Join the positions of overdeliveries [equitania]', help="When an overdelivery occures it will automaticly join the positions of the picking.")
                }