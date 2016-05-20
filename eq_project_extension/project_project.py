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
from openerp.exceptions import except_orm, Warning, RedirectWarning

class project_project(models.Model):
    _inherit = 'project.project'
    
    eq_can_set_to_done = fields.Boolean(compute='_check_tasks_done', readonly=False)
    
    def _check_tasks_done(self):
        
        project_task_object = self.env['project.task']
        
        for record in self:
        
            tasks_done = project_task_object.search([('project_id', '=', record.id)])
            
            if ((tasks_done.filtered(lambda t: t.stage_id.id == 23 or t.stage_id.id == 8)) == (tasks_done.filtered(lambda t: t.id == t.id))):
                
                record.eq_can_set_to_done = True
                
            else:
                
                record.eq_can_set_to_done = False
    
#     def create(self, cr, uid, vals, context=None):
#         if context is None:
#             context = {}
#         # Prevent double project creation when 'use_tasks' is checked + alias management
#         create_context = dict(context, project_creation_in_progress=True,
#                               alias_model_name=vals.get('alias_model', 'project.task'),
#                               alias_parent_model_name=self._name)
#  
#         if vals.get('type', False) not in ('template', 'contract'):
#             vals['type'] = 'contract'
#  
#         project_id = super(project_project, self).create(cr, uid, vals, context=create_context)
#         project_rec = self.browse(cr, uid, project_id, context=context)
#         self.pool.get('mail.alias').write(cr, uid, [project_rec.alias_id.id], {'alias_parent_thread_id': project_id, 'alias_defaults': {'project_id': project_id}}, context)
#         return project_id
#      
#      
    def write(self, cr, uid, ids, vals, context=None):
        project_state = vals.get('state')
        if project_state != 'open':
            raise Warning(_('Edit cancelled. \nThe project is already closed or cancelled.'))
        else:
            print"project_state", project_state
            # if alias_model has been changed, update alias_model_id accordingly
            if vals.get('alias_model'):
                model_ids = self.pool.get('ir.model').search(cr, uid, [('model', '=', vals.get('alias_model', 'project.task'))])
                vals.update(alias_model_id=model_ids[0])
            return super(project_project, self).write(cr, uid, ids, vals, context=context)
            
