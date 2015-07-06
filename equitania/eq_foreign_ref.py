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


class eq_foreign_ref(osv.osv):
    _inherit = 'res.partner'
    
    _columns = {
                'eq_foreign_ref': fields.char('Foreign reference'),
                }
        

class eq_purchase_order(osv.osv):
    _inherit = 'purchase.order'
    
    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        """
            Extension of standard function onchange_partner_id(...) which adds eq_foreign_ref as partner_ref  to result values
            
            @cr: cursor
            @uid: user id
            @ids: ids
            @partner_id: partner id
            @context: context
            @return: original values together with eq_foreign_ref stored in partner_ref
        """        
        original_values = super(eq_purchase_order, self).onchange_partner_id(cr, uid, ids, partner_id, context=context)
        if partner_id:
            partner = self.pool.get('res.partner')
            supplier = partner.browse(cr, uid, partner_id, context=context)            
            original_values['value']['partner_ref'] = supplier.eq_foreign_ref
        
        return original_values
        
            
class eq_sale_order(osv.osv):
    _inherit = 'sale.order'
    
    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        """
            Extension of standard function onchange_partner_id(...) which adds eq_foreign_ref as partner_ref  to result values
            
            @cr: cursor
            @uid: user id
            @ids: ids
            @partner_id: partner id
            @context: context
            @return: original values together with eq_foreign_ref stored in partner_ref
        """        
        original_values = super(eq_sale_order, self).onchange_partner_id(cr, uid, ids, partner_id, context)
        
        if partner_id:
            partner = self.pool.get('res.partner')
            customer = partner.browse(cr, uid, partner_id, context=context)   
            original_values['value']['client_order_ref'] = customer.eq_foreign_ref
        
        return original_values
        