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

# 
from openerp.osv import osv, fields
from datetime import timedelta
from datetime import datetime
import time

class bonus_return(osv.osv):
    _name = "bonus.return"

    def _get_cust(self, cr, uid, context=None):
        users_obj = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        company_id = users_obj.company_id.id
        return company_id

    _columns = {
        'company_id': fields.many2one('res.company', 'Company', readonly=True), 
        'name': fields.char('Description', size=128),
        'date_create': fields.date('Issue Date', readonly=True),
        'bonus_amount': fields.float('Amount'),
        'bonus_remaining_amt': fields.float('Remaining Amount', readonly=True),
        'bonus_history': fields.one2many('pos.bonus.history', 'bonus_return_id', 'Hostory Lines', readonly=True)
    }
    _defaults = {
        'company_id': _get_cust,
        'date_create': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        date_create = time.strftime("%Y:%m:%d")
        date_formatted_create = datetime.strptime(date_create , '%Y:%m:%d')
        res = super(bonus_return, self).create(cr, uid, vals, context=context)
        return res

bonus_return()

class pos_bonus_history(osv.osv):
    _name = "pos.bonus.history"
    _columns = {
        'name': fields.char('Bonus Serial', size=264),
        'used_amount': fields.float('Used Amount'),
        'used_date': fields.date('Used Date'),
        'bonus_return_id': fields.many2one('bonus.return', 'Bonus Coupon'),
        'pos_order': fields.char('POS Order')
    }
    
    _defaults = {
        'used_date': lambda *a: time.strftime('%Y-%m-%d')
    }
    
pos_bonus_history()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: