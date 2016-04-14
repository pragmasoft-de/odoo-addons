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

from openerp import models, api, fields as fields_V8

class eq_product_product_new_api(models.Model):
    _inherit = "product.product"
    
    @api.depends('product_tmpl_id')
    def _get_product_tmpl_id(self):
        for rec in self:
            rec.eq_display_prod_tmpl_id = rec.product_tmpl_id
    
    eq_display_prod_tmpl_id = fields_V8.Many2one(string="Product Template", comodel_name="product.template", compute="_get_product_tmpl_id", store=False)
    #computed
    
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self._context.get('eq_filter_prod_sup'):
            partner_id = self._context['eq_partner_id']
            sql_query = """select product_tmpl_id from product_supplierinfo where name = %s""" % (partner_id)
            self._cr.execute(sql_query)
            supplierinfo = self._cr.fetchall()
            product_ids = [x[0] for x in supplierinfo]
            if args == None:
                args = []
            args.append(['id', 'in', product_ids])
        res = super(eq_product_product_new_api, self).name_search(name, args=args, operator=operator, limit=limit)
        return res

class eq_product_template(osv.osv):
    _inherit = 'product.template'
    
    def _eq_sale_count(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            cr.execute("""select sum(product_uom_qty) from stock_move where procurement_id in 
            (select id from procurement_order where sale_line_id in 
            (select id from sale_order_line as sol where sol.product_id in 
            (select id from product_product where product_tmpl_id = %d) 
            and sol.state not in ('cancel', 'done') 
            and (select state from sale_order where id = sol.order_id) not in ('sent', 'draft'))) 
            and state not in ('done', 'cancel')
            and picking_id is not null""" % (id))
            open = cr.fetchone()[0] or 0
            cr.execute("""select sum(product_uom_qty) from sale_order_line where product_id in (select id from product_product where product_tmpl_id = %d) and state != 'cancel' and (select state from sale_order where id = order_id) not in ('sent', 'draft')""" % (id))
            all = cr.fetchone()[0] or 0
            res[id] = '%d / %d' % (open, all)
        return res
    
    _columns = {
                'eq_sale_count': fields.function(_eq_sale_count, type="char", string='Sales'),
                #'eq_sale_min_qty': fields.integer(string='Min. order quantity'),                
                }
    
    """
    _defaults = {
                 'eq_sale_min_qty': 0,
    }
    """
    
    def action_view_stock_moves(self, cr, uid, ids, context=None):
        products = self._get_products(cr, uid, ids, context=context)
        result = self._get_act_window_dict(cr, uid, 'stock.act_product_stock_move_open', context=context)
        if len(ids) == 1 and len(products) == 1:
            ctx = "{'tree_view_ref':'stock.view_move_tree', \
                  'default_product_id': %s, 'search_default_product_id': %s}" \
                  % (products[0], products[0])
            result['context'] = ctx
        else:
            result['domain'] = "[('product_id','in',[" + ','.join(map(str, products)) + "])]"
            result['context'] = "{'tree_view_ref':'stock.view_move_tree'}"
        return result
    
    def action_view_stock_moves(self, cr, uid, ids, context=None):
        products = self._get_products(cr, uid, ids, context=context)
        result = self._get_act_window_dict(cr, uid, 'equitania.eq_act_product_stock_move_open', context=context)
        if len(ids) == 1 and len(products) == 1:
            ctx = "{'tree_view_ref':'stock.view_move_tree', \
                  'default_product_id': %s, 'search_default_product_id': %s}" \
                  % (products[0], products[0])
            result['context'] = ctx
            result['context'] = result['context'][:-1] + ", 'search_default_in_and_out': 1" + result['context'][-1]
        else:
            result['domain'] = "[('product_id','in',[" + ','.join(map(str, products)) + "])]"
            result['context'] = result['context'][:-1] + ", 'search_default_in_and_out': 1" + result['context'][-1]
        return result
    
    def write(self, cr, uid, ids, vals, context=None):
        if 'standard_price' in vals:
            for sep_id in ids:
                old_price = self.read(cr, uid, sep_id, ['standard_price'], context)['standard_price']
                new_price = vals['standard_price']
                history_vals = {
                                'eq_product_id': sep_id,
                                'eq_old_price': old_price,
                                'eq_new_price': new_price,
                                }
                self.pool.get('product.template.standard_price_history').create(cr, uid, history_vals, context=context)
        res = super(eq_product_template, self).write(cr, uid, ids, vals, context=context)
        return res
    
class eq_product_product(osv.osv):
    _inherit = 'product.product'
    
    def _eq_sale_count(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:            
            cr.execute("""select sum(product_uom_qty) from stock_move where procurement_id in 
            (select id from procurement_order where sale_line_id in 
            (select id from sale_order_line as sol where sol.product_id  = %d 
            and sol.state not in ('cancel', 'done') 
            and (select state from sale_order where id = sol.order_id) not in ('sent', 'draft'))) 
            and state not in ('done', 'cancel')
            and picking_id is not null""" % (id))                    
            open = cr.fetchone()[0] or 0
            cr.execute("""select sum(product_uom_qty) from sale_order_line where product_id = %d and state != 'cancel' 
            and (select state from sale_order where id = order_id) not in ('sent', 'draft')""" % (id))
            all = cr.fetchone()[0] or 0
            res[id] = '%d / %d' % (open, all)
        return res
    
    _columns = {
                'eq_sale_count': fields.function(_eq_sale_count, type="char", string='Sales'),                
                'eq_rrp': fields.float(string='RRP'),
                'eq_sale_min_qty': fields.integer(string='Min. order quantity'),
                'attribute_value_ids': fields.many2many('product.attribute.value', id1='prod_id', id2='att_id', string='Attributes', readonly=False, ondelete='restrict'),
                }
    
    _defaults = {
                 'eq_sale_min_qty': 0,
    }
    
class eq_product_template_standard_price_history(osv.osv):
    _name = 'product.template.standard_price_history'
    
    _columns = {
                'eq_product_id': fields.many2one('product.template', string="Product"),
                'eq_old_price': fields.float(string="Old Price"),
                'eq_new_price': fields.float(string="New Price"),
                'create_uid': fields.many2one('res.users', string="User"),
                'create_date': fields.datetime(string="Create Date"),
                }
    
    
class eq_product_attribute_value(osv.osv):
    _inherit = 'product.attribute.value'
    _order = 'attribute_id, sequence'
    
    
    
    