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

from openerp.osv import fields, osv
import polib
from openerp.modules.module import get_module_path

#This is for methods that will be executed at startup.
#Used to initiate the paper format of the reports.

class eq_install_func(osv.osv):
    _name = "eq_install_func"
    
    def _set_paper_format(self, cr, uid, ids=None, context=None):
        """
        eu_a4_reports = self.pool.get('ir.actions.report.xml').search(cr, uid, ['|', '|', '|',('report_name', '=', 'purchase.report_purchaseorder'), ('report_name', '=', 'purchase.report_purchasequotation'), ('report_name', '=', 'account.report_invoice'), ('report_name', '=', 'sale.report_saleorder')])
        
        for report in eu_a4_reports:
            val = {'paperformat_id': 1,}
            self.pool.get('ir.actions.report.xml ').write(cr, uid, ids, val)
        """
        eu_a4 = {
                 'page_width': 0,
                 'orientation': 'Portrait', 
                 'header_line': False, 
                 'default': True, 
                 'format': 'A4', 
                 'header_spacing': 35, 
                 'margin_right': 17, 
                 'margin_top': 40, 
                 'margin_left': 17, 
                 'margin_bottom': 23, 
                 'page_height': 0, 
                 'display_name': 'European A4', 
                 'report_ids': [], 
                 'dpi': 90, 
                 'name': 'European A4'}
        eu_a4_id = self.pool.get('report.paperformat').write(cr, uid, 1, eu_a4)
        
        if self.pool.get('report.paperformat').search(cr, uid, [('name', '=', 'European A4 Intern')]) == []:           
            eu_a4_intern = {
                     'page_width': 0,
                     'orientation': 'Portrait', 
                     'header_line': False, 
                     'default': True, 
                     'format': 'A4', 
                     'header_spacing': 10, 
                     'margin_right': 17, 
                     'margin_top': 15, 
                     'margin_left': 17, 
                     'margin_bottom': 23, 
                     'page_height': 0, 
                     'display_name': 'European A4 Intern', 
                     'report_ids': [], 
                     'dpi': 90, 
                     'name': 'European A4 Intern'}
            
            eu_a4_intern_id = self.pool.get('report.paperformat').create(cr, uid, eu_a4_intern)
        
        return True
    
    def _create_report_price_precision(self, cr, uid, ids=None, context=None):
        dp = self.pool.get('decimal.precision')
        product_price_id = dp.search(cr, uid, [('name', '=', 'Product Price')])
        product_price = dp.browse(cr, uid, product_price_id[0])
        
        search_price_sale = dp.search(cr, uid, [('name', '=', 'Report Product Price Sales')])
        
        if len(search_price_sale) == 0:
            values_sale = {
                           'name': 'Report Product Price Sales',
                           'digits': product_price.digits,
                           
                           }
            
            dp.create(cr, uid, values_sale)
        
        search_price_purchase = dp.search(cr, uid, [('name', '=', 'Report Product Price Purchase')])
        
        if len(search_price_purchase) == 0:
            values_purchase = {
                           'name': 'Report Product Price Purchase',
                           'digits': product_price.digits,
                           
                           }
            
            dp.create(cr, uid, values_purchase)
        
        return True
    
    def _load_translation(self, cr, uid, ids=None, context=None):
        addon_folder = get_module_path('equitania')

        po = polib.pofile(addon_folder + '/i18n/de.po')
        valid_entries = [e for e in po if not e.obsolete]
        ir_translation_obj = self.pool.get('ir.translation')
        ir_ui_view_obj = self.pool.get('ir.ui.view')
        ir_translation_obj.clear_caches()
        for entry in valid_entries:
            for occurence in entry.occurrences:
                occurence_split = occurence[0].split(':')
                #Views
                if occurence_split[0] == 'view':
                    #website reports
                    if occurence_split[1] == 'website':
                        report_id = occurence_split[2].split('.')[-1]
                        view_id = ir_ui_view_obj.search(cr, uid, [('name', '=', report_id)])[0]
                        translation_id = ir_translation_obj.search(cr, uid, [('src', '=', entry.msgid), ('res_id', '=', view_id), ('name', '=', occurence_split[1])])
                        if len(translation_id) != 0:
                            vals = {
                                    'value': entry.msgstr,
                                    'state': 'translated',
                                    }
                            ir_translation_obj.write(cr, uid, translation_id[0], vals)
                        else:
                            vals = {
                                    'lang': 'de_DE',
                                    'src': entry.msgid,
                                    'name': 'website',
                                    'res_id': view_id,
                                    'module': occurence_split[2].split('.')[0],
                                    'state': 'translated',
                                    'values': entry.msgstr,
                                    'type': occurence_split[0],
                                    }
                            ir_translation_obj.create(cr, uid, vals)
        return True