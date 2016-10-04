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

from openerp.osv import fields, osv
from openerp.tools.translate import _
import re

class crm_lead2opportunity_partner(osv.osv_memory):
    _inherit = 'crm.lead2opportunity.partner'
    
    def action_apply(self, cr, uid, ids, context=None):
        """
        Convert lead to opportunity or merge lead and opportunity and open
        the freshly created opportunity view.
        """
        if context is None:
            context = {}
        
        ir_translation_pool = self.pool.get('ir.translation')
        



        lead_obj = self.pool['crm.lead']
        partner_obj = self.pool['res.partner']

        w = self.browse(cr, uid, ids, context=context)[0]
        opp_ids = [o.id for o in w.opportunity_ids]
        function = w.partner_id.function
        
        ir_translation_title_ids = ir_translation_pool.search(cr,uid,[('name','=','res.partner.title,name'),('res_id','=',w.partner_id.title.id)])       
         
        ir_translation_title_obj = ir_translation_pool.browse(cr,uid,ir_translation_title_ids)
        
        if function == False or function == None:
            function = ''
        else:
            function = function.encode(encoding='UTF-8',errors='strict')
        vals = {
            'section_id': w.section_id.id,
            'firstname':w.partner_id.eq_firstname or " ",
            'lastname':w.partner_id.name or " ",
            'function': function or " ",
            'mobil':w.partner_id.mobile or " ",
            'fax':w.partner_id.fax or " ",
            'street': w.partner_id.street or " ",
            'eq_house_no': w.partner_id.eq_house_no or " ",
            'birthdate': w.partner_id.eq_birthday,
            'title': ir_translation_title_obj.res_id or "",
        }
        if w.partner_id:
            vals['partner_id'] = w.partner_id.id
        if w.name == 'merge':
            lead_id = lead_obj.merge_opportunity(cr, uid, opp_ids, context=context)
            lead_ids = [lead_id]
            lead = lead_obj.read(cr, uid, lead_id, ['type', 'user_id'], context=context)
            if lead['type'] == "lead":
                context = dict(context, active_ids=lead_ids)
                vals.update({'lead_ids': lead_ids, 'user_ids': [w.user_id.id]})
                self._convert_opportunity(cr, uid, ids, vals, context=context)
            elif not context.get('no_force_assignation') or not lead['user_id']:
                vals.update({'user_id': w.user_id.id})
                lead_obj.write(cr, uid, lead_id, vals, context=context)
        else:
            lead_ids = context.get('active_ids', [])
            vals.update({'lead_ids': lead_ids, 'user_ids': [w.user_id.id]})
            self._convert_opportunity(cr, uid, ids, vals, context=context)
            for lead in lead_obj.browse(cr, uid, lead_ids, context=context):
                if lead.partner_id and lead.partner_id.user_id != lead.user_id:
                    partner_obj.write(cr, uid, [lead.partner_id.id], {'user_id': lead.user_id.id}, context=context)

        return self.pool.get('crm.lead').redirect_opportunity_view(cr, uid, lead_ids[0], context=context)