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
{
    'name': 'EQ POS customization',
    'version': '1.0.36',
    'category': 'Point of Sale',
    'description': """
This module is used to return the products to the customer from POS Interface, Gift coupon voucher.
""",
    'author': "Acespritech Solutions Pvt. Ltd.",
    'website': "www.acespritech.com",
    'depends': ['web', 'point_of_sale', 'base'],
    'data': [
             'security/ir.model.access.csv',
             'views/eq_pos.xml',
             'views/eq_report_sessionsummary.xml',          
             'pos_order/point_of_sale_view.xml',
             'res_partner_view.xml',
             'coupon/pos_coupon_view.xml',
             'coupon/pos_coupon_security.xml',
             'coupon/account_journal.xml',
             'bonus_return/bonus_return_view.xml'     
             ],
    'demo': [],
    'test': [],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: