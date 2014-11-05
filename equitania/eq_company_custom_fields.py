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

#Adds custom fields to the objects res.company, product.category, product.pricelist.version and res.users.
#The custom fields of res.company can be used in the header and footer of the reports and is shown in the form. 
#The rest is for dataimport and won't be shown.

class eq_company_custom_fields(osv.osv):
    _name = 'res.company'
    _inherit = 'res.company'

    _columns = {
        'eq_custom_1': fields.char('Custom 1', size=50, help="The content of this field may be used in the header or footer of reports."),
        'eq_custom_2': fields.char('Custom 2', size=50, help="The content of this field may be used in the header or footer of reports."),
        'eq_custom_3': fields.char('Custom 3', size=50, help="The content of this field may be used in the header or footer of reports."),
        'eq_custom_4': fields.char('Custom 4', size=50, help="The content of this field may be used in the header or footer of reports."),
        'eq_report_logo': fields.binary('Company Report Logo')
    }
    
class eq_product_category_custom_fields(osv.osv):
    _inherit = 'product.category'
    
    _columns = {
                'eq_custom01': fields.char(size=64)
                }
class eq_pricelist_version_custom_fields(osv.osv):
    _inherit = 'product.pricelist.version'
    
    _columns = {
                'eq_custom01': fields.char(size=64)
                }
class eq_res_users_custom_fields(osv.osv):
    _inherit = 'res.users'
    
    _columns = {
                'eq_custom01': fields.char(size=64)
                }