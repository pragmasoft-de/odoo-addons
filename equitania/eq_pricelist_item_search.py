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
from openerp.tools.translate import _

#Adds a Search for the Positions of a pricelist.

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
        
class eq_product_pricelist_item_search_item(osv.osv):
    _inherit = 'product.pricelist.item'
    
    _columns = {}

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