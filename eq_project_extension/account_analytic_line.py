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

#Old API, Remove New API import if the Old API is used. Otherwise you'll get an import error.
from openerp import models, fields, api, _

class account_analytic_line(models.Model):
    _inherit = 'account.analytic.line'
     
    eq_tags = fields.Many2many('project.category', string='Tags', compute='copy_tags', readonly=False)
    
    def copy_tags(self):
        
        hr_object = self.env['hr.analytic.timesheet']
        project_work_object = self.env['project.task.work']
        project_task_object = self.env['project.task']
        
        for record in self:
            
            eq_id_layaway = hr_object.search([('line_id', '=', record.id)]).id
            
            eq_id_layaway = project_work_object.search([('hr_analytic_timesheet_id', '=', eq_id_layaway)]).task_id
            
            record.eq_tags = project_task_object.search([('id', '=', eq_id_layaway.id)]).categ_ids