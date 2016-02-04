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

class eq_res_users(models.Model):
    _inherit = 'res.users'

    
    def _get_group(self):
        """
            Get link to groups
            @return: Returns array with group ids to be linked with an user
        """
        result = super(eq_res_users, self)._get_group()
        try:
            group_id = self.env['ir.model.data'].get_object_reference('equitania', 'purchase_in_products')
            result.append(group_id)
        except ValueError:            
            pass            # If these groups does not exists anymore
        
        return result
        
        
    eq_employee_id = fields.Many2one('hr.employee', 'Employee', copy=False)
    eq_custom01 = fields.Char(size=64) # field added from eq_company_custom_fields.py                
    groups_id = fields.Many2many('res.groups', 'res_groups_users_rel', 'uid', 'gid', 'Groups', default=_get_group)

    
    
    @api.model    
    def create(self, vals):
        """
            Extension of default create method
            @vals: values to be set
            @return: new created res.user
        """

        # default call - create new user and save automaticaly created new partner_id            
        new_user =  super(eq_res_users, self).create(vals)
                
        # STEP 1 - main save function that gets executed if user has selected employee
        if 'eq_employee_id' in vals and 'do_not_repeat' not in self._context:
            if vals['eq_employee_id']:
                emp_obj = self.env['hr.employee']
                
                # Removes the user from all employees, except the selected one. It's possible to link only 1 user with 1 employee
                user_ids_to_del = self.search([('eq_employee_id', '=', vals['eq_employee_id'])])
                if len(user_ids_to_del) != 0:
                    for user_id in user_ids_to_del:                        
                        if user_id != new_user:
                            user_id.eq_employee_id = False
                
                # Sets the user_id in the employee. do_not_repeat in context so that the employee does not set the employee_id for the user.                
                employee = emp_obj.search([('id', '=', vals['eq_employee_id'])])                
                employee.with_context(do_not_repeat = True).write({'user_id': new_user.id})
                
        
        # STEP 2 - check if we can find at least one record in res_partner with same email as user provided
        if new_user.login : #fixed the issue for users
            partner = self.env['res.partner'].search([('email', '=',new_user.login), ('customer', '=', True)])
            if len(partner) > 1:
                existing_partner_id = partner[0].id         # it's a tuple
            else:
                existing_partner_id = partner.id            # it's a single record
                
                                                                    
            new_generated_partner_id = new_user.partner_id.id   # save id of new & automaticaly generated partner_id
            
            # yes, we have an existing partner, so there's no need to use new created one. just use existing partner and delete new one
            if existing_partner_id is not False:
                if existing_partner_id != new_generated_partner_id:     # ok, it's call from backend ILLINGEN - deleted new generated record"                            
                    new_user.partner_id = existing_partner_id                                                        
                    wrong_partner = self.env['res.partner'].search([('id', '=', new_generated_partner_id)])     # get new + automaticaly generated partner and delete him - we don't need him
                    wrong_partner.unlink() 
        
        return new_user
    
    @api.multi
    def write(self, vals):
        """
            Extension of default write method
            @vals: values to be set
            @return: true = record updated
        """
             
        if 'eq_employee_id' in vals and 'do_not_repeat' not in self._context:
            emp_obj = self.env['hr.employee']
            if vals['eq_employee_id']:                            
                if vals['eq_employee_id'] != self.browse(self._ids).eq_employee_id.id:
                    # Removes the user from all employees, except the selected one
                    user_ids_to_del = self.search([('eq_employee_id', '=', vals['eq_employee_id'])])                    
                    if len(user_ids_to_del) != 0:
                        for user_id in user_ids_to_del:
                            if user_id != self._ids:
                                user_id.eq_employee_id = False
                    
                    
                    emp_ids_to_del = emp_obj.search([('user_id', 'in', self._ids)])
                    if len(emp_ids_to_del) != 0:
                        for employee_id in emp_ids_to_del:                            
                            employee = emp_obj.search([('id', '=', employee_id.id)])                
                            employee.with_context(do_not_repeat = True).write({'user_id': False})                                                                                    
                    
                    #Sets the user_id in the employee
                    for user_id in self._ids:
                        employee = emp_obj.search([('id', '=', vals['eq_employee_id'])])
                        employee.with_context(do_not_repeat = True).write({'user_id': user_id})
            else:   
                # Removes the user from all employees - user deleted link to an employee
                emp_ids_to_del = emp_obj.search([('user_id', 'in', self._ids)])
                for employee_id in emp_ids_to_del:                                            
                    employee = emp_obj.search([('id', '=', employee_id.id)])                
                    employee.with_context(do_not_repeat = True).write({'user_id': False})
                        
        res = super(eq_res_users, self).write(vals)
        return res