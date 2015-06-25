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

class eq_hr_employee(osv.osv):
    _inherit = 'hr.employee'
    
    _columns = {
                'eq_work_fax': fields.char('Work Fax'),
                }
    
    def write(self, cr, uid, ids, values, context={}):
        if context == None:
            context = {}
            
        if type(ids) is not list: ids = [ids]
            
        if 'user_id' in values and 'do_not_repeat' not in context:
            user_obj = self.pool.get('res.users')
            if values['user_id']:
                if values['user_id'] != self.browse(cr, uid, ids).user_id.id:
                    #Removes the employee from all users, except the current one.
                    emp_ids_to_del = self.search(cr, SUPERUSER_ID, [('user_id', '=', values['user_id'])])
                    if len(emp_ids_to_del) != 0:
                        for emp_id in emp_ids_to_del:
                            self.write(cr, SUPERUSER_ID, emp_id, {'user_id': False}, context)
                    user_ids_to_del = user_obj.search(cr, SUPERUSER_ID, [('eq_employee_id', 'in', ids)])
                    if len(user_ids_to_del) != 0:
                        user_obj.write(cr, SUPERUSER_ID, user_ids_to_del, {'eq_employee_id': False}, context={'do_not_repeat': True})
                    #Sets the employee_id for the user.
                    for emp_id in ids:
                        user_obj.write(cr, SUPERUSER_ID, values['user_id'], {'eq_employee_id': emp_id}, context={'do_not_repeat': True})
            else:
                #Removes the employee from all the users.
                user_ids_to_del = user_obj.search(cr, SUPERUSER_ID, [('eq_employee_id', 'in', ids)])
                user_obj.write(cr, SUPERUSER_ID, user_ids_to_del, {'eq_employee_id': False}, context={'do_not_repeat': True})
                
        res = super(eq_hr_employee, self).write(cr, uid, ids, values, context)
            
        return res
    
    def create(self, cr, uid, values, context={}):
        if context == None:
            context = {}
            
        res = super(eq_hr_employee, self).create(cr, uid, values, context)
        if 'user_id' in values and 'do_not_repeat' not in context:
            if values['user_id']:
                user_obj = self.pool.get('res.users')
                
                emp_ids_to_del = self.search(cr, SUPERUSER_ID, [('user_id', '=', values['user_id'])])
                if len(emp_ids_to_del) != 0:
                    for emp_id in emp_ids_to_del:
                        if emp_id != res:
                            self.write(cr, SUPERUSER_ID, emp_id, {'user_id': False}, context)
                        
                user_obj.write(cr, uid, values['user_id'], {'eq_employee_id': res}, context={'do_not_repeat': True})
                        
        return res