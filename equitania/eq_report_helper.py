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

class eq_report_helper(osv.osv):
    
    _name = "eq_report_helper"
            
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
        precision = 2
        string = ("%%5.%df" % precision)
        result = (string % object)        
        result = self.reformat_string(cr, uid, result, precision, language)
        #Currency Symbol is added
        if currency_id:
            result += (' %s' % currency_id.symbol)
        
        return result    
            
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
    