## -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import time
from openerp.osv import osv
from openerp.report import report_sxw

class eq_report_sale_order_qe(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(eq_report_sale_order_qe, self).__init__(cr, uid, name, context=context)
        
        self.localcontext.update({
            'get_optional_positions':self.get_optional_positions,
        })
        
    
    def get_optional_positions(self, sale_line, option_lines):
        res = []
        for option_line in option_lines:
            if option_line.product_id.id == sale_line.product_id.id:
                vals = {
                        'default_code': option_line.product_id.default_code,
                        'name': option_line.product_id.name,
                        'quantity': option_line.quantity,
                        'price_unit': option_line.price_unit,
                        'price_subtotal': option_line.quantity * option_line.price_unit,
                        'uom_name': option_line.uom_id.name,
                        }
        return res

class report_eq_saleorder_quotation_enhancement(osv.AbstractModel):
    _inherit = 'report.sale.report_saleorder'
    _template = 'sale.report_saleorder'
    _wrapped_report_class = eq_report_sale_order_qe