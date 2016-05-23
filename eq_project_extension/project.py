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
from openerp.osv import fields, osv
from openerp.exceptions import except_orm, Warning, RedirectWarning


class task(osv.osv):
    _inherit = "project.task"
    
    def _read_group_stage_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        stage_obj = self.pool.get('project.task.type')
        order = stage_obj._order
        access_rights_uid = access_rights_uid or uid
        if read_group_order == 'stage_id desc':
            order = '%s desc' % order
        search_domain = []
        project_id = self._resolve_project_id_from_context(cr, uid, context=context)
        if project_id:
            search_domain += [('project_ids', '=', project_id)]
        stage_ids = stage_obj._search(cr, uid, search_domain, order=order, access_rights_uid=access_rights_uid, context=context)
        result = stage_obj.name_get(cr, access_rights_uid, stage_ids, context=context)
        # restore order of the search
        result.sort(lambda x,y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))

        fold = {}
        for stage in stage_obj.browse(cr, access_rights_uid, stage_ids, context=context):
            fold[stage.id] = stage.fold or False
        return result, fold
    
    def _read_group_user_id(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        res_users = self.pool.get('res.users')
        project_id = self._resolve_project_id_from_context(cr, uid, context=context)
        access_rights_uid = access_rights_uid or uid
        if project_id:
            ids += self.pool.get('project.project').read(cr, access_rights_uid, project_id, ['members'], context=context)['members']
            order = res_users._order
            # lame way to allow reverting search, should just work in the trivial case
            if read_group_order == 'user_id desc':
                order = '%s desc' % order
            # de-duplicate and apply search order
            ids = res_users._search(cr, uid, [('id','in',ids)], order=order, access_rights_uid=access_rights_uid, context=context)
        result = res_users.name_get(cr, access_rights_uid, ids, context=context)
        # restore order of the search
        result.sort(lambda x,y: cmp(ids.index(x[0]), ids.index(y[0])))
        return result, {}
    
    _group_by_full = {
        'stage_id': _read_group_stage_ids,
        'user_id': _read_group_user_id,
    }
    
    
    def create(self, cr, uid, vals, context=None):
        project_id = vals.get('project_id')
        project = self.pool.get('project.project').browse(cr, uid, project_id, context)
        project_state = project.state
        context = dict(context or {})
        if project_state != 'close' and project_state != 'cancelled':
            # for default stage
            if vals.get('project_id') and not context.get('default_project_id'):
                context['default_project_id'] = vals.get('project_id')
            # user_id change: update date_start
            if vals.get('user_id') and not vals.get('date_start'):
                vals['date_start'] = fields.datetime.now()
            
            # context: no_log, because subtype already handle this
            create_context = dict(context, mail_create_nolog=True)
            task_id = super(task, self).create(cr, uid, vals, context=create_context)
            self._store_history(cr, uid, [task_id], context=context)
            return task_id
        else:
            raise osv.except_osv(_('Error'), _('The project is already closed or cancelled.'))


    def write(self, cr, uid, ids, vals, context=None):
        tasks = self.browse(cr, uid, ids, context)
        if 'message_last_post' not in vals:
            for rec in tasks:
                task_status = rec.stage_id.name
                project_state = rec.project_id.state

                if project_state != 'close' and project_state != 'cancelled':
                    if task_status != 'Abgebrochen' and task_status != 'Erledigt' or 'stage_id' in vals:
                        if isinstance(ids, (int, long)):
                            ids = [ids]
                          
                        # stage change: update date_last_stage_update
                        if 'stage_id' in vals:
                            vals['date_last_stage_update'] = fields.datetime.now()
                        # user_id change: update date_start
                        if vals.get('user_id') and 'date_start' not in vals:
                            vals['date_start'] = fields.datetime.now()
                  
                        # Overridden to reset the kanban_state to normal whenever
                        # the stage (stage_id) of the task changes.
                        if vals and not 'kanban_state' in vals and 'stage_id' in vals:
                            new_stage = vals.get('stage_id')
                            vals_reset_kstate = dict(vals, kanban_state='normal')
                            for t in self.browse(cr, uid, ids, context=context):
                                write_vals = vals_reset_kstate if t.stage_id.id != new_stage else vals
                                super(task, self).write(cr, uid, [t.id], write_vals, context=context)
                            result = True
                        else:
                            result = super(task, self).write(cr, uid, ids, vals, context=context)
                  
                        if any(item in vals for item in ['stage_id', 'remaining_hours', 'user_id', 'kanban_state']):
                            self._store_history(cr, uid, ids, context=context)
                        return result
                    else:
                        raise Warning(_('The task is already done or cancelled.'))
                else:
                    raise Warning(_('The project is already done or cancelled.'))
        else: 
            super(task, self).write(cr, uid, ids, vals, context=context)
               