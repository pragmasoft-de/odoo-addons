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

class sale_order(osv.osv):
    _inherit = 'sale.order'

    _columns = {
        'eq_pricelist_change': fields.boolean('Pricelist Default')
        }

sale_order()

class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _columns = {}

    #Extends the standard name_search method, which is used by the many2one field. Adds a backslash plus the address type
    #at the end of the name.
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        res = super(res_partner, self).name_search(cr, uid, name, args, operator, context, limit)
        if context is None:
            context = {}
        if context.has_key('active_model'):
            partner_ids = [r[0] for r in res]
            new_res = []

            for partner_id in self.browse(cr, uid, partner_ids):
                company_name = partner_id.parent_id and partner_id.parent_id.name + ' ; ' or ''
                if partner_id.is_company:
                    new_res.append((partner_id.id, company_name + partner_id.name + ' / ' + 'Company'))
                else:
                    new_res.append((partner_id.id, "%s, %s %s %s" % ( company_name, (partner_id.title.name if partner_id.title else ''), (partner_id.eq_firstname if partner_id.eq_firstname else ''), partner_id.name + ' / ' + str(partner_id.type))))
            return new_res
        return res

res_partner()
