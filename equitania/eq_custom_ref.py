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

#The customer and creditor number with the appropriate sequence

class eq_custom_ref(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _columns = {
        'eq_creditor_ref': fields.char('Supplier Number', size=64),
        'eq_customer_ref': fields.char('Customer Number', size=64)
    }

    def eq_creditor_update(self, cr, uid, ids, context=None):
        #Gets the Partner
        partner = self.pool.get('res.partner').browse(cr, uid, ids, context=context)

        #If the field isn't filled, it should do this
        if not partner[0].eq_creditor_ref:
            #Gets the sequence and sets it in the apropriate field
            vals = {
                'eq_creditor_ref': self.pool.get('ir.sequence').get(cr, uid, 'eq_creditor_ref')
            }

            super(eq_custom_ref, self).write(cr, uid, ids, vals, context=context)


    def eq_customer_update(self, cr, uid, ids, context=None):
        #Gets the Partner
        partner = self.pool.get('res.partner').browse(cr, uid, ids, context=context)

        #If the field isn't filled, it should do this
        if not partner[0].eq_customer_ref:
                #Gets the sequence and sets it in the apropriate field
                ref = self.pool.get('ir.sequence').get(cr, uid, 'eq_customer_ref')
                vals = {
                    'eq_customer_ref': ref,
                    'ref': ref,
                }

                super(eq_custom_ref, self).write(cr, uid, ids, vals, context=context)
    
    def on_change_customer_ref(self, cr, uid, ids, eq_customer_ref, context=None):
        vals = {}
        vals['ref'] = eq_customer_ref
        return {'value': vals}

eq_custom_ref()

class eq_product_template(osv.osv):
    _name = 'product.template'
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
    
    # changed default_code to required field
    _columns = {
                'eq_drawing_number': fields.char('Drawing Number', size=50),
                'eq_index': fields.char('Index', size=64),
                'eq_default_code_copy': fields.function(_set_eq_default_code_dup, type='char', arg='context', method=True, store={'product.product' : (_reset_default_code, ['default_code'], 10)}),                
                'eq_state_dup': fields.function(_set_eq_state_dup, type='char', arg='context', method=True),
                'eq_internal_number': fields.char('Internal Number', size=64),
                'eq_internal_text': fields.char('Internal Info', size=255),
                'default_code': fields.related('product_variant_ids', 'default_code', type='char', string='Internal Reference'),
                'eq_pricelist_items_count': fields.function(_eq_pricleist_items_count, type="char", method=True)
    }
    
    # default setting to make sure, that no "Interne Kategorie" by default selected is
    _defaults = {
                'categ_id': False,
    }
    
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
                product_obj.write(cr, uid, product_variant, vals, context=context)
                if prod_rec == '' and max_prefix_count == 0:
                    company_ean = self.pool.get('res.users').browse(cr, uid, uid, context).company_id.eq_company_ean
                    if company_ean:
                        product_obj._generate_ean(cr, uid, product_variant, company_ean, seq, context)
        
        
eq_product_template()  


class eq_product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    
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
    
    # changed default_code to required field
    _columns = {
                'default_code' : fields.char('Product Number', select=True),
                'eq_drawing_number': fields.char('Drawing Number', size=50),
                'eq_index': fields.char('Index', size=64),
                'eq_default_code_dub': fields.function(_set_eq_default_code_dup, type='char', arg='context', method=True),
                'eq_state_dup': fields.function(_set_eq_state_dup, type='char', arg='context', method=True),
                'eq_internal_number': fields.char('Internal Number', size=64),
                'eq_internal_text': fields.char('Internal Info', size=255),
                'eq_pricelist_items_count': fields.function(_eq_pricleist_items_count, type="char", method=True)
    }
    
    # default setting to make sure, that no "Interne Kategorie" by default selected is
    _defaults = {
                'categ_id': False,
                'lst_price': 0,
    }
    
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