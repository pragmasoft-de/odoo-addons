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
        'eq_creditor_ref': fields.char('Creditor Number', size=64),
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
        print '================================================='
        print eq_customer_ref
        vals['ref'] = eq_customer_ref
        return {'value': vals}

eq_custom_ref()

class eq_product_template(osv.osv):
    _name = 'product.template'
    _inherit = 'product.template'
    
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
    
    
    _columns = {
                'eq_drawing_number': fields.char('Drawing Number', size=50),
                'eq_index': fields.char('Index', size=64),
                'eq_default_code_dub': fields.function(_set_eq_default_code_dup, type='char', arg='context', method=True),
                'eq_state_dup': fields.function(_set_eq_state_dup, type='char', arg='context', method=True),
                'eq_internal_number': fields.char('Internal Number', size=64),
                'eq_internal_text': fields.char('Internal Info', size=255),
    }
    def eq_product_number_update(self, cr, uid, ids, context=None):
        #Gets the product
        product = self.pool.get('product.template').browse(cr, uid, ids, context)
        prod_rec = product[0].default_code
        #Deletes all spaces in the string
        if prod_rec:
            prod_rec = replace(prod_rec, '-', '')
            prod_rec = replace(prod_rec, ' ', '')
            if len(prod_rec) == 3:
                #Sql Query (self explaining), which gets the entries where prefix is identical to prefix.
                cr.execute("Select * From ir_sequence Where code=%s", ('product_no_purch.' + prod_rec, ))

                #cr.fetchone is a dictionary with the row from the database. which we got with cr.execute
                #If the sequence with the prefix is present, we just use the sequence
                if cr.fetchone():
                    #Gets the sequence for the and sets it in the appropriate field
                    vals = {
                        'default_code': self.pool.get('ir.sequence').get(cr, uid, 'product_no_purch.' + prod_rec)
                    }

                    super(eq_product_template, self).write(cr, uid, ids, vals, context=context)

                #Else we create that sequence and the sequence.type and use it
                else:
                    #Defines the sequence.type
                    vals_seq_type = {
                        'code': 'product_no_purch.' + prod_rec,
                        'name': 'Product Number Purchase SQ',
                    }

                    #Creates the sequence.type in OpenERP
                    self.pool.get('ir.sequence.type').create(cr, uid, vals_seq_type, context)

                    #Gets the company_id, which is needed for the sequence
                    user_rec = self.pool.get('res.users').browse(cr, uid, uid, context)
                    company_id = user_rec.company_id.id

                    #Defines the sequence and uses the ir.sequence.type that was previously created
                    vals_seq = {
                        'code': 'product_no_purch.' + prod_rec,
                        'suffix': '',
                        'number_next': 1,
                        'number_increment': 1,
                        'implementation': 'standard',
                        'company_id': company_id,
                        'padding': 5,
                        'active': True,
                        'prefix': prod_rec + '-',
                        'name': 'Product Number Purchase SQ',
                    }
                    #Creates the sequence in OpenERP
                    self.pool.get('ir.sequence').create(cr, uid, vals_seq, context=context)

                    #Gets the sequence for the and sets it in the appropriate field
                    vals = {
                        'default_code': self.pool.get('ir.sequence').get(cr, uid, 'product_no_purch.' + prod_rec)
                    }
                    super(eq_product_template, self).write(cr, uid, ids, vals, context=context)
            elif len(prod_rec) == 2:
                #Sql Query (self explaining), which gets the entries where prefix is identical to entered prefix
                cr.execute("Select * From ir_sequence Where code=%s", ('product_no_sale.' + prod_rec, ))

                #cr.fetchone is a dictionary with the row from the database. which we got with cr.execute
                #If the sequence with the prefix of entered prefix is present, we just use the sequence
                if cr.fetchone():
                    #Gets the sequence for the and sets it in the appropriate field
                    vals = {
                        'default_code': self.pool.get('ir.sequence').get(cr, uid, 'product_no_sale.' + prod_rec)
                    }

                    super(eq_product_template, self).write(cr, uid, ids, vals, context=context)

                #Else we create that sequence and the sequence.type and use it
                else:
                    #Defines the sequence.type
                    vals_seq_type = {
                        'code': 'product_no_sale.' + prod_rec,
                        'name': 'Product Number Sales SQ',
                    }

                    #Creates the sequence.type in OpenERP
                    self.pool.get('ir.sequence.type').create(cr, uid, vals_seq_type, context)

                    #Gets the company_id, which is needed for the sequence
                    user_rec = self.pool.get('res.users').browse(cr, uid, uid, context)
                    company_id = user_rec.company_id.id

                    #Defines the sequence and uses the ir.sequence.type that we created
                    vals_seq = {
                        'code': 'product_no_sale.' + prod_rec,
                        'suffix': '',
                        'number_next': 1,
                        'number_increment': 1,
                        'implementation': 'standard',
                        'company_id': company_id,
                        'padding': 5,
                        'active': True,
                        'prefix': prod_rec + '-',
                        'name': 'Product Number Purchase SQ',
                    }
                    #Creates the sequence in OpenERP
                    self.pool.get('ir.sequence').create(cr, uid, vals_seq, context=context)

                    #Gets the sequence for the and sets it in the appropriate field
                    vals = {
                        'default_code': self.pool.get('ir.sequence').get(cr, uid, 'product_no_sale.' + prod_rec)
                    }
                    super(eq_product_template, self).write(cr, uid, ids, vals, context=context)
    
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
    
    
    _columns = {
                'default_code' : fields.char('Product Number', select=True),
                'eq_drawing_number': fields.char('Drawing Number', size=50),
                'eq_index': fields.char('Index', size=64),
                'eq_default_code_dub': fields.function(_set_eq_default_code_dup, type='char', arg='context', method=True),
                'eq_state_dup': fields.function(_set_eq_state_dup, type='char', arg='context', method=True),
                'eq_internal_number': fields.char('Internal Number', size=64),
                'eq_internal_text': fields.char('Internal Info', size=255),
    }
    
    def eq_product_number_update(self, cr, uid, ids, context=None):
        #Gets the product
        product = self.pool.get('product.product').browse(cr, uid, ids, context)
        prod_rec = product[0].default_code
        #Deletes all spaces in the string
        if prod_rec:
            prod_rec = replace(prod_rec, '-', '')
            prod_rec = replace(prod_rec, ' ', '')
            if len(prod_rec) == 3:
                #Sql Query (self explaining), which gets the entries where prefix is identical to prefix.
                cr.execute("Select * From ir_sequence Where code=%s", ('product_no_purch.' + prod_rec, ))

                #cr.fetchone is a dictionary with the row from the database. which we got with cr.execute
                #If the sequence with the prefix is present, we just use the sequence
                if cr.fetchone():
                    #Gets the sequence for the and sets it in the appropriate field
                    vals = {
                        'default_code': self.pool.get('ir.sequence').get(cr, uid, 'product_no_purch.' + prod_rec)
                    }

                    super(eq_product_product, self).write(cr, uid, ids, vals, context=context)

                #Else we create that sequence and the sequence.type and use it
                else:
                    #Defines the sequence.type
                    vals_seq_type = {
                        'code': 'product_no_purch.' + prod_rec,
                        'name': 'Product Number Purchase SQ',
                    }

                    #Creates the sequence.type in OpenERP
                    self.pool.get('ir.sequence.type').create(cr, uid, vals_seq_type, context)

                    #Gets the company_id, which is needed for the sequence
                    user_rec = self.pool.get('res.users').browse(cr, uid, uid, context)
                    company_id = user_rec.company_id.id

                    #Defines the sequence and uses the ir.sequence.type that was previously created
                    vals_seq = {
                        'code': 'product_no_purch.' + prod_rec,
                        'suffix': '',
                        'number_next': 1,
                        'number_increment': 1,
                        'implementation': 'standard',
                        'company_id': company_id,
                        'padding': 5,
                        'active': True,
                        'prefix': prod_rec + '-',
                        'name': 'Product Number Purchase SQ',
                    }
                    #Creates the sequence in OpenERP
                    self.pool.get('ir.sequence').create(cr, uid, vals_seq, context=context)

                    #Gets the sequence for the and sets it in the appropriate field
                    vals = {
                        'default_code': self.pool.get('ir.sequence').get(cr, uid, 'product_no_purch.' + prod_rec)
                    }
                    super(eq_product_product, self).write(cr, uid, ids, vals, context=context)
            elif len(prod_rec) == 2:
                #Sql Query (self explaining), which gets the entries where prefix is identical to entered prefix
                cr.execute("Select * From ir_sequence Where code=%s", ('product_no_sale.' + prod_rec, ))

                #cr.fetchone is a dictionary with the row from the database. which we got with cr.execute
                #If the sequence with the prefix of entered prefix is present, we just use the sequence
                if cr.fetchone():
                    #Gets the sequence for the and sets it in the appropriate field
                    vals = {
                        'default_code': self.pool.get('ir.sequence').get(cr, uid, 'product_no_sale.' + prod_rec)
                    }

                    super(eq_product_product, self).write(cr, uid, ids, vals, context=context)

                #Else we create that sequence and the sequence.type and use it
                else:
                    #Defines the sequence.type
                    vals_seq_type = {
                        'code': 'product_no_sale.' + prod_rec,
                        'name': 'Product Number Sales SQ',
                    }

                    #Creates the sequence.type in OpenERP
                    self.pool.get('ir.sequence.type').create(cr, uid, vals_seq_type, context)

                    #Gets the company_id, which is needed for the sequence
                    user_rec = self.pool.get('res.users').browse(cr, uid, uid, context)
                    company_id = user_rec.company_id.id

                    #Defines the sequence and uses the ir.sequence.type that we created
                    vals_seq = {
                        'code': 'product_no_sale.' + prod_rec,
                        'suffix': '',
                        'number_next': 1,
                        'number_increment': 1,
                        'implementation': 'standard',
                        'company_id': company_id,
                        'padding': 5,
                        'active': True,
                        'prefix': prod_rec + '-',
                        'name': 'Product Number Purchase SQ',
                    }
                    #Creates the sequence in OpenERP
                    self.pool.get('ir.sequence').create(cr, uid, vals_seq, context=context)

                    #Gets the sequence for the and sets it in the appropriate field
                    vals = {
                        'default_code': self.pool.get('ir.sequence').get(cr, uid, 'product_no_sale.' + prod_rec)
                    }
                    super(eq_product_product, self).write(cr, uid, ids, vals, context=context)