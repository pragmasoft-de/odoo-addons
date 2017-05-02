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

class eq_stock_transfer_details(models.TransientModel):
    _name = 'stock.transfer_details'
    _inherit = 'stock.transfer_details'
    
 
    @api.one
    def do_detailed_transfer(self):
        """
            Inherited the existing method()
        """
        is_shipcloud = False
        eq_shipcloud_obj = self.pool.get('eq.shipcloud')
        stock_picking_obj = self.pool.get('stock.picking')
        res = super(eq_stock_transfer_details, self).do_detailed_transfer()
        if res and stock_picking_obj.browse(self._cr,self._uid,self.picking_id.id,context=None).eq_is_shipped == False:
            result = eq_shipcloud_obj.eq_create_shipments(self._cr,self._uid,self.picking_id.id,context=None)
            
            if result :
                is_shipcloud = eq_shipcloud_obj.eq_create_shipcloud(self._cr,self._uid,result,context=None)
                
            if not is_shipcloud or not result:
#               current transaction be rollback
                self._cr.rollback()
                stock_picking_obj.action_cancel(self._cr,self._uid, self.picking_id.id, context=None)
                stock_picking_obj.write(self._cr,self._uid,self.picking_id.id,{'eq_state': 'eq_shipment_error','eq_reason': "CODE " +str(result[0].get('response').status_code )+ ": " + result[0].get('response').reason},context=None)
        return True