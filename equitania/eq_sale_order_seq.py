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
#from reportlab.rl_config import _DEFAULTS
#from numpy.ma.core import ids

#Shows the sequence of the sale.order.line

class eq_sale_order_seq(osv.osv):
    _inherit = "sale.order"
    _columns = { 
    }    
    

eq_sale_order_seq()

class eq_sale_order_line_seq(osv.osv):
    _inherit = "sale.order.line"
    SEQUENCE_VALUE = 10
    
    def default_get(self, cr, uid, ids, context=None):
        res =  super(eq_sale_order_line_seq, self).default_get(cr, uid, ids, context=context)        
        if context:
            context_keys = context.keys()
            next_sequence = self.SEQUENCE_VALUE
            if 'ref_ids' in context_keys:
                if len(context.get('ref_ids')) > 0:
                    next_sequence = (len(context.get('ref_ids')) + 1) * self.SEQUENCE_VALUE
        
        res.update({'sequence': next_sequence})
        return res
    
        
eq_sale_order_seq()


class eq_product_name_is_ref(osv.osv):
    _inherit = "product.product"
    
    _columns = {
    }
    
    def name_get(self, cr, uid, ids, context={}):
        if context.get('eq_only_ref'):
            res = []
            for id in ids:
                elmt = super(eq_product_name_is_ref, self).browse(cr, uid, id, context)
                res.append((id, str(elmt.default_code)))
            return res
        else:
            return super(eq_product_name_is_ref, self).name_get(cr, uid, ids, context=context)
    
eq_product_name_is_ref()