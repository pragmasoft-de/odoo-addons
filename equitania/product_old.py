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
from datetime import datetime
from string import replace
from openerp import SUPERUSER_ID
from openerp.tools.translate import _

from openerp import models, api


class eq_product_template(osv.osv):
    _inherit = 'product.template'
    _order = 'eq_default_code_copy'
    
    def _set_eq_default_code_dup(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            record = self.browse(cr, uid, id)
            res.update({id:record.default_code})
        return res
    
    def _reset_default_code(self, cr, uid, ids, context=None):
        """
            Trigger function which will be called after change of trigger fields in product.product table
            @self: self
            @cr: cursor
            @uid: user id
            @ids: ids of record from product.product
            @return: list of ids of the source model whose function field values need to be recomputed
        """
        result = {}
        for line in self.pool.get('product.product').browse(cr, uid, ids, context=context):            
            result[line.product_tmpl_id.id] = line.default_code                    

        return result.keys()
    
    def _set_eq_state_dup(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            record = self.browse(cr, uid, id)
            res.update({id:record.state})
        return res
    
    def _eq_pricleist_items_count(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            cr.execute("""select count(*) from product_pricelist_item where product_tmpl_id = %d""" % (id))
            all = cr.fetchone() or [0]
            res[id] = '%d' % (all[0])
        return res
    
    def _eq_invoice_count_out(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            cr.execute("""select count(id) from account_invoice where type = 'out_invoice' and id in (select invoice_id from account_invoice_line where product_id   in (select id from product_product where product_tmpl_id = %d) group by invoice_id)""" % (id))
            all = cr.fetchone() or [0]
            res[id] = '%d' % (all[0])
        return res
    
    def _eq_invoice_count_in(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            cr.execute("""select count(id) from account_invoice where type = 'in_invoice' and id in (select invoice_id from account_invoice_line where product_id   in (select id from product_product where product_tmpl_id = %d) group by invoice_id)""" % (id))
            all = cr.fetchone() or [0]
            res[id] = '%d' % (all[0])
        return res
    
    def _eq_sale_count(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            cr.execute("""select sum(product_uom_qty) from stock_move where procurement_id in 
            (select id from procurement_order where sale_line_id in 
            (select id from sale_order_line as sol where sol.product_id in 
            (select id from product_product where product_tmpl_id = %d) 
            and sol.state not in ('cancel', 'done') 
            and (select state from sale_order where id = sol.order_id) not in ('sent', 'draft'))) 
            and state != 'done'""" % (id))
            open = cr.fetchone()[0] or 0
            cr.execute("""select sum(product_uom_qty) from sale_order_line where product_id in (select id from product_product where product_tmpl_id = %d) and state != 'cancel' and (select state from sale_order where id = order_id) not in ('sent', 'draft')""" % (id))
            all = cr.fetchone()[0] or 0
            res[id] = '%d / %d' % (open, all)
        return res
    
    
    def action_view_invoice_out(self, cr, uid, ids, context=None):
        cr.execute("""select id from account_invoice where type = 'out_invoice' and id in (select invoice_id from account_invoice_line where product_id   in (select id from product_product where product_tmpl_id = %d) group by invoice_id)""" % (ids[0]))
        all = cr.fetchall() or [0]
            
        result = self._get_act_window_dict(cr, uid, 'account.action_invoice_tree1', context=context)
        result['domain'] = "[('id','in',[" + ','.join(map(str, all)) + "])]"
        return result
    
    def action_view_invoice_in(self, cr, uid, ids, context=None):
        cr.execute("""select id from account_invoice where type = 'in_invoice' and id in (select invoice_id from account_invoice_line where product_id   in (select id from product_product where product_tmpl_id = %d) group by invoice_id)""" % (ids[0]))
        all = cr.fetchall() or [0]
            
        result = self._get_act_window_dict(cr, uid, 'account.action_invoice_tree2', context=context)
        result['domain'] = "[('id','in',[" + ','.join(map(str, all)) + "])]"
        return result
    
    def eq_product_number_update(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product')
        #Gets the product
        product = self.pool.get('product.template').browse(cr, uid, ids, context)
        prod_rec = product[0].default_code
        product_variant = product[0].product_variant_ids[0].id
        
        #Gets the config values for the product number
        ir_values = self.pool.get('ir.values')
        min_prefix_count = ir_values.get_default(cr, uid, 'product.product', 'default_eq_min_prefix_count')
        max_prefix_count = ir_values.get_default(cr, uid, 'product.product', 'default_eq_max_prefix_count')
        prod_num_lenght = ir_values.get_default(cr, uid, 'product.product', 'default_eq_prod_num_lenght')
        seperator = ir_values.get_default(cr, uid, 'product.product', 'default_eq_seperator')
        #Deletes all spaces in the string
        if prod_rec:
            prod_rec = replace(prod_rec, ' ', '')
            if seperator: 
                prod_rec = replace(prod_rec, seperator, '')
        else:
            prod_rec = ''
            seperator = ''
        if len(prod_rec) >= min_prefix_count and  len(prod_rec) <= max_prefix_count:
            #Sql Query (self explaining), which gets the entries where prefix is identical to prefix.
            cr.execute("Select * From ir_sequence Where code=%s", ('eq_product_no.' + prod_rec, ))
    
            #cr.fetchone is a dictionary with the row from the database. which we got with cr.execute
            #If the sequence with the prefix is present, we just use the sequence
            if cr.fetchone():
                #Gets the sequence for the and sets it in the appropriate field
                seq = self.pool.get('ir.sequence').get(cr, uid, 'eq_product_no.' + prod_rec)
                vals = {
                    'default_code': seq
                }
    
                product_obj.write(cr, uid, product_variant, vals, context=context)
                if prod_rec == '' and max_prefix_count == 0 :
                    company_ean = self.pool.get('res.users').browse(cr, uid, uid, context).company_id.eq_company_ean
                    if company_ean:
                        product_obj._generate_ean(cr, uid, product_variant, company_ean, seq, context)
    
            #Else we create that sequence and the sequence.type and use it
            else:
                #Defines the sequence.type
                vals_seq_type = {
                    'code': 'eq_product_no.' + prod_rec,
                    'name': 'Product Number ' + prod_rec,
                }
    
                #Creates the sequence.type in OpenERP
                self.pool.get('ir.sequence.type').create(cr, SUPERUSER_ID, vals_seq_type, context)
    
                #Gets the company_id, which is needed for the sequence
                user_rec = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid, context)
                company_id = user_rec.company_id.id
    
                #Defines the sequence and uses the ir.sequence.type that was previously created
                vals_seq = {
                    'code': 'eq_product_no.' + prod_rec,
                    'suffix': '',
                    'number_next': 1,
                    'number_increment': 1,
                    'implementation': 'standard',
                    'company_id': company_id,
                    'padding': prod_num_lenght,
                    'active': True,
                    'prefix': prod_rec + seperator,
                    'name': 'Product Number ' + prod_rec,
                }
                #Creates the sequence in OpenERP
                self.pool.get('ir.sequence').create(cr, SUPERUSER_ID, vals_seq, context=context)
    
                #Gets the sequence for the and sets it in the appropriate field
                seq = self.pool.get('ir.sequence').get(cr, SUPERUSER_ID, 'eq_product_no.' + prod_rec)
                vals = {
                    'default_code': seq
                }
                product_obj.write(cr, uid, product_variant, vals, context=context)
                if prod_rec == '' and max_prefix_count == 0:
                    company_ean = self.pool.get('res.users').browse(cr, uid, uid, context).company_id.eq_company_ean
                    if company_ean:
                        product_obj._generate_ean(cr, uid, product_variant, company_ean, seq, context)
    
    _columns = {
                'eq_sale_count': fields.function(_eq_sale_count, type="char", string='Sales'),
                #'eq_sale_min_qty': fields.integer(string='Min. order quantity'),
                'eq_drawing_number': fields.char('Drawing Number', size=50),
                'eq_index': fields.char('Index', size=64),
                'eq_default_code_copy': fields.function(_set_eq_default_code_dup, type='char', arg='context', method=True, store={'product.product' : (_reset_default_code, ['default_code'], 10)}),                
                'eq_state_dup': fields.function(_set_eq_state_dup, type='char', arg='context', method=True),
                'eq_internal_number': fields.char('Internal Number', size=64),
                'eq_internal_text': fields.char('Internal Info', size=255),
                'default_code': fields.related('product_variant_ids', 'default_code', type='char', string='Internal Reference'),
                'eq_pricelist_items_count': fields.function(_eq_pricleist_items_count, type="char", method=True),
                'eq_invoice_count_out': fields.function(_eq_invoice_count_out, type="char", methode=True),
                'eq_invoice_count_in': fields.function(_eq_invoice_count_in, type="char", methode=True),                
                }
    
    _defaults = {
                'categ_id': False,
    }
    
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
    
    
    def name_get(self, cr, uid, ids, context={}):
        if context.get('eq_only_ref'):
            res = []
            for id in ids:
                elmt = super(eq_product_name_is_ref, self).browse(cr, uid, id, context)
                res.append((id, str(elmt.default_code)))
            return res
        else:
            return super(eq_product_name_is_ref, self).name_get(cr, uid, ids, context=context)
        
    
    def _set_eq_default_code_dup(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            record = self.browse(cr, uid, id)
            res.update({id:record.default_code})
        return res
    
    def _set_eq_state_dup(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            record = self.browse(cr, uid, id)
            res.update({id:record.state})
        return res
    
    def _get_partner_code_name(self, cr, uid, ids, product, partner_id, context=None):
        for supinfo in product.seller_ids:
            if supinfo.name.id == partner_id:
                return {'code': supinfo.product_code or product.default_code,'default_code': product.default_code, 'name': supinfo.product_name or product.name}
        res = {'code': product.default_code,'default_code': product.default_code, 'name': product.name}
        return res
    
    def _eq_pricleist_items_count(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            cr.execute("""select count(*) from product_pricelist_item where product_id = %d""" % (id))
            all = cr.fetchone() or [0]
            res[id] = '%d' % (all[0])
        return res
    
    def _eq_invoice_count_out(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            cr.execute("""select count(id) from account_invoice where type = 'out_invoice' and id in (select invoice_id from account_invoice_line where product_id = %d group by invoice_id)""" % (id))
            all = cr.fetchone() or [0]
            res[id] = '%d' % (all[0])
        return res
    
    def _eq_invoice_count_in(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            cr.execute("""select count(id) from account_invoice where type = 'in_invoice' and id in (select invoice_id from account_invoice_line where product_id = %d group by invoice_id)""" % (id))
            all = cr.fetchone() or [0]
            res[id] = '%d' % (all[0])
        return res
    
    def _eq_sale_count(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            cr.execute("""select sum(product_uom_qty) from stock_move where procurement_id in 
            (select id from procurement_order where sale_line_id in 
            (select id from sale_order_line as sol where sol.product_id  = %d 
            and sol.state not in ('cancel', 'done') 
            and (select state from sale_order where id = sol.order_id) not in ('sent', 'draft'))) 
            and state != 'done'""" % (id))
            open = cr.fetchone()[0] or 0
            cr.execute("""select sum(product_uom_qty) from sale_order_line where product_id = %d and state != 'cancel' 
            and (select state from sale_order where id = order_id) not in ('sent', 'draft')""" % (id))
            all = cr.fetchone()[0] or 0
            res[id] = '%d / %d' % (open, all)
        return res
    
    def action_view_invoice_out(self, cr, uid, ids, context=None):
        cr.execute("""select id from account_invoice where type = 'out_invoice' and id in (select invoice_id from account_invoice_line where product_id = %d group by invoice_id)""" % (ids[0]))
        all = cr.fetchall() or [0]
            
        result = self.pool.get('product.template')._get_act_window_dict(cr, uid, 'account.action_invoice_tree1', context=context)
        result['domain'] = "[('id','in',[" + ','.join(map(str, all)) + "])]"
        return result
    
    def action_view_invoice_in(self, cr, uid, ids, context=None):
        cr.execute("""select id from account_invoice where type = 'in_invoice' and id in (select invoice_id from account_invoice_line where product_id = %d group by invoice_id)""" % (ids[0]))
        all = cr.fetchall() or [0]
            
        result = self.pool.get('product.template')._get_act_window_dict(cr, uid, 'account.action_invoice_tree2', context=context)
        result['domain'] = "[('id','in',[" + ','.join(map(str, all)) + "])]"
        return result
    
    def _generate_ean(self, cr, uid, ids, company_ean, sequence, context):
        ean_without_checksum = company_ean + sequence[-5:]
        
        oddsum = 0
        evensum = 0
        for i in range(0, len(ean_without_checksum)):
            if i % 2 == 0:
                oddsum += int(ean_without_checksum[i])
            else:
                evensum += int(ean_without_checksum[i])
        total= oddsum + (evensum * 3)
        checksum = int(10 - total % 10.0) %10
        if checksum == 10:
            checksum == 0
        ean13 = ean_without_checksum + str(checksum)
        self.write(cr, uid, ids ,{'ean13': ean13}, context)
    
    def eq_product_number_update(self, cr, uid, ids, context=None):
        #Gets the product
        product = self.pool.get('product.product').browse(cr, uid, ids, context)
        prod_rec = product[0].default_code
        
        #Gets the config values for the product number
        ir_values = self.pool.get('ir.values')
        min_prefix_count = ir_values.get_default(cr, uid, 'product.product', 'default_eq_min_prefix_count')
        max_prefix_count = ir_values.get_default(cr, uid, 'product.product', 'default_eq_max_prefix_count')
        prod_num_lenght = ir_values.get_default(cr, uid, 'product.product', 'default_eq_prod_num_lenght')
        seperator = ir_values.get_default(cr, uid, 'product.product', 'default_eq_seperator')
        #Deletes all spaces in the string
        if prod_rec:
            prod_rec = replace(prod_rec, ' ', '')
            if seperator: 
                prod_rec = replace(prod_rec, seperator, '')
        else:
            prod_rec = ''
            seperator = ''
        if len(prod_rec) >= min_prefix_count and  len(prod_rec) <= max_prefix_count:
            #Sql Query (self explaining), which gets the entries where prefix is identical to prefix.
            cr.execute("Select * From ir_sequence Where code=%s", ('eq_product_no.' + prod_rec, ))
    
            #cr.fetchone is a dictionary with the row from the database. which we got with cr.execute
            #If the sequence with the prefix is present, we just use the sequence
            if cr.fetchone():
                #Gets the sequence for the and sets it in the appropriate field
                seq = self.pool.get('ir.sequence').get(cr, uid, 'eq_product_no.' + prod_rec)
                vals = {
                    'default_code': seq
                }
    
                super(eq_product_product, self).write(cr, uid, ids, vals, context=context)
                if prod_rec == '' and max_prefix_count == 0 :
                    company_ean = self.pool.get('res.users').browse(cr, uid, uid, context).company_id.eq_company_ean
                    if company_ean:
                        self._generate_ean(cr, uid, ids, company_ean, seq, context)
    
            #Else we create that sequence and the sequence.type and use it
            else:
                #Defines the sequence.type
                vals_seq_type = {
                    'code': 'eq_product_no.' + prod_rec,
                    'name': 'Product Number ' + prod_rec,
                }
    
                #Creates the sequence.type in OpenERP
                self.pool.get('ir.sequence.type').create(cr, uid, vals_seq_type, context)
    
                #Gets the company_id, which is needed for the sequence
                user_rec = self.pool.get('res.users').browse(cr, uid, uid, context)
                company_id = user_rec.company_id.id
    
                #Defines the sequence and uses the ir.sequence.type that was previously created
                vals_seq = {
                    'code': 'eq_product_no.' + prod_rec,
                    'suffix': '',
                    'number_next': 1,
                    'number_increment': 1,
                    'implementation': 'standard',
                    'company_id': company_id,
                    'padding': prod_num_lenght,
                    'active': True,
                    'prefix': prod_rec + seperator,
                    'name': 'Product Number ' + prod_rec,
                }
                #Creates the sequence in OpenERP
                self.pool.get('ir.sequence').create(cr, uid, vals_seq, context=context)
    
                #Gets the sequence for the and sets it in the appropriate field
                seq = self.pool.get('ir.sequence').get(cr, uid, 'eq_product_no.' + prod_rec)
                vals = {
                    'default_code': seq
                }
                super(eq_product_product, self).write(cr, uid, ids, vals, context=context)
                if prod_rec == '' and max_prefix_count == 0:
                    company_ean = self.pool.get('res.users').browse(cr, uid, uid, context).company_id.eq_company_ean
                    if company_ean:
                        self._generate_ean(cr, uid, ids, company_ean, seq, context)
    
    _columns = {
                'eq_sale_count': fields.function(_eq_sale_count, type="char", string='Sales'),                
                'eq_rrp': fields.float(string='RRP'),
                'eq_sale_min_qty': fields.integer(string='Min. order quantity'),
                'default_code' : fields.char('Product Number', select=True),
                'eq_drawing_number': fields.char('Drawing Number', size=50),
                'eq_index': fields.char('Index', size=64),
                'eq_default_code_dub': fields.function(_set_eq_default_code_dup, type='char', arg='context', method=True),
                'eq_state_dup': fields.function(_set_eq_state_dup, type='char', arg='context', method=True),
                'eq_internal_number': fields.char('Internal Number', size=64),
                'eq_internal_text': fields.char('Internal Info', size=255),
                'eq_pricelist_items_count': fields.function(_eq_pricleist_items_count, type="char", method=True),
                'eq_invoice_count_out': fields.function(_eq_invoice_count_out, type="char", methode=True),
                'eq_invoice_count_in': fields.function(_eq_invoice_count_in, type="char", methode=True),
                }
    
    _defaults = {
                 'eq_sale_min_qty': 0,
                 'categ_id': False,
                 'lst_price': 0,
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
    

class eq_product_pricelist_item(osv.osv):
    _inherit = 'product.pricelist.item'
    
    
    def _get_default_price_version_id(self, cr, uid, context):
        """
            Return first id from product.pricelist.version and set it as actual one
            @return: False or id
        """        
        result = False
        versions = self.pool.get('product.pricelist.version').search(cr, uid, [], context=context)
        if versions:
            result = versions[0]

            
        return result
    
    
    def delete(self, cr, uid, ids, context=None):
        self.unlink(cr,uid,ids,context)
        return True
    
    
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = _("%s, Min. %s New Price %s") % (record.name, record.min_quantity, record.price_surcharge)
            res.append((record.id, name))
        return res
    
    """
    def set_defaults(self, cr, uid, ids, context=None):        
        # Set defalt values for pricelist after click on button 'set defaults'
        res = {}
        for id in ids:
            record = self.browse(cr, uid, id)
            record.min_quantity = 1
            record.base = 1
            record.price_discount = -1
                        
            versions = self.pool.get('product.pricelist.version').search(cr, uid, [], context=context)
            if versions:
                    record.price_version_id = versions[0]          
        return res
    """
    
    
    _defaults = {
        'min_quantity': 1,
        'price_discount': -1,
        'base': 1,           
        'price_version_id' : lambda self, cr, uid, context: self._get_default_price_version_id(cr, uid, context),
    }
    
        
eq_product_pricelist_item()


class eq_pricelist_item_search(osv.osv):
    _name = "eq_pricelist_item_search"

    _columns = {
        'eq_pricelist_version_id': fields.many2one('product.pricelist.version', 'Pricelist Version'),
        'eq_items_id': fields.many2one('product.pricelist.item', 'Item'),
    }
    # Opens a pup-up window with the selected pricelist version
    def open(self, cr, uid, ids, context={}):
        mod_obj = self.pool.get('ir.model.data')
        item = self.pool.get('eq_pricelist_item_search').browse(cr, uid, ids, context)
        cr.execute("DELETE FROM eq_pricelist_item_search",)
        res = mod_obj.get_object_reference(cr, uid, 'equitania', 'eq_pricelist_item_search_item_form')

        return {
            'name': 'Item',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res and res[1] or False],
            'res_model': 'product.pricelist.item',
            'context': "{}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'res_id': context['item'] or False,
        }
        
eq_pricelist_item_search()