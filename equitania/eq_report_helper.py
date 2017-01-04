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

import time
import datetime


from openerp.osv import osv
from openerp.report import report_sxw

class eq_report_helper(osv.osv_memory):
    
    _name = "eq_report_helper"
    
    
    def get_user_infos(self, cr, uid, context = None):
        """
            Get user info (name + phone) of actual logged user on odoo
            @cr: cursor
            @uid: user id
            @context: context
            @return: user info (name + phone)
        """        
        sql = "select partner_id from res_users where id = " + str(uid)        
        cr.execute(sql)
        partner_id = cr.fetchone()[0]
                
        sql_2 = "select name, phone from res_partner where id = " + str(partner_id) 
        cr.execute(sql_2)
        record = cr.fetchone()
        result = record[0]
        if record[1]:
            result = record[0] + ", " + record[1]
        
        return result
    
    def get_user_signature(self, cr, uid, context = None):
        """
            Get user signature of actual logged user on odoo
            @cr: cursor
            @uid: user id
            @context: context
            @return: user signature
        """        
        sql = "select eq_signature from res_users where id = " + str(uid)        
        cr.execute(sql)
        result = cr.fetchone()[0]
        return result
            
    def get_qty(self, cr, uid, object, language, param_name, context = None):
        """
            Quantity formater
        """
        #precision = self.pool.get('decimal.precision').precision_get( self.cr, self.uid, 'Purchase Quantity Report')        
        precision = self.pool.get('decimal.precision').precision_get( cr, uid, param_name)
        string = ("%%5.%df" % precision)                
        result = (string % object)
             
        # parse string and generate correct number format
        result = self.reformat_string(cr, uid, result, precision, language) 
           
        return result
    
    def get_price(self, cr, uid, object, language, param_name, currency_id=False, context = None):
        """
            Price formater
        """        
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, param_name)
        string = ("%%5.%df" % precision)
        result = (string % object)        
        
        # parse string and generate correct number format
        result = self.reformat_string(cr, uid, result, precision, language)
        #Currency Symbol is added
        if currency_id:
            result += (' %s' % currency_id.symbol)
        
        return result
    
    def get_standard_price(self, cr, uid, object, language, currency_id=False, context =None):
        """
            Price formater - formats given number to default price format 1.000,00
        """
        
        precision = 2
        string = ("%%5.%df" % precision)
        result = (string % object)        
        result = self.reformat_string(cr, uid, result, precision, language)
        #Currency Symbol is added
        if currency_id:
            result += (' %s' % currency_id.symbol)
        
        return result    

    def get_gross_price_invoice(self, cr, uid, object, language, currency_id=False, context =None):
        """
            Calculate gross price a return result as string together with currency back
            @cr: cursor
            @uid: user id
            @object: order line object
            @currency_id: Currency
            @context: Context
            @return: Calculated gross price
        """
        
        gross_price = object.price_unit *  object.quantity
        return self.get_standard_price(cr, uid, gross_price, language, currency_id)

    
    def get_gross_price(self, cr, uid, object, language, currency_id=False, context =None):
        """
            Calculate gross price a return result as string together with currency back
            @cr: cursor
            @uid: user id
            @object: order line object
            @currency_id: Currency
            @context: Context
            @return: Calculated gross price
        """
        
        gross_price = object.price_unit *  object.product_uom_qty
        return self.get_standard_price(cr, uid, gross_price, language, currency_id)
       
    def get_gross_price_as_float_invoice(self, cr, uid, object, language, currency_id=False, context =None):
        """
            Calculate gross price a return result as float
            @cr: cursor
            @uid: user id
            @object: order line object
            @currency_id: Currency
            @context: Context
            @return: Calculated gross price
        """
        
        return object.price_unit *  object.quantity
    
    def get_gross_price_as_float(self, cr, uid, object, language, currency_id=False, context =None):
        """
            Calculate gross price a return result as float
            @cr: cursor
            @uid: user id
            @object: order line object
            @currency_id: Currency
            @context: Context
            @return: Calculated gross price
        """
        
        return object.price_unit *  object.product_uom_qty
            
    def check_if_display_gross_price(self, cr, uid, order, context=None):        
        """
            Check if we should display prices a gross pricess
            @cr: Cursor
            @uid: User id
            @orde: Actual order
            @context: Context
            @return: True (show gross price) if tax is (19% Umsatzsteuer or 7% Umsatzsteuer) and price_include = true
        """
                
        tax_obj = self.pool.get('account.tax')
        sale_order_line_obj = self.pool.get('sale.order.line')
        sale_line_ids = sale_order_line_obj.search(cr, uid, [('order_id', '=', order.id),], context=context)
        for line_id in sale_line_ids:
            sale_order_line = sale_order_line_obj.browse(cr, uid, line_id, context=context)
            tax_id = sale_order_line.tax_id.id
            if tax_id:
                tax = tax_obj.browse(cr, uid, tax_id, context=context)
                
                if ("19% Umsatzsteuer" in tax.name or "7% Umsatzsteuer" in tax.name) and tax.price_include is True:
                    return True
        
        return False    
    
    def _convert_string_to_date(self, date_as_string):
        """
            Convert date in string format like '2016-02-09' into date
            @date_as_string: date in string format
            @return: string converted into date
            
        """        
        return datetime.datetime.strptime(date_as_string, '%Y-%m-%d')
        
    def _get_date_format_for_language(self, cr, uid, lang_code, context =None):
        """
            Get date format for actual language
            @cr: cursor
            @uid: user id
            @lang_code: actual language code
            @context: context
            @return: Date forma for actual language
        """        
        lang_obj = self.pool.get('res.lang')
        lang_ids = lang_obj.search(cr, uid, [('code', '=', lang_code),], context=context)
        for lang_id in lang_ids:
            language = lang_obj.browse(cr, uid, lang_id, context=context)
            return language.date_format
                    
    def get_eq_payment_terms(self, cr, uid, object, language, currency_id=False, context =None):
        """
            Show payment terms with custom text using 2 kinds of placeholders.
            Date1 & Date2 = Placeholder for Date that will be calculated and replaced
            Value1 % Value2 = Placehold for Value that will be calculated and replaced
            @cr: cursor
            @uid: user id
            @object: account.invoice object
            @language: actual language
            @currency_id: actual currency_id of given invoice
            @context: context
            @return: Return new string with formated & calculated date and prices            
        """
        payment_term_result = object.payment_term.note      # hold our result and return it back as final result
                
        # get details of selected paycondition
        payment_term_line_obj = self.pool.get('account.payment.term.line')
        payment_term_line_ids = payment_term_line_obj.search(cr, uid, [('payment_id', '=', object.payment_term.id),], context=context)
        
        d1_set = False      # helper flag - true => date1 was set
        d2_set = False      # helper flag - true => date1 was set
        v1_set = False      # helper flag - true => value1 was set
        d1_set = False      # helper flag - true => value2 was set
        ignore_invoice_date = True
        
        # convert string to date 
        if object.date_invoice:
            invoice_date_object = self._convert_string_to_date(object.date_invoice)
            ignore_invoice_date = False
            
        # let's get all payment termn lines for actual payment term, calculate date & value and replace result in our final text
        for line_id in payment_term_line_ids:
            line = payment_term_line_obj.browse(cr, uid, line_id, context=context)
            
            if ignore_invoice_date is False:        # recalculate and set date only if an invoice date is provided                    
                recalculated_date = invoice_date_object + datetime.timedelta(days = line.days)
                date_format = self._get_date_format_for_language(cr, uid, language, context=context)
            
                # calculate date and replace it
                if d1_set is False:
                    if payment_term_result:
                        payment_term_result = payment_term_result.replace("[Date1]", recalculated_date.strftime(date_format))                                                            
                        d1_set = True
                else:
                    if payment_term_result:
                        payment_term_result = payment_term_result.replace("[Date2]", recalculated_date.strftime(date_format))
                        d2_set = True
        
        
            # calculate price and replace it    
            if line.value_amount > 0:
                total_value = object.amount_total * line.value_amount
            else:
                total_value = object.amount_total
            
            # reformat price
            total_value = self.get_standard_price(cr, uid, total_value, language, currency_id)
            
            # and now set price...make sure that you set price for each placeholder                    
            if v1_set is False: 
                if payment_term_result:
                    payment_term_result = payment_term_result.replace("[Value1]", total_value)
                    v1_set = True
            else:
                if payment_term_result:
                    payment_term_result = payment_term_result.replace("[Value2]", total_value)
                    v2_set = True
        
        return payment_term_result
    
    
    
    
    
    def reformat_string(self, cr, uid, data, precision, language, context =None):    
        """
            Creates formated number with count of decimal positions from odd and puts hardcoded thousand separator on right place.
            We can chane both tags for decimal separator and thousand separator in our variables
            @data: number as string formated from odoo
            @precision: count of decimal positions from odoo
        """
        
        res_lang_obj = self.pool.get("res.lang")
        language_id = res_lang_obj.search(cr, uid, [("code", "=", language)])        
        langauge_record =  res_lang_obj.browse(cr, uid, language_id[0])
        
        #print langauge_record
        
        
        DECIMAL_SEPARATOR_TAG = langauge_record.decimal_point
        THOUSAND_SEPARATOR_TAG = langauge_record.thousands_sep
                
        #DECIMAL_SEPARATOR_TAG = ","
        #THOUSAND_SEPARATOR_TAG = "."
        
        # replace . with ,   
        data = data.replace(".", DECIMAL_SEPARATOR_TAG)
        
        # delete all white spaces
        data = data.replace(" ", "")
        
        #finalResult = data
        tempData = ""
        decimal_part = ""
        
        # extract decimal part in case, that we have one in our string
        if precision > 0:
            startIndex = data.find(DECIMAL_SEPARATOR_TAG);
            endIndex = len(data)
                        
            # get decimal part...example 1256,85 -> decimal_part = ,85
            decimal_part = data[startIndex:endIndex]
                        
            tempdata = data[0:startIndex]
            data = tempdata

        
        # iterate our numbre from end to start and set THOUSAND_SEPARATOR_TAG on right place         
        index = len(data)
        counter = 0
        finalResult = ""
        while index > 0:
            if counter == 3:
                finalResult += THOUSAND_SEPARATOR_TAG
                counter = 0
                
            finalResult += data[index - 1]
            index = index -1
            counter = counter + 1
        
        # we're done here, let's reverse our string to get back to normal number
        finalResult = finalResult[::-1]
        
        # append decimal_part if we have one
        if len(decimal_part) > 0:
            finalResult += decimal_part
          
        return finalResult          
    