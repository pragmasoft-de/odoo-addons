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

class eq_report_sale_order(report_sxw.rml_parse):
    
    price = 0    
    data_dict = {}
    display_gross_price = False 
    
    def __init__(self, cr, uid, name, context):
        
        self.price = 0
        self.data_dict = {}
        self.display_gross_price = False
        
        super(eq_report_sale_order, self).__init__(cr, uid, name, context=context)
        
        self.localcontext.update({
            'get_qty':self.get_qty,
            'get_price': self.get_price,
            'get_standard_price': self.get_standard_price,
            'append_price': self.append_price,
            'calculate': self.calculate,
            'get_gross_price': self.get_gross_price,
            'get_gross_price_as_float': self.get_gross_price_as_float,
            'check_if_display_gross_price': self.check_if_display_gross_price,
            'calculate_sum': self.calculate_sum,
        })
        
    
    def get_qty(self, object, language):
        return self.pool.get("eq_report_helper").get_qty(self.cr, self.uid, object, language, 'Sale Quantity Report')
               
    def get_price(self, object, language, currency_id):                
        return self.pool.get("eq_report_helper").get_price(self.cr, self.uid, object, language, 'Sale Price Report', currency_id)
        
    def get_standard_price(self, object, language, currency_id):
        return self.pool.get("eq_report_helper").get_standard_price(self.cr, self.uid, object, language, currency_id)
    
    def check_if_display_gross_price(self, object):
        """
            Check if we should display gross price
            @object: order position
            @return: True = display gross price
        """
        return self.pool.get("eq_report_helper").check_if_display_gross_price(self.cr, self.uid, object)
    
    """
    def check_if_display_gross_price(self, object):
        self.display_gross_price =  self.pool.get("eq_report_helper").check_if_display_gross_price(self.cr, self.uid, object)
        return self.display_gross_price
    """
    
    def get_gross_price(self, object, language, currency_id):
        """
            Get gross price for given order position together with currency
            @object: Order position
            @language: Actual language
            @currency_id: Currency id
            @return: Gross price as string together with currency 
        """
        return self.pool.get("eq_report_helper").get_gross_price(self.cr, self.uid, object, language, currency_id)
    
    def get_gross_price_as_float(self, object, language, currency_id):
        """
            Get gross price for given order position as float
            @object:
            @language:
            @currency_id:
            @return: Gross price as float
        """
        return self.pool.get("eq_report_helper").get_gross_price_as_float(self.cr, self.uid, object, language, currency_id)
    
        
        
    def append_price(self, input_price, category_no):
        """
            Append price for category and save it
            @input_price: Price to be saved
            @category_no: Category no
            @return: None - it's a void. We'll save all data in member variable
        """            
        if category_no in self.data_dict:
            value = self.data_dict[category_no]
            value += input_price
            self.data_dict[category_no] = value
        else:
            self.data_dict[category_no] = input_price
        
        return None
    
    def calculate_sum(self, input, category_no, lines):
        """
            Calculate sum - just a simple total price
            @input: input
            @category_no: category
            @lines: order lines
        """
        result = 0
        
        for line in lines:
            if line.eq_optional is False:
                quantity = line.product_uom_qty
                price = line.price_unit
                result += quantity * price  

        return result
        
    def calculate(self, input, category_no):
        """
            Calculate total price without optional products
            @input: Subtotal price - total inkl. optional products
            @category_no: Category no
            @return: Total price without optional products
        """     
                   
        if category_no in self.data_dict:               # check if we find total price for category
            if self.display_gross_price is False:
                total_price = self.data_dict[category_no]
                result = input - total_price
                return result
            else:
                total_price = self.data_dict[category_no]            
                result = input - total_price
                return result
        
        return input
        
    
class report_lunchorder(osv.AbstractModel):
    _name = 'report.sale.report_saleorder'
    _inherit = 'report.abstract_report'
    _template = 'sale.report_saleorder'
    _wrapped_report_class = eq_report_sale_order