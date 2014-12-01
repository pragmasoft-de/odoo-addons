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
        
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = ['|',('name', operator, name),('eq_customer_ref', 'ilike', name)]
        categories = self.search(args, limit=limit)
        res = categories.name_get()
        
        if self.env.context is None:
            self.env.context = {}
        if self.env.context.has_key('active_model'):
            partner_ids = [r[0] for r in res]
            new_res = []
            
            show_address = self.env['ir.values'].get_default('sale.order', 'default_show_address')

            for partner_id in self.browse(partner_ids):
                company_name = partner_id.parent_id and partner_id.parent_id.name + ' ; ' or ''
                street = partner_id.street if partner_id.street else ''
                city = partner_id.city if partner_id.city else ''
                deb_num = ('[' + str(partner_id.eq_customer_ref) + '] ') if partner_id.eq_customer_ref else ''
                if partner_id.is_company:
                    new_res.append((partner_id.id, deb_num + company_name + partner_id.name + ' / ' + _('Company') + ' // ' + street + ', ' + city))
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