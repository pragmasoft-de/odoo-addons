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
            args.append(['product_tmpl_id', 'in', product_ids])
            #args.append(['id', 'in', product_ids])
        res = super(eq_product_product_new_api, self).name_search(name, args=args, operator=operator, limit=limit)    
        #res = super(eq_product_product_new_api, self).name_search(name, args=args, operator=operator, limit=limit)
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
            and sol.state not in ('cancel') 
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
    
    # TODO: ! Step 1
#     def copy(self, cr, uid, id, default=None, context=None):
#         
#         print "*** COPY ***"
#         print "* id: ", id
#         print "* default: ", default
#         print "* context: ", context
        
#         sql = "delete from product_attribute_value_product_product_rel where prod_id = '" + str(id) + "'"
#         cr.execute(sql)
#         record = cr.fetchone()
     
        
        
        """
        hier noch attribute löschen        
        """
        
        """
        old_id = context['active_id']        
        
        self.new_product_template = self.copy_product(cr, uid, ids, context)
        self.copy_bom(old_id, cr, uid, ids, context)
        self.copy_workplan(cr, uid, ids, context)
        
        # open new created copy of product on new page
        return self.open_product(cr, uid, self.new_product_template.id, context)
        """
    
    # def _get_partner_code_name(self, cr, uid, ids, product, partner_id, context=None):
#     def _get_product_tmpl_id_for_product(self, cr, uid, ignored_product_id, context=None):
#         
#         sql = "select product_tmpl_id from product_product where id = '" + str(ignored_product_id) + "'"
#         cr.execute(sql)
#         record = cr.fetchone()
#         return record[0]
#     
#     def _get_products_for_template(self, cr, uid, ignored_product_id, context=None):        
#         result = []
#         product_tmpl_id = self._get_product_tmpl_id_for_product(cr, uid, ignored_product_id, context)                
#         """
#         select id from product_product where product_tmpl_id = 196 and id != 4478
#         
#         select id from product_product where product_tmpl_id = product_tmpl_id and id != ignored_product_id
#         
#         liefert eine liste mit allen product_ids zurück
#         
#         [1, 2, 3, 4,]
#         """
#         list_product_ids = "select id from product_product where product_tmpl_id =" + str(product_tmpl_id) + "and id !=" + str(ignored_product_id)
#         cr.execute(list_product_ids)
#         records = cr.fetchall()
#         for record in records:
#             result.append(record[0])
#         
#         return result
#     
#     
#     # TODO: ! das implementieren !
#     def write(self, cr, uid, ids, values, context={}):
#         if context == None:    
#             context = {}
#                 
#         print "***** write *****"
#         print "* values: ", values
#         print type(values)
#         
#         attribute_ids = []
#         if 'attribute_value_ids' in values:
#             attr_ids = values['attribute_value_ids']
#             for x in attr_ids:
#                 attribute_ids = x[2]
#                                         
#                           
#             # hier logik implementieren
#             product_id = ids
#             print "attribute_ids: ", attribute_ids            
#             count_of_attributes_from_user = len(attribute_ids)
#             
#             
#             # get attributes of EACH saved product.product 
#             existing_product_ids_for_actual_template = self._get_products_for_template(cr, uid, ids[0], context)            
#             print"existing_product_ids_for_actual_template:", existing_product_ids_for_actual_template
#             
#             save_is_possible = True
#             for existing_product_id in existing_product_ids_for_actual_template:            
#                 attributes_from_db = []
#                 sql = "select att_id from product_attribute_value_product_product_rel where prod_id = '" + str(existing_product_id) + "'"
#                 cr.execute(sql)
#                 records = cr.fetchall()
#                 for record in records:
#                     att_id = record[0]
#                     print "att_id: ", att_id
#                     attributes_from_db.append(att_id)
#                   
#                 count_of_attributes_from_db = len(attributes_from_db)
#                 print "attributes_from_db: ", attributes_from_db
#                 print "count_of_attributes_from_db: ", count_of_attributes_from_db
#                                                             
#                 if count_of_attributes_from_db == count_of_attributes_from_user:
#                     print"Anzahl ist gleich"
#                     if attributes_from_db == attribute_ids:
#                         print"Attribute sind auch gleich"
#                         #Fehlermeldung
#                         save_is_possible = False                
#             
#             if save_is_possible:
#                 return super(eq_product_product, self).write(cr, uid, ids, values, context=context)
#         
        #can_save = False
        
       
#         if can_save:
#             res = super(eq_product_product, self).write(cr, uid, ids, values, context=context)
#             print "* write - result: ", res
#         else:
#             # warnung ausgeben
#             print "*** update nicht möglich, variante bereits vorhanden ***"
#         
#         return res
#       
    
    
    
    
    _columns = {
                'eq_sale_count': fields.function(_eq_sale_count, type="char", string='Sales'),                
                'eq_rrp': fields.float(string='RRP'),
                'eq_sale_min_qty': fields.integer(string='Min. order quantity'),
                #'attribute_value_ids': fields.many2many('product.attribute.value', id1='prod_id', id2='att_id', string='Attributes', readonly=False, ondelete='restrict', copy=False),
                #'attribute_value_ids': fields.many2many('product.attribute.value', id1='prod_id', id2='att_id', string='Attributes', readonly=True, ondelete='restrict', copy=False),
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
    
    
    
    
    
    
    