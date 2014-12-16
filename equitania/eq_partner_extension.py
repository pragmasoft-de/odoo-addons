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

#Adds the fields first name and birthday to the contact form and shows the first name in the search of that object.
#Adds the address type post box.

class eq_deliver_conditions(osv.osv):
    _name = 'eq.delivery.conditions'
    _rec_name = 'eq_name'
    
    _columns = {
                'eq_name': fields.char('Name', size=128)
                }

class eq_partner_sale_order_extension(osv.osv):
    _inherit = 'sale.order'
    _name = _inherit
    
    _columns = {
                'eq_deliver_condition_id': fields.many2one('eq.delivery.conditions', 'Delivery Condition'),
                'partner_id': fields.many2one('res.partner', 'Customer', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, select=True, track_visibility='always'),
                }
    
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        result = super(eq_partner_sale_order_extension, self).onchange_partner_id(cr, uid, ids, part, context=context)
        
        partner = self.pool.get('res.partner').browse(cr, uid, part, context)
        if partner:
            if partner.eq_incoterm:
                result['value']['incoterm'] = partner.eq_incoterm.id
            else:
                result['value']['incoterm'] = False
            if partner.eq_deliver_condition_id:
                result['value']['eq_deliver_condition_id'] = partner.eq_deliver_condition_id.id
            else:
                result['value']['eq_deliver_condition_id'] = False
        return result

class eq_partner_extension(osv.osv):
    _inherit = "res.partner"
    _name = "res.partner"
    
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            if record.parent_id and not record.is_company:
                name =  "%s, %s" % (record.parent_id.name, name)
                if record.type == 'contact':
                    name = "%s, %s %s %s" % (record.parent_id.name, (record.title.name if record.title else ''), (record.eq_firstname if record.eq_firstname else ''), record.name)
            if context.get('show_address_only'):
                name = self._display_address(cr, uid, record, without_company=True, context=context)
            if context.get('show_address'):
                name = name + "\n" + self._display_address(cr, uid, record, without_company=True, context=context)
            name = name.replace('\n\n','\n')
            name = name.replace('\n\n','\n')
            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            res.append((record.id, name))
        return res
    
    def _display_name_compute(self, cr, uid, ids, name, args, context=None):
        context = dict(context or {})
        context.pop('show_address', None)
        context.pop('show_address_only', None)
        context.pop('show_email', None)
        return dict(self.name_get(cr, uid, ids, context=context))
    
    _display_name = lambda self, *args, **kwargs: self._display_name_compute(*args, **kwargs)
    
    _display_name_store_triggers = {
        'res.partner': (lambda self,cr,uid,ids,context=None: self.search(cr, uid, [('id','child_of',ids)], context=dict(active_test=False)),
                        ['parent_id', 'is_company', 'name', 'eq_firstname', 'title'], 10)
    }
    
    _columns = {
        'eq_firstname': fields.char('Firstname', size=128),
        'eq_birthday': fields.date('Birthday'),
        'display_name': fields.function(_display_name, type='char', string='Name', store=_display_name_store_triggers, select=True),
        'title': fields.many2one('res.partner.title', 'Title'),
        'eq_custom01': fields.char(size=64),
        'type': fields.selection([('default', 'Default'), ('invoice', 'Invoice'),
                                   ('delivery', 'Shipping'), ('contact', 'Contact'),
                                   ('pobox', 'P.O. box'), ('other', 'Other')], 'Address Type',
            help="Used to select automatically the right address according to the context in sales and purchases documents."),
        'eq_incoterm': fields.many2one('stock.incoterms', 'Incoterm'),
        'eq_deliver_condition_id': fields.many2one('eq.delivery.conditions', 'Delivery Condition'),
        }
    
    _defaults = {
                'user_id': lambda self, cr, uid, context: uid if self.pool.get('ir.values').get_default(cr, uid, 'res.partner', 'default_creator_saleperson') else False,
                }
    
class eq_partner_extension_base_config_settings(osv.osv):
    _inherit = "base.config.settings"
    
    def set_default_creator(self, cr, uid, ids, context):
        ir_values_obj = self.pool.get('ir.values')
        config = self.browse(cr, uid, ids[0], context)
        
        ir_values_obj.set_default(cr, uid, 'res.partner', 'default_creator_saleperson', config.default_creator_saleperson or False)
        
    def get_default_creator(self, cr, uid, ids, context):
        ir_values_obj = self.pool.get('ir.values')
        creator = ir_values_obj.get_default(cr, uid, 'res.partner', 'default_creator_saleperson')
        return {
                'default_creator_saleperson': creator,
                }    
    
    _columns = {
                'default_creator_saleperson': fields.boolean('Use the creator of the Partner as the Saleperson [equitania]')
                }