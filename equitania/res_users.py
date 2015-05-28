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
from openerp import SUPERUSER_ID

class eq_res_users(osv.osv):
    _inherit = 'res.users'
    
    _columns = {
                'eq_employee_id': fields.many2one('hr.employee', 'Employee')
                }
    
    
    def write(self, cr, uid, ids, values, context=None):
        res = super(eq_res_users, self).write(cr, uid, ids, values, context={})
        
        if 'eq_employee_id' in values and 'do_not_repeat' not in context:
            if values['eq_employee_id']:
                if values['eq_employee_id'] != self.browse(cr, uid, ids).eq_employee_id.id:
                    emp_obj = self.pool.get('hr.employee')
                    user_ids_to_del = self.search(cr, SUPERUSER_ID, [('eq_employee_id', '=', values['eq_employee_id'])])
                    if len(user_ids_to_del) != 0:
                        for user_id in user_ids_to_del:
                            self.write(cr, SUPERUSER_ID, user_id, {'eq_employee_id': False}, context={'do_not_repeat': True})
                    emp_obj.write(cr, SUPERUSER_ID, values['eq_employee_id'], {'user_id': ids}, context={'do_not_repeat': True})
        
        return res
    
    def create(self,cr, uid, values, context=None):
        res = super(eq_res_users, self).create(cr, uid, values, context)
        
        if 'eq_employee_id' in values:
            if values['eq_employee_id']:
                emp_obj = self.pool.get('hr.employee')
                user_ids_to_del = self.search(cr, SUPERUSER_ID, [('eq_employee_id', '=', values['eq_employee_id'])])
                if len(user_ids_to_del) != 0:
                    for user_id in user_ids_to_del:
                        self.write(cr, SUPERUSER_ID, user_id, {'eq_employee_id': False}, context={})
                emp_obj.write(cr, SUPERUSER_ID, [values['eq_employee_id']], {'user_id': res}, context={})
        
        return res