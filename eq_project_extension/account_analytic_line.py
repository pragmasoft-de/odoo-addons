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
from datetime import datetime

class account_analytic_line(models.Model):
    _inherit = 'account.analytic.line'
     
    eq_tags_id = fields.Many2many('project.category', compute='_add_tags', readonly=False)
    #eq_project_classification_id = fields.Many2one(comodel_name='project.classification',search='_search_total', compute='_add_classification', readonly=False)
    eq_project_classification_id = fields.Many2one(comodel_name='project.classification',compute='_add_classification', readonly=False)
    eq_filter_by_day = fields.Char(compute='_get_day_from_date', readonly=False, store=True)
    
    eq_customer_number = fields.Char(compute='_get_customer_number', readonly=False)
    eq_company_id = fields.Many2one(comodel_name='res.partner',compute='_get_company', readonly=False)
    
    #def _search_total(self, operator, operand):
    
    def _get_company(self):
        hr_object = self.env['hr.analytic.timesheet']
        project_work_object = self.env['project.task.work']
        project_task_object = self.env['project.task']
        
        for record in self:
            analytic_timesheet = hr_object.search([('line_id', '=', record.id)])
            analytic_timesheet_id = analytic_timesheet.id    
            project_task_works = project_work_object.search([('hr_analytic_timesheet_id', '=', analytic_timesheet_id)])
            for project_task_work in project_task_works:
                project_task_work_id = project_task_work.task_id
                project_task = project_task_object.search([('id', '=', project_task_work_id.id)])
                project_rec = project_task.project_id
                partner_rec = project_rec.partner_id
                record.eq_company_id = partner_rec.id
    
    
    def _get_customer_number(self):
        hr_object = self.env['hr.analytic.timesheet']
        project_work_object = self.env['project.task.work']
        project_task_object = self.env['project.task']
        res_partner_object = self.env['res.partner']
        
        for record in self:
            analytic_timesheet = hr_object.search([('line_id', '=', record.id)])
            analytic_timesheet_id = analytic_timesheet.id    
            project_task_works = project_work_object.search([('hr_analytic_timesheet_id', '=', analytic_timesheet_id)])
            for project_task_work in project_task_works:
                project_task_work_id = project_task_work.task_id
                project_task = project_task_object.search([('id', '=', project_task_work_id.id)])
                project_rec = project_task.project_id
                partner_rec = project_rec.partner_id 
                record.eq_customer_number = partner_rec.eq_customer_ref
        
    #@api.depends('product_id.name')
    def _add_classification(self):
        hr_object = self.env['hr.analytic.timesheet']
        project_work_object = self.env['project.task.work']
        project_task_object = self.env['project.task']
        
        for record in self:
            analytic_timesheet = hr_object.search([('line_id', '=', record.id)])
            analytic_timesheet_id = analytic_timesheet.id    
            project_task_works = project_work_object.search([('hr_analytic_timesheet_id', '=', analytic_timesheet_id)])
            for project_task_work in project_task_works:
                project_task_work_id = project_task_work.task_id
                project_task = project_task_object.search([('id', '=', project_task_work_id.id)])
                project_rec = project_task.project_id
                classification_rec = project_rec.classification_id
                record.eq_project_classification_id = classification_rec.id
       
        
    def _add_tags(self):
        
        hr_object = self.env['hr.analytic.timesheet']
        project_work_object = self.env['project.task.work']
        project_task_object = self.env['project.task']
        
        for record in self:
               
            analytic_timesheet = hr_object.search([('line_id', '=', record.id)])
            analytic_timesheet_id = analytic_timesheet.id    
            project_task_works = project_work_object.search([('hr_analytic_timesheet_id', '=', analytic_timesheet_id)])
            for project_task_work in project_task_works:
                project_task_work_id = project_task_work.task_id
                project_task =  project_task_object.search([('id', '=', project_task_work_id.id)])
                record.eq_tags_id = project_task.categ_ids

    @api.depends('date')
    def _get_day_from_date(self):
        
        for record in self:
            
            month_day = datetime.strptime(record.date, '%Y-%m-%d')
            record.eq_filter_by_day = month_day.strftime('%d. %b')