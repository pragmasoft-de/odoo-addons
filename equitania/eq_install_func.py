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