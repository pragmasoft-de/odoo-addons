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

import logging
from openerp.osv import osv, fields
from openerp.report import report_sxw


class eq_product_sales_report(report_sxw.rml_parse):
    """
        Report class for qweb report product_sales_report that was originaly created as pentaho report
    """
    
    _name = 'equitania.eq_product_sales_report'
    
    date_from   = ""
    date_to     = ""
    parent_ID   = 0
    
    
    def __init__(self, cr, uid, name, context):
        """
            Default init function - register all helper methods here to be able to call them from report (xml)
            @cr: cursor
            @uid: user id
            @name: name
            @context: context
        """
                            
        super(eq_product_sales_report, self).__init__(cr, uid, name, context=context)
        
        # save variables from wizard
        self.date_from = context['DateFrom']
        self.date_to = context['DateTo']
        self.parent_ID = context['ParentID']
     
        # register helpers
        self.localcontext.update({
            'get_date_from': self._get_date_from,
            'get_date_to': self._get_date_to,       
            'get_records': self._get_records,
            'format_number': self._format_number,
        })
    
    
    def _format_number(self, number, digits_count):
        """
            Small ui helper - formates number to our standard with give digits
            @number: number to be formated
            @digits_count: maximal digits count
            @return: formated number
        """
        prefix = "{0:.Xf}"
        prefix = prefix.replace('X', str(digits_count))        
        result = prefix.format(number)
        result = result.replace(".", ",")
        return result
    
    
    def _get_records(self):
        """
            Get all records created by wizard and show them as lines in table
            @return: An array with all created records from eq_product_sales_data table
        """
                
        result = []
        table = self.pool.get('eq.product.sales.data')        
        ids = table.search(self.cr, self.uid, [('parent_id','=', self.parent_ID)])
        for id in ids:
             result.append(table.browse(self.cr, self.uid, id))
        
        return result
                    
    def _get_date_from(self):
        """
            Get DateFrom from wizard
            @return: DateFrom
        """        
        return self.date_from
    
    def _get_date_to(self):
        """
            Get DateTo from wizard
            @return: DateTo
        """        
        return self.date_to
        
        
class report_lunchorder(osv.AbstractModel):
    _name = 'report.equitania.eq_product_sales_report'
    _inherit = 'report.abstract_report'
    _template = 'equitania.eq_product_sales_report'
    _wrapped_report_class = eq_product_sales_report