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
from openerp import SUPERUSER_ID

class eq_hr_employee(models.Model):
    _inherit = 'hr.employee'


    eq_work_fax = fields.Char('Work Fax')


    @api.model
    def create(self, vals):
        """
            Extension of default create method
            @vals: values to be set
            @return: new created hr.employee
        """

        res = super(eq_hr_employee, self).create(vals)
        if 'user_id' in vals and 'do_not_repeat' not in self._context:
            if vals['user_id']:
                user_obj = self.env['res.users']
                emp_ids_to_del = self.search([('user_id', '=', vals['user_id'])])               #Removes the employee from all users, except the current one.
                if len(emp_ids_to_del) != 0:
                    for emp_id in emp_ids_to_del:
                        if emp_id != res:
                            emp_id.user_id = False

                user = user_obj.search([('id', '=', vals['user_id'])])
                check = user.with_context(do_not_repeat = True).write({'eq_employee_id': res.id})

        return res

    @api.multi
    def write(self, vals):
        """
            Extension of default write method
            @vals: values to be set
            @return: true = record updated
        """

        if 'user_id' in vals and 'do_not_repeat' not in self._context:
            user_obj = self.env['res.users']
            if vals['user_id']:
                if vals['user_id'] != self.search([('user_id', '=', vals['user_id'])]):
                    emp_ids_to_del = self.search([('user_id', '=', vals['user_id'])])           #Removes the employee from all users, except the current one.
                    if len(emp_ids_to_del) != 0:
                        for emp_id in emp_ids_to_del:
                            emp_id.user_id = False

                    user_ids_to_del = user_obj.search([('eq_employee_id', 'in', self._ids)])
                    if len(user_ids_to_del) != 0:
                        for user_id in user_ids_to_del:
                            user = user_obj.search([('id', '=', user_id.id)])
                            user.with_context(do_not_repeat = True).write({'eq_employee_id': False})


                    #Sets the employee_id for the user.
                    for emp_id in self._ids:
                        user = user_obj.search([('id', '=', vals['user_id'])])
                        user.with_context(do_not_repeat = True).write({'eq_employee_id': emp_id})

            else:
                # Employee has deleted his link to user to NULL, so delete all links
                user_ids_to_del = user_obj.search([('eq_employee_id', 'in', self._ids)])        #Removes the employee from all the users.
                if len(user_ids_to_del) != 0:
                    for user_id in user_ids_to_del:
                        user = user_obj.search([('id', '=', user_id.id)])
                        user.with_context(do_not_repeat = True).write({'eq_employee_id': False})

        res = super(eq_hr_employee, self).write(vals)
        return res