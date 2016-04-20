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

class project_project(models.Model):
    _inherit = 'project.project'
    
    eq_can_set_to_done = fields.Boolean(compute='_check_tasks_done', readonly=False)
    
    def _check_tasks_done(self):
        
        project_task_object = self.env['project.task']
        
        for record in self:
        
            tasks_done = project_task_object.search([('project_id', '=', record.id)])
            
            if ((tasks_done.filtered(lambda t: t.stage_id.id == 7 or t.stage_id.id == 8)) == (tasks_done.filtered(lambda t: t.id == t.id))):
                
                record.eq_can_set_to_done = True
                
            else:
                
                record.eq_can_set_to_done = False