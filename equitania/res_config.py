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

class eq_purchase_config_settings(osv.osv_memory):
    _inherit = 'purchase.config.settings'
    
    def set_default_filter(self, cr, uid, ids, context=None):
        ir_values = self.pool.get('ir.values')
        config = self.browse(cr, uid, ids[0], context)
        ir_values.set_default(cr, uid, 'purchase.order', 'eq_filter_prod_sup', config.default_eq_filter_prod_sup)
        
    def get_default_filter(self, cr, uid, fields, context=None):
        ir_values = self.pool.get('ir.values')
        filter_prod_sup = ir_values.get_default(cr, uid, 'purchase.order', 'eq_filter_prod_sup')
        return {
                'default_eq_filter_prod_sup': filter_prod_sup,
                }
    
    _columns = {
                'default_eq_filter_prod_sup': fields.boolean('Only show Products of selected supplier [equitania]'),
                }

    

class eq_stock_config_settings(osv.osv_memory):
    _inherit = 'stock.config.settings'
    
    def set_default_sale_settings_eq(self, cr, uid, ids, context=None):
        ir_values = self.pool.get('ir.values')
        config = self.browse(cr, uid, ids[0], context)
        ir_values.set_default(cr, uid, 'stock.picking', 'default_eq_join_stock_moves', config.default_eq_join_stock_moves)
        ir_values.set_default(cr, uid, 'product.product', 'default_eq_min_prefix_count', config.default_eq_min_prefix_count)
        ir_values.set_default(cr, uid, 'product.product', 'default_eq_max_prefix_count', config.default_eq_max_prefix_count)
        ir_values.set_default(cr, uid, 'product.product', 'default_eq_prod_num_lenght', config.default_eq_prod_num_lenght)
        ir_values.set_default(cr, uid, 'product.product', 'default_eq_seperator', config.default_eq_seperator)
        
    def get_default_use_sale_settings_eq(self, cr, uid, fields, context=None):
        ir_values = self.pool.get('ir.values')
        join_stock_moves = ir_values.get_default(cr, uid, 'stock.picking', 'default_eq_join_stock_moves')
        default_eq_min_prefix_count = ir_values.get_default(cr, uid, 'product.product', 'default_eq_min_prefix_count')
        default_eq_max_prefix_count = ir_values.get_default(cr, uid, 'product.product', 'default_eq_max_prefix_count')
        default_eq_prod_num_lenght = ir_values.get_default(cr, uid, 'product.product', 'default_eq_prod_num_lenght')
        default_eq_seperator = ir_values.get_default(cr, uid, 'product.product', 'default_eq_seperator')
        return {
                'default_eq_join_stock_moves': join_stock_moves,
                'default_eq_min_prefix_count': default_eq_min_prefix_count,
                'default_eq_max_prefix_count': default_eq_max_prefix_count,
                'default_eq_prod_num_lenght': default_eq_prod_num_lenght,
                'default_eq_seperator': default_eq_seperator,
                }
    
    _columns = {
                'default_eq_join_stock_moves': fields.boolean('Join the positions of overdeliveries [equitania]', help="When an overdelivery occures it will automaticly join the positions of the picking."),
                'default_eq_min_prefix_count': fields.integer('Min prefix lenght [equitania]'),
                'default_eq_max_prefix_count': fields.integer('Max prefix lenght [equitania]'),
                'default_eq_prod_num_lenght': fields.integer('Product number lenght [equitania]'),
                'default_eq_seperator': fields.char('Seperator [equitania]'),
                'module_eq_info_for_product_product': fields.boolean('Volume, weight and net weight from product variant [equitania]', help="The volume, weight and net weight will be set in the product variant (product.product)."),
                }