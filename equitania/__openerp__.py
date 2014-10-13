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
    'name': 'Equitania Erweiterungsmodul',
    'version': '1.0.0',
    'description': """
        Equitania Software GmbH
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'purchase', 'sale',  'account', 'product', 'mail', 'report', 'hr', 'crm',],
    'category' : 'General Improvements',
    'summary': 'Sale, Account, Product, Mail, Report, CRM, Purchase',
    #'init': [
    #         'eq_install_func.xml', 
    #         ],
    'data': [
        'security/equitania_security.xml',
        'security/ir.model.access.csv',
        'eq_custom_ref_view.xml',
        'eq_address_extension_view.xml',
        'eq_pricelist_item_search_view.xml',
        'eq_modules_first_view.xml',
        'eq_company_custom_fields_view.xml',
        'eq_sale_order_seq_view.xml',
        'eq_install_func.xml',
        'eq_partner_extension_view.xml',
        'eq_report_extension_view.xml',
        'views/eq_footer.xml',
        'views/eq_header.xml',
        'views/eq_report_purchase_order.xml',
        'views/eq_report_purchase_quotation.xml',
        'views/eq_report_sale_order.xml',
        'views/eq_report_invoice.xml',
        'views/eq_report_style.xml',
        'views/eq_report_internal_layout.xml',
        'eq_lead_referred_view.xml',

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
