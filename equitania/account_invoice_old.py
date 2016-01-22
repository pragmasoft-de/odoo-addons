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


class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    
    def _compute_street_house_no(self, cr, uid, ids, field_name, arg, context):
        """ Generate street and house no info for purchase order """
        
        res = {}
        
        for person in self.browse(cr, uid, ids):
            if person.partner_id.street and person.partner_id.eq_house_no:                
                    res[person.id] = person.partner_id.street + ' ' + person.partner_id.eq_house_no
            elif person.partner_id.street:                                
                    res[person.id] = person.partner_id.street
            else:
                res[person.id] = False
                     
        return res
    
    
    def _compute_zip_city(self, cr, uid, ids, field_name, arg, context):
        """ Generate zip and city info for purchase order """
                
        res = {}
        for person in self.browse(cr, uid, ids):
            if person.partner_id.zip and person.partner_id.city:                
                    res[person.id] = person.partner_id.zip + ' ' + person.partner_id.city
            elif person.partner_id.zip:                                
                    res[person.id] = person.partner_id.zip
            elif person.partner_id.city:                                
                    res[person.id] = person.partner_id.city
            else:
                res[person.id] = False
                
        return res
    
    def _compute_country(self, cr, uid, ids, field_name, arg, context):
       """ Generate country info for purchase order """
       res = {}
       for person in self.browse(cr, uid, ids, context):
            if person.partner_id.country_id:
                    res[person.id] = person.partner_id.country_id.name           
            else:
                res[person.id] = False
                
       return res
    
    _columns = {
                'eq_street_house_no': fields.function(_compute_street_house_no, string=" ", store=False, type="char"),
                'eq_zip_city': fields.function(_compute_zip_city, string=" ", store=False, type="char"),
                'eq_country': fields.function(_compute_country, string=" ", store=False, type="char"),
                'eq_contact_person_id': fields.many2one('hr.employee', 'Contact Person', size=100),
                'eq_head_text': fields.html('Head Text'),
                'eq_ref_number': fields.char('Sale Order Referenc', size=64),
                'eq_delivery_address': fields.many2one('res.partner', 'Delivery Address'),
                'comment': fields.html('Additional Information'),
                }
    
    _defaults = {
                'eq_contact_person_id': lambda obj, cr, uid, context: obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])[0] if len(obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])) >= 1 else obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)]) or False 
                }

account_invoice()


class eq_report_extension_invoice(osv.osv):
    """
     Small extension of standard functionality.
     - added new field eq_pos_no as a container for sequence no from contract (AB). we'll use this information as pos on delivery note and invoice 
    """
    
    _inherit = "account.invoice.line"
    
    _order = "sequence"
    
    _columns = {
                'eq_delivery_date': fields.date('Delivery Date'),
                'eq_move_id': fields.many2one('stock.move'),
                'eq_pos_no' : fields.integer('Seq')
                }
    
    def create(self, cr, user, vals, context={}):    
        """
            let's get original sequence no from deliverynote and save it for every position on delivery note
            @cr: cursor
            @use: actual user
            @vals: alle values to be saved
            @context: context
        """
        if vals.get('eq_move_id'):
            move_id = vals["eq_move_id"] 
            
            # get corresponding sequence no for our positions
            result_id = self.pool.get('stock.move').browse(cr, user, move_id, context)    
            
            # save sequence into our new field    
            vals["eq_pos_no"] = result_id.eq_pos_no

        # use standard save functionality and save it
        return super(eq_report_extension_invoice, self).create(cr, user, vals, context)