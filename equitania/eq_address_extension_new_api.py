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

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        
        ir_values_obj = self.env['ir.values']
        
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = ['|','|',('name', operator, name),('eq_customer_ref', 'ilike', name),('eq_creditor_ref', 'ilike', name)] + args
        if ir_values_obj.get_default('sale.order', 'default_search_only_company'):
            if self.env.context.has_key('main_address'):
                args += [('is_company', '=', True)]
            elif self.env.context.has_key('default_type'):
                if self.env.context['default_type'] in ['delivery', 'invoice']:
                    args += [('type', '!=', 'contact')]
        categories = self.search(args, limit=limit)
        res = categories.name_get()
        
        if self.env.context is None:
            self.env.context = {}
        if self.env.context.has_key('active_model'):
            partner_ids = [r[0] for r in res]
            new_res = []
            
            show_address = ir_values_obj.get_default('sale.order', 'default_show_address')

            for partner_id in self.browse(partner_ids):
                #Company name
                company_name = partner_id.parent_id and partner_id.parent_id.name + ' ; ' or ''
                #Street City
                street = partner_id.street if partner_id.street else ''
                city = partner_id.city if partner_id.city else ''
                #customer/creditor number
                deb_num = ''
                if partner_id.eq_customer_ref and partner_id.eq_creditor_ref:
                    deb_num = '[' + partner_id.eq_customer_ref + '/' + partner_id.eq_creditor_ref + '] '
                elif partner_id.eq_customer_ref:
                    deb_num = '[' + partner_id.eq_customer_ref + '] '
                elif partner_id.eq_creditor_ref:
                    deb_num = '[' + partner_id.eq_creditor_ref + '] '
                if partner_id.is_company:
                    if show_address:
                        new_res.append((partner_id.id, deb_num + company_name + partner_id.name + ' / ' + _('Company') + ' // ' + street + ', ' + city))
                    else:
                        new_res.append((partner_id.id, deb_num + company_name + partner_id.name + ' / ' + _('Company')))
                else:
                    type = partner_id.type
                    if partner_id.type == 'contact':
                        type = _('contact')
                    elif partner_id.type == 'invoice':
                        type = _('invoice')
                    elif partner_id.type == 'delivery':
                        type = _('delivery')
                    elif partner_id.type == 'default':
                        type = _('default')
                    elif partner_id.type == 'other':
                        type = _('other')
                    if show_address:
                        new_res.append((partner_id.id, "%s %s %s %s" % ( deb_num + company_name, (partner_id.title.name if partner_id.title else ''), (partner_id.eq_firstname if partner_id.eq_firstname else ''), partner_id.name + ' / ' + type + ' // ' + street + ', ' + city)))
                    else:
                        new_res.append((partner_id.id, "%s %s %s %s" % ( deb_num + company_name, (partner_id.title.name if partner_id.title else ''), (partner_id.eq_firstname if partner_id.eq_firstname else ''), partner_id.name + ' / ' + type)))
            return new_res
        return res