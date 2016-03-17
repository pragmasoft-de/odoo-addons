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
from openerp import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.osv import osv

model = 'eq.product.analysis.data'
report_name = 'equitania.equitania_rep_product_analysis_qweb2'


class eq_product_analysis_report_wiz(models.TransientModel):
    _name = 'equitania.product.analysis.report.wiz'
    
    date_start = fields.Date('Start of period')
    date_end = fields.Date('End of period')
    eq_supplier_id = fields.Many2one('res.partner', string='Supplier', domain = "[('supplier','=',True)]")
    product_category_id = fields.Many2one('product.category', string='Product category')
    
    output_type = fields.Selection(selection = [('pdf', 'Portable Document (pdf)'),('xls', 'Excel Spreadsheet (xls)'),('csv', 'Comma Separated Values (csv)'),\
                                                  ('rtf', 'Rich Text (rtf)'), ('html', 'HyperText (html)'), ('txt', 'Plain Text (txt)')], required=True)
    
    
    def remove_menu_ir_value(self, cr, uid, ids=None, context=None):
        #Eintrag in ir_values entfernen (erzeugt durch report_data) um doppelten Menueintrag zu vermeiden
        values_obj = self.pool.get('ir.values')
        find_menu_entry = values_obj.search(cr,uid, [('name', '=', 'EQ Product Analysis Report'), ('model', '=', model)])
        if (find_menu_entry):            
            values_obj.unlink(cr, uid, find_menu_entry, context=context)
            
        return True
    
    def _get_output_type(self, cr, uid, context=None):
        
        return "pdf"
        """
        if context is None:
            context = {}
        reports_obj = self.pool.get('ir.actions.report.xml')
        domain = [('report_name','=',report_name)]
        report_id = reports_obj.search(cr, uid, domain, limit=1)
        res = reports_obj.browse(cr, uid, report_id, context=context)[0].pentaho_report_output_type
        return res
        """
    
    _defaults = {
        'date_start': lambda *a: datetime.now().strftime('%Y-%m-01'),
        'date_end': lambda *a: (datetime.now()  + relativedelta(months=1)).strftime('%Y-%m-01'),
        'output_type': _get_output_type,
    }
    
    
    def _convert_string_to_date(self, dateText):
        dt = None
        try:
            dt = datetime.strptime(dateText, '%Y-%m-%d %H:%M:%S')
        except:
            try:
                dt = datetime.strptime(dateText, '%Y-%m-%d')
            except:
                pass
        return dt
    
    
    
    def _process_invoice_data(self, account_invoice_data, get_full_data, supplier_id = 0, prod_cat_id = 0):
        """
        Group invoice data for product
        """
        prod_analysis_data = {}
        for invoice in account_invoice_data:
            invoice_lines = invoice['invoice_line']
            
            for invoice_line in invoice_lines:
                cur_product = invoice_line['product_id']
                product_id  = cur_product.id
                
                if (not cur_product or (not product_id) or (product_id == 0)):
                    continue
                
                
                if ((prod_cat_id > 0) and (cur_product.categ_id.id <> prod_cat_id)):
                    continue
                
                record_data = {}
                if product_id in prod_analysis_data:
                    record_data = prod_analysis_data[product_id]
                else:
                    if (get_full_data):
                        record_data = {
                                       'product_id': product_id,
                                       'ean' : cur_product.ean13,
                                       'article_desc': cur_product.name,
                                       'article_number' : cur_product.default_code or '-',
                                       'supplier':'',
                                       'sale_price': cur_product.list_price,
                                       'purchase_price':cur_product.standard_price,
                                       'gross_margin':0,
                                       }
                        
                        profit = cur_product.list_price-cur_product.standard_price
                        record_data['gross_profit']= profit
                        if (cur_product.list_price <> 0):
                            record_data['gross_margin'] = float(profit*100 / cur_product.list_price) 
                        
                        if (cur_product.seller_id):
                            seller_id_val = cur_product.seller_id.id
                            if ((supplier_id > 0) and (supplier_id <> seller_id_val)):
                                continue
                            record_data['supplier'] = cur_product.seller_id.name
                        elif supplier_id > 0:
                            continue
                
                prod_analysis_data[product_id] = record_data
        return prod_analysis_data
    
    
    def check_report(self, cr, uid, ids, context=None):

        form_data = self.read(cr, uid, ids)[0]#date_start, date_end
        wizard = self.browse(cr, uid, ids[0], context=context)
        
        if context is None:
            context = {}
        data = {}
        
        date_from = form_data['date_start']
        date_to= form_data['date_end']
        
        filter_supplier_id = 0
        filter_category_id = 0
        filter_supplier= form_data['eq_supplier_id']
        filter_category= form_data['product_category_id']
        if (filter_supplier and len(filter_supplier) > 0):
            filter_supplier_id = filter_supplier[0]
        if (filter_category and len(filter_category) > 0):
            filter_category_id = filter_category[0]
        
        
        filter_date = []
        data['variables'] = {}
        if (date_from or date_to):
            filter_date = []
            if (date_from):
                filter_date.append(('create_date', '>=', date_from))
                
                date_to_conv = self._convert_string_to_date(date_from)
                date_to_text_conv = date_to_conv.strftime('%d.%m.%Y')
                data['variables']['DateFrom'] = date_to_text_conv
            if (date_to):
                date_to_conv = self._convert_string_to_date(date_to)
                date_to_text_conv = (date_to_conv + relativedelta(days=1)).strftime('%Y-%m-%d')
                
                filter_date.append(('create_date', '<', date_to_text_conv))
                 
                date_for_report = date_to_conv.strftime('%d.%m.%Y')
                data['variables']['DateTo'] = date_for_report
        
        
        account_invoice_ids = []
        obj_account_invoice= self.pool.get('account.invoice')
        obj_account_invoice_line = self.pool.get('account.invoice.line')
        obj_prod_analysis_data= self.pool.get('eq.product.analysis.data')
        obj_prod_analysis_data_master= self.pool.get('eq.product.analysis.data.master')
        
        account_invoice_ids  = obj_account_invoice.search(cr, uid, filter_date)
        account_invoices = []    
        if (len(account_invoice_ids) > 0):
            account_invoices = obj_account_invoice.browse(cr, uid, account_invoice_ids, context=context)
        else:
            raise osv.except_osv(_('No Data!'),
                            _('There is no data for current filters.'))
            
        
        prod_analysis_data = self._process_invoice_data(account_invoices, True, filter_supplier_id, filter_category_id)
        
        if (len(prod_analysis_data) == 0):
            raise osv.except_osv(_('No Data!'), _('There is no data for current filters.'))
        
        data_parent_id = obj_prod_analysis_data_master.create(cr, uid, {}, context=context)
        data['variables']['Parent_ID'] = data_parent_id
        
        if (len(prod_analysis_data) > 0):
            for key, record in prod_analysis_data.items():
                record_data={
                    'parent_id' : data_parent_id,
                    'article_number' : record['article_number'],
                    'ean': record['ean'],
                    'article_desc': record['article_desc'],
                    'supplier' :  record['supplier'],
                    'gross_profit' : record['gross_profit'],
                    'gross_margin' : record['gross_margin']
                }
                
                obj_prod_analysis_data.create(cr, uid, record_data, context=context)
        
        data['model'] = model
        data['output_type'] = 'pdf' # wizard.output_type
        return self._print_report(cr, uid, ids, data, context=context)
    
          
    def _print_report(self, cr, uid, ids, mydata, context=None):
        """
            Print_report - Button click handle
            Prepares all data and executes report
            @cr: cursor
            @uid: user id
            @ids: ids
            @mydata: data created by Oli's function
            @context: context
            @return: call of report action
        """
        
        context['DateFrom'] = mydata['variables']['DateFrom']
        context['DateTo'] = mydata['variables']['DateTo']
        context['ParentID'] = mydata['variables']['Parent_ID']
        
        datas = {
             'ids': [],
             'model': 'eq.product.analysis.data',
             #'form': data
             'form': mydata
            } 
        return self.pool['report'].get_action(cr, uid, [], "equitania.eq_product_analysis_report", data=datas, context=context)
    
    """
    def _print_report(self, cr, uid, ids, data, context=None):

        if context is None:
            context = {}

        return {
            'type': 'ir.actions.report.xml',
            'report_name': report_name,
            'datas': data,
           
        }
    """