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
from openerp.osv import osv


class eq_company_custom_fields(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    eq_custom_1 = fields.Char('Chief labeling', size=50, help="The content of this field may be used in the header or footer of reports.")
    eq_custom_2 = fields.Char('1st person', size=50, help="The content of this field may be used in the header or footer of reports.")
    eq_custom_3 = fields.Char('2nd person', size=50, help="The content of this field may be used in the header or footer of reports.")
    eq_custom_4 = fields.Char('3rd person', size=50, help="The content of this field may be used in the header or footer of reports.")
    eq_report_logo = fields.Binary('Company Report Logo')
    eq_company_ean = fields.Char('Company EAN13', size=7)
    eq_citypart = fields.Char('Disctirct')
    eq_house_no = fields.Char('House number')
    
