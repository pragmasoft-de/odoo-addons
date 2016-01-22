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

class eq_purchase_config_settings(models.TransientModel):
    _inherit = 'purchase.config.settings'
    
    @api.multi
    def set_default_filter(self):
        ir_values = self.env['ir.values']
        config = self.browse(self.ids[0])
        ir_values.set_default('purchase.order', 'eq_filter_prod_sup', config.default_eq_filter_prod_sup)
    
    @api.multi    
    def get_default_filter(self):
        ir_values = self.env['ir.values']
        filter_prod_sup = ir_values.get_default('purchase.order', 'eq_filter_prod_sup')
        return {
                'default_eq_filter_prod_sup': filter_prod_sup,
                }
        
    """ added this functionality from eq_report_extension.py """    
    @api.multi
    def set_default_sale_settings_eq(self):
        ir_values = self.env['ir.values']
        config = self.browse(self.ids[0])
        ir_values.set_default('purchase.order', 'show_delivery_date', config.default_show_delivery_date)
        ir_values.set_default('purchase.order', 'use_calendar_week', config.default_use_calendar_week)
    
    """ added this functionality from eq_report_extension.py """
    @api.multi
    def get_default_use_sale_settings_eq(self):
        ir_values = self.env['ir.values']
        show_delivery_date = ir_values.get_default('purchase.order', 'show_delivery_date')
        use_calendar_week = ir_values.get_default('purchase.order', 'use_calendar_week')
        return {
                'default_show_delivery_date': show_delivery_date,
                'default_use_calendar_week': use_calendar_week,
                }
        
        
    default_eq_filter_prod_sup = fields.Boolean('Only show Products of selected supplier [equitania]')
    
    # added these fields from eq_report_extension.py
    default_show_delivery_date = fields.Boolean('Show the Delivery Date on the Purchase Order [equitania]', help='The delivery date will be shown in the Purchase Order', default_model='purchase.order')
    default_use_calendar_week = fields.Boolean('Show Calendar Week for Delivery Date [equitania]', help='The delivery date will be shown as a calendar week ', default_model='purchase.order')
    

class eq_stock_config_settings(models.TransientModel):
    _inherit = 'stock.config.settings'
    
    @api.multi
    def set_default_sale_settings_eq(self):
        ir_values = self.env['ir.values']
        config = self.browse(self.ids[0])
        ir_values.set_default('stock.picking', 'default_eq_join_stock_moves', config.default_eq_join_stock_moves)
        ir_values.set_default('product.product', 'default_eq_min_prefix_count', config.default_eq_min_prefix_count)
        ir_values.set_default('product.product', 'default_eq_max_prefix_count', config.default_eq_max_prefix_count)
        ir_values.set_default('product.product', 'default_eq_prod_num_lenght', config.default_eq_prod_num_lenght)
        ir_values.set_default('product.product', 'default_eq_seperator', config.default_eq_seperator)
    
    @api.multi    
    def get_default_use_sale_settings_eq(self):
        ir_values = self.env['ir.values']
        join_stock_moves = ir_values.get_default('stock.picking', 'default_eq_join_stock_moves')
        default_eq_min_prefix_count = ir_values.get_default('product.product', 'default_eq_min_prefix_count')
        default_eq_max_prefix_count = ir_values.get_default( 'product.product', 'default_eq_max_prefix_count')
        default_eq_prod_num_lenght = ir_values.get_default( 'product.product', 'default_eq_prod_num_lenght')
        default_eq_seperator = ir_values.get_default( 'product.product', 'default_eq_seperator')
        return {
                'default_eq_join_stock_moves': join_stock_moves,
                'default_eq_min_prefix_count': default_eq_min_prefix_count,
                'default_eq_max_prefix_count': default_eq_max_prefix_count,
                'default_eq_prod_num_lenght': default_eq_prod_num_lenght,
                'default_eq_seperator': default_eq_seperator,
                }
    
    
    default_eq_join_stock_moves = fields.Boolean('Join the positions of overdeliveries [equitania]', help="When an overdelivery occures it will automaticly join the positions of the picking.")
    default_eq_min_prefix_count = fields.Integer('Min prefix lenght [equitania]')
    default_eq_max_prefix_count = fields.Integer('Max prefix lenght [equitania]')
    default_eq_prod_num_lenght = fields.Integer('Product number lenght [equitania]')
    default_eq_seperator = fields.Char('Seperator [equitania]')
    module_eq_info_for_product_product = fields.Boolean('Volume, weight and net weight from product variant [equitania]', help="The volume, weight and net weight will be set in the product variant (product.product).")
    
    
    
class eq_sale_configuration_address(models.TransientModel):
    _name = 'sale.config.settings'
    _inherit = _name
    
    @api.multi
    def set_default_values_eq_address(self):
        ir_values_obj = self.env['ir.values']
        config = self.browse(self.ids[0])
        
        ir_values_obj.set_default('sale.order', 'default_show_address', config.default_show_address or False)
        ir_values_obj.set_default('sale.order', 'default_search_only_company', config.default_search_only_company or False)
            
                
    @api.multi
    def get_default_values_eq_address(self):
        ir_values_obj = self.env['ir.values']
        notification = ir_values_obj.get_default('sale.order', 'default_show_address')
        only_company = ir_values_obj.get_default('sale.order', 'default_search_only_company')
        return {
                'default_show_address': notification,
                'default_search_only_company': only_company,
                }
    
 
    default_show_address = fields.Boolean('Show street and city in the partner search of the Sale and Purchase Order [equitania]', help="This adds the street and the city to the results of the partner search of the Sale and Purchase Order.")
    default_search_only_company = fields.Boolean('Only Search for Companies [equitania]', help="Only Companies will be shown in the Customer search of the Sale and Purchase Order.")
    group_product_rrp = fields.Boolean('Show RRP for products [equitania]', implied_group='equitania.group_product_rrp')
    
    
    
class eq_partner_extension_base_config_settings(models.TransientModel):
    _inherit = "base.config.settings"
    
    @api.multi
    def set_default_creator(self):
        ir_values_obj = self.env['ir.values']
        config = self.browse(self.ids[0])
        
        ir_values_obj.set_default('base.config.settings','default_creator_saleperson', config.default_creator_saleperson or False)
    
    @api.multi    
    def get_default_creator(self):
        ir_values_obj = self.env['ir.values']
        creator = ir_values_obj.get_default('base.config.settings','default_creator_saleperson')
        return {
                'default_creator_saleperson': creator,
                }    
    
    
    default_creator_saleperson = fields.Boolean('The creator of the address dataset will be set automatically as sales person. [equitania]')


