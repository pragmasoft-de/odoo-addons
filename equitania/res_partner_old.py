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

class eq_partner_extension(osv.osv):
    _inherit = "res.partner"
    _name = "res.partner"
    
    
    """
    def name_get(self, cr, uid, ids, context=None):
        print "--------------- OLD - name_get -----------------"
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
    """
    
    
    def _display_name_compute(self, cr, uid, ids, name, args, context=None):
        print "--------------- OLD - _display_name_compute -----------------"
        
        context = dict(context or {})
        context.pop('show_address', None)
        context.pop('show_address_only', None)
        context.pop('show_email', None)
        return dict(self.name_get(cr, uid, ids, context=context))
    
    """ added the method from eq_report_extension.py """
    def _show_deb_cred_number(self, cr, uid, ids, name, arg, context={}):
        print "--------------- OLD - _show_deb_cred_number -----------------"
        
        result = {}
        for partner in self.browse(cr, uid, ids, context):
            deb_cred = False
            if partner.eq_customer_ref != 'False' and partner.eq_customer_ref and partner.eq_creditor_ref != 'False' and partner.eq_creditor_ref:
                deb_cred = partner.eq_customer_ref + ' / ' + partner.eq_creditor_ref
            elif partner.eq_customer_ref != 'False' and partner.eq_customer_ref:
                deb_cred = partner.eq_customer_ref
            elif partner.eq_creditor_ref != 'False' and partner.eq_creditor_ref:
                deb_cred = partner.eq_creditor_ref
            result[partner.id] = deb_cred
            
        return result
    
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
        'eq_default_delivery_address': fields.many2one('res.partner', 'Delivery Address'),
        'eq_default_invoice_address': fields.many2one('res.partner', 'Invoice Address'),
        'eq_citypart': fields.char('Disctirct'),
        'eq_house_no': fields.char('House number'),
        'eq_name2': fields.char('Name2'),
        'eq_letter_salutation': fields.char('Salutation'),
        'eq_creditor_ref': fields.char('Supplier Number', size=64), # added the field from eq_custom_ref.py
        'eq_customer_ref': fields.char('Customer Number', size=64), # added the field from eq_custom_ref.py
        'eq_deb_cred_number': fields.function(_show_deb_cred_number, type='char', store=False) # added the field from eq_report_extension.py
        }
    
    _defaults = {
                'user_id': lambda self, cr, uid, context: uid if self.pool.get('ir.values').get_default(cr, uid, 'res.partner', 'default_creator_saleperson') else False,
                }
    
    
    """ added the method from eq_custom_ref.py """
    def eq_creditor_update(self, cr, uid, ids, context=None):
        print "--------------- OLD - eq_creditor_update -----------------"
        
        #Gets the Partner
        partner = self.pool.get('res.partner').browse(cr, uid, ids, context=context)

        #If the field isn't filled, it should do this
        if not partner[0].eq_creditor_ref:
            #Gets the sequence and sets it in the apropriate field
            vals = {
                'eq_creditor_ref': self.pool.get('ir.sequence').get(cr, uid, 'eq_creditor_ref')
            }

            super(eq_custom_ref, self).write(cr, uid, ids, vals, context=context)

    """ added the method from eq_custom_ref.py """
    def eq_customer_update(self, cr, uid, ids, context=None):
        print "--------------- OLD - eq_customer_update -----------------"
        
        #Gets the Partner
        partner = self.pool.get('res.partner').browse(cr, uid, ids, context=context)

        #If the field isn't filled, it should do this
        if not partner[0].eq_customer_ref:
                #Gets the sequence and sets it in the apropriate field
                ref = self.pool.get('ir.sequence').get(cr, uid, 'eq_customer_ref')
                vals = {
                    'eq_customer_ref': ref,
                    'ref': ref,
                }

                super(eq_custom_ref, self).write(cr, uid, ids, vals, context=context)
    
    """ added the method from eq_custom_ref.py """
    def on_change_customer_ref(self, cr, uid, ids, eq_customer_ref, context=None):
        print "--------------- OLD - on_change_customer_ref -----------------"
        
        vals = {}
        vals['ref'] = eq_customer_ref
        return {'value': vals}
    
