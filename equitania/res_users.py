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

    def _get_group(self,cr, uid, context=None):
        dataobj = self.pool.get('ir.model.data')
        result = super(eq_res_users, self)._get_group(cr, uid, context=context)
        try:
            dummy,group_purchase_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'equitania', 'purchase_in_products')
            dummy,group_supplier_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'equitania', 'supplier_in_account')
            dummy,group_access_reporting_menu_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'equitania', 'group_access_reporting')
            dummy,group_access_employee_menu_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'equitania', 'group_access_hr_menu')
            result.append(group_purchase_id)
            result.append(group_supplier_id)
            
            result.append(group_access_reporting_menu_id)
            result.append(group_access_employee_menu_id)
        except ValueError:
            # If these groups does not exists anymore
            pass
        return result
    
    _columns = {
                'eq_employee_id': fields.many2one('hr.employee', 'Employee', copy=False),
                'eq_signature' : fields.binary('Signature'),
                }

    _defaults = {
        'groups_id': _get_group,
    }
    
    def write(self, cr, uid, ids, values, context={}):
        if context == None:
            context = {}
            
        if type(ids) is not list: ids = [ids]
        
        if 'eq_employee_id' in values and 'do_not_repeat' not in context:
            emp_obj = self.pool.get('hr.employee')
            if values['eq_employee_id']:
                if values['eq_employee_id'] != self.browse(cr, uid, ids).eq_employee_id.id:
                    #Removes the user from all employees, except the selected one
                    user_ids_to_del = self.search(cr, SUPERUSER_ID, [('eq_employee_id', '=', values['eq_employee_id'])])
                    print 'User user_ids_to_del', user_ids_to_del
                    if len(user_ids_to_del) != 0:
                        for user_id in user_ids_to_del:
                            if user_id != ids:
                                self.write(cr, SUPERUSER_ID, user_id, {'eq_employee_id': False})
                    emp_ids_to_del = emp_obj.search(cr, uid, [('user_id', 'in', ids)])
                    if len(emp_ids_to_del) != 0:
                        emp_obj.write(cr, SUPERUSER_ID, emp_ids_to_del, {'user_id': False}, context={'do_not_repeat': True})
                    #Sets the user_id in the employee
                    for user_id in ids:
                        emp_obj.write(cr, SUPERUSER_ID, values['eq_employee_id'], {'user_id': user_id}, context={'do_not_repeat': True})
            else:
                #Removes the user from all employees
                emp_ids_to_del = emp_obj.search(cr, SUPERUSER_ID, [('user_id', 'in', ids)], context=context)
                emp_obj.write(cr, SUPERUSER_ID, emp_ids_to_del, {'user_id': False}, context={'do_not_repeat': True})
                
        res = super(eq_res_users, self).write(cr, uid, ids, values, context={})
        
        return res
    
    def create(self,cr, uid, values, context={}):        
        if context == None:
            context = {}
            
        res = super(eq_res_users, self).create(cr, uid, values, context=context)
        
        if 'eq_employee_id' in values and 'do_not_repeat' not in context:
            if values['eq_employee_id']:
                emp_obj = self.pool.get('hr.employee')
                #Removes the user from all employees, except the selected one.
                user_ids_to_del = self.search(cr, SUPERUSER_ID, [('eq_employee_id', '=', values['eq_employee_id'])])
                if len(user_ids_to_del) != 0:
                    for user_id in user_ids_to_del:
                        if user_id != res:
                            self.write(cr, SUPERUSER_ID, user_id, {'eq_employee_id': False}, context=context)
                #Sets the user_id in the employee. do_not_repeat in context so that the employee does not set the employee_id for the user.
                emp_obj.write(cr, uid, values['eq_employee_id'], {'user_id': res}, context={'do_not_repeat': True})
        return res