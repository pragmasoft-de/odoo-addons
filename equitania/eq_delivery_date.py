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

from openerp.osv import fields, osv

from datetime import datetime, timedelta

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT

class eq_delivery_date(osv.osv):
    _inherit = "sale.order.line"
    
    _columns = {
                'eq_delivery_date': fields.date('Delivery Date'),
                }
    
    def on_change_delivery_date(self, cr, uid, ids, date_order, eq_delivery_date, context={}):
        values = {}
        if date_order and eq_delivery_date:
            date_order = datetime.strptime(date_order.split(' ')[0], OE_DFORMAT)
            eq_delivery_date = datetime.strptime(eq_delivery_date, OE_DFORMAT)
            
            delay = (eq_delivery_date - date_order).days
            
            values = {'delay': delay}
        return {'value': values,}
    
    def on_change_delay(self, cr, uid, ids, date_order, delay, context={}):
        values = {}
        if date_order and delay:
            date_order = datetime.strptime(date_order.split(' ')[0], OE_DFORMAT)
            eq_delivery_date = date_order + timedelta(days=int(delay))
            values = {
                      'eq_delivery_date': eq_delivery_date
                      }
        return {'value': values,}
        