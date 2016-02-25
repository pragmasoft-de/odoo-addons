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

# functionality for our eq_report_invoice report
class stock_picking(report_sxw.rml_parse):
    
    price = 0    
    data_dict = {}
    display_gross_price = False
    
    
    def __init__(self, cr, uid, name, context):
        
        self.price = 0
        self.data_dict = {}
        self.display_gross_price = False
        
        super(stock_picking, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_pickings':self.get_pickings,
            'get_qty':self.get_qty,
            'get_price': self.get_price,
            'get_standard_price': self.get_standard_price,
            'append_price': self.append_price,
            'calculate': self.calculate,
            'get_gross_price': self.get_gross_price,
            'get_gross_price_as_float': self.get_gross_price_as_float,
            'get_gross_price_invoice': self.get_gross_price_invoice,
            'get_gross_price_as_float_invoice': self.get_gross_price_as_float_invoice,
            'check_if_display_gross_price': self.check_if_display_gross_price,
            'calculate_sum': self.calculate_sum,
            'get_eq_payment_terms': self.get_eq_payment_terms,
        })
        
    def get_pickings(self, object):
        result = []
        for l in object:
            if l.eq_move_id:
                if l.eq_move_id.picking_id not in result:
                    result.append(l.eq_move_id.picking_id)
        return result
    
    def get_qty(self, qty, language):
        return self.pool.get("eq_report_helper").get_qty(self.cr, self.uid, qty, language, 'Sale Quantity Report')
               
    def get_price(self, price, language, currency_id):                
        return self.pool.get("eq_report_helper").get_price(self.cr, self.uid, price, language, 'Sale Price Report', currency_id)
        
    def get_standard_price(self, price, language, currency_id):
        return self.pool.get("eq_report_helper").get_standard_price(self.cr, self.uid, price, language, currency_id)
    
    def check_if_display_gross_price(self, object):
        """
            Check if we should display gross price
            @object: order position
            @return: True = display gross price
        """
        return self.pool.get("eq_report_helper").check_if_display_gross_price(self.cr, self.uid, object)
    
    def get_gross_price(self, object, language, currency_id):
        """
            Get gross price for given order position together with currency
            @object: Order position
            @language: Actual language
            @currency_id: Currency id
            @return: Gross price as string together with currency 
        """
        return self.pool.get("eq_report_helper").get_gross_price(self.cr, self.uid, object, language, currency_id)
    
    def get_gross_price_invoice(self, object, language, currency_id):
        """
            Get gross price for an invoice position as string together with currency
            @object: Invoice position
            @language: Language
            @currency_id: Currency
            @return: Gross  price of an invoice position as string together with currency
        """
        return self.pool.get("eq_report_helper").get_gross_price_invoice(self.cr, self.uid, object, language, currency_id)
    
    def get_gross_price_as_float(self, object, language, currency_id):
        """
            Get gross price for an order position as string together with currency
            @object: Invoice position
            @language: Language
            @currency_id: Currency
            @return: Gross  price of an order position as float
        """
        return self.pool.get("eq_report_helper").get_gross_price_as_float(self.cr, self.uid, object, language, currency_id)        
    
    def get_gross_price_as_float_invoice(self, object, language, currency_id):
        """
            Get gross price for an invoice position as string together with currency
            @object: Invoice position
            @language: Language
            @currency_id: Currency
            @return: Gross  price of an invoice position as float
        """
        return self.pool.get("eq_report_helper").get_gross_price_as_float_invoice(self.cr, self.uid, object, language, currency_id)
    
    """
    def check_if_display_gross_price(self, object):
        self.display_gross_price =  self.pool.get("eq_report_helper").check_if_display_gross_price(self.cr, self.uid, object)
        return self.display_gross_price    
    """
     
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

    def get_eq_payment_terms(self, object, language, currency_id):
        """
            Show payment terms with custom text using 2 kinds of placeholders.
            Date1 & Date2 = Placeholder for Date that will be calculated and replaced
            Value1 % Value2 = Placehold for Value that will be calculated and replaced            
            @object: account.invoice object
            @language: actual language
            @currency_id: actual currency_id of given invoice
            @return: Return new string with formated & calculated date and prices            
        """
        
        return self.pool.get("eq_report_helper").get_eq_payment_terms(self.cr, self.uid, object, language, currency_id)
    
        
class report_invoice(osv.AbstractModel):
    _name = 'report.account.report_invoice'
    _inherit = 'report.abstract_report'
    _template = 'account.report_invoice'
    _wrapped_report_class = stock_picking

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: