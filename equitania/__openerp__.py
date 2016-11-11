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
    'license': 'AGPL-3',
    'version': '1.1.112',
    'description': """
        Equitania Software GmbH
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': [
                'base_setup', 'purchase', 'sale',  'account', 'stock_account', 'product',
                'mail', 'report', 'hr', 'crm', 'stock','sale_stock', 'delivery',
                'website','website_quote', 'website_report', 'account_cancel' ],
    'category' : 'General Improvements',
    'summary': 'Sale, Account, Product, Mail, Report, CRM, Purchase',
    #'init': [
    #         'eq_install_func.xml',
    #         ],
    'data': [
        'security/equitania_security.xml',
        'security/ir.model.access.csv',
        'security/menuitems_managed_admin.xml',
        'security/ir_ui_menu.xml',
        'wizard/eq_multy_assign_product_no_view.xml',
        'account_invoice_view.xml',
        'eq_reports_view.xml',
        'eq_custom_ref_view.xml',
        'eq_address_extension_view.xml',
        'eq_pricelist_item_search_view.xml',
        'eq_modules_first_view.xml',
        'eq_company_custom_fields_view.xml',
        'eq_sale_order_seq_view.xml',
        'eq_partner_extension_view.xml',
        'eq_report_extension_view.xml',
        'eq_lead_referred_view.xml',
        'eq_open_sale_order_line_view.xml',
        'sale_view.xml',
        'hr_view.xml',
        'views/eq_footer.xml',
        'views/eq_header.xml',
        'views/eq_report_purchase_order.xml',
        'views/eq_report_purchase_quotation.xml',
        'views/eq_report_sale_order.xml',
        'views/eq_report_invoice.xml',
        'views/eq_report_style.xml',
        'views/eq_report_internal_layout.xml',
        'views/eq_report_stockpicking.xml',
        'views/eq_report_stockpicking_return.xml',
        'views/eq_report_open_sale_order_line.xml',
        'views/eq_product_analysis_wiz_view.xml',        
        'views/eq_product_sales_wiz_view.xml',
        'eq_install_func.xml',
        'eq_install_func_no_update.xml',
        'data/sale_layout_category_data.xml',
        'sale_layout/views/sale_layout_category_view.xml',
        'sale_layout/views/sale_layout_template.xml',
        'data/decimal_precision.xml',
        'res_config_view.xml',
        'res_users_view.xml',
        'res_partner_view.xml',
        'stock_view.xml',
        'product_view.xml',
        'purchase_view.xml',
        'wizard/eq_date_done_change_view.xml',
        'wizard/stock_transfer_details_view.xml',
        'wizard/eq_partner_wiz.xml',
        'views/eq_purchase_view.xml',
        'views/eq_css.xml',
        #'views/eq_portal_sale_data.xml',
        'views/eq_sale_order_action_data.xml',
        'views/eq_website_quotation_data.xml',
        'eq_foreign_ref_view.xml',
        'account_payment_term.xml',
        'sale_config.xml',
        'crm_view.xml',
        'eq_address_search_view.xml',
        'pricelist_view.xml',
        'reports/eq_product_sales_report.xml',
        'reports/eq_product_analysis_report.xml',
        'eq_email_template_view.xml',
        'res_country_view.xml',
    ],
    'demo': [],
    'css': ['static/src/css/eq_style.css'],
    'installable': True,
    'auto_install': False,
}
