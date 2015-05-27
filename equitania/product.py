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

class eq_product_template(osv.osv):
    _inherit = 'product.template'
    
    def _eq_sale_count(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            cr.execute("""select sum(product_uom_qty) from sale_order_line where product_id in (select id from product_product where product_tmpl_id = %d) and state not in ('cancel', 'done')""" % (id))
            open = cr.fetchone()[0] or 0
            cr.execute("""select sum(product_uom_qty) from sale_order_line where product_id in (select id from product_product where product_tmpl_id = %d) and state != 'cancel'""" % (id))
            all = cr.fetchone()[0] or 0
            res[id] = '%d / %d' % (open, all)
        return res
    
    _columns = {
                'eq_sale_count': fields.function(_eq_sale_count, type="char", string='Sales'),                
                }
    
    def action_view_stock_moves(self, cr, uid, ids, context=None):
        result = super(eq_product_template, self).action_view_stock_moves(cr, uid, ids, context=context)
        result['context'] = result['context'][:-1] + ", 'search_default_in_and_out': 1" + result['context'][-1]
        return result
    
class eq_product_product(osv.osv):
    _inherit = 'product.product'
    
    def _eq_sale_count(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            cr.execute("""select sum(product_uom_qty) from sale_order_line where product_id = %d and state not in ('cancel', 'done')""" % (id))
            open = cr.fetchone()[0] or 0
            cr.execute("""select sum(product_uom_qty) from sale_order_line where product_id = %d and state != 'cancel'""" % (id))
            all = cr.fetchone()[0] or 0
            res[id] = '%d / %d' % (open, all)
        return res
    
    _columns = {
                'eq_sale_count': fields.function(_eq_sale_count, type="char", string='Sales'),                
                }