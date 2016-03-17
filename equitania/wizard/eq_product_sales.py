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


model = 'eq.product.sales.data'
report_name = 'equitania.equitania_rep_product_analysis_qweb'


class eq_product_sales_report_wiz(models.TransientModel):
    _name = 'equitania.product.sales.report.wiz'
    
    date_start = fields.Date('Start of period')
    date_end = fields.Date('End of period')
    eq_supplier_id = fields.Many2one('res.partner', string='Supplier', domain = "[('supplier','=',True)]")
    product_category_id = fields.Many2one('product.category', string='Product category')
    
    output_type = fields.Selection(selection = [('pdf', 'Portable Document (pdf)'),('xls', 'Excel Spreadsheet (xls)'),('csv', 'Comma Separated Values (csv)'),\
                                                  ('rtf', 'Rich Text (rtf)'), ('html', 'HyperText (html)'), ('txt', 'Plain Text (txt)')], required=True)
    
    
        
    def remove_menu_ir_value(self, cr, uid, ids=None, context=None):
        #Eintrag in ir_values entfernen (erzeugt durch report_data) um doppelten Menueintrag zu vermeiden
        values_obj = self.pool.get('ir.values')
        find_menu_entry = values_obj.search(cr,uid, [('name', '=', 'EQ Product Sales Report'), ('model', '=', model)])
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
        res = reports_obj.browse(cr, uid, report_id, context=context)
        res = reports_obj.browse(cr, uid, report_id, context=context)[0].pentaho_report_output_type
        return res
        """

    _defaults = {
        'date_start': lambda *a: datetime.now().strftime('%Y-01-01'),
        'date_end': lambda *a: (datetime.now()).strftime('%Y-%m-%d'),
        'output_type': _get_output_type,
    }
    
    
    def _convert_string_to_date(self, dateText):
        """
            Simple convert date from string
            @dateText: Date as string
            @return: Date converted from string
        """
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
        prod_sales_data = {}
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
                if product_id in prod_sales_data:
                    record_data = prod_sales_data[product_id]
                else:
                    if (get_full_data):
                        record_data = {
                                       'product_id': product_id,
                                       'ean' : cur_product.ean13,
                                       'article_desc': cur_product.name,
                                       'article_number' : cur_product.default_code or '-',
                                       'quantity':0,
                                       'sum_total':0,
                                       'supplier':'',
                                       'sale_price': cur_product.list_price,
                                       }
                        
                        if (cur_product.seller_id):
                            seller_id_val = cur_product.seller_id.id
                            if ((supplier_id > 0) and (supplier_id <> seller_id_val)):
                                continue
                            record_data['supplier'] = cur_product.seller_id.name
                        elif supplier_id > 0:
                            continue
                        
                    
                        #=======================================================
                        # if (seller_ids and len(seller_ids) > 0):
                        #     record_data['supplier'] = seller_ids[0].name.name
                        #=======================================================
                    else:
                        record_data = {
                                       'product_id': product_id,
                                       'quantity':0,
                                       }
                    
                    
                
                record_data['quantity'] = record_data['quantity'] + invoice_line.quantity
                if (get_full_data):
                    record_data['sum_total'] = record_data['sum_total'] + invoice_line.price_subtotal
                
                prod_sales_data[product_id] = record_data
        return prod_sales_data
    
    def check_report(self, cr, uid, ids, context=None):
        """
            Create report data and save them
            @cr: cursor
            @uid: user id
            @ids: ids
            @context: context
            @return: open report
        """
                
        form_data = self.read(cr, uid, ids)[0]
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
        
        #TODO: supplier, Kategorie
               
        #=======================================================================
        # obj_model_settlements = self.pool.get('eq.sale.commission.settlement')
        #  
        #=======================================================================
        
        filter_date = []
        filter_date_prev_year = []
  
        prev_year_start = None
        prev_year_end = None
        data['variables'] = {}
        if (date_from or date_to):            
            if (date_from):
                filter_date.append(('create_date', '>=', date_from))
                
                
                
                date_to_conv = self._convert_string_to_date(date_from)
                prev_year_end = (date_to_conv).strftime('%Y-01-01')
                prev_year_start = (date_to_conv + relativedelta(years=-1)).strftime('%Y-01-01')
                
                filter_date_prev_year.append(('create_date', '>=', prev_year_start))
                filter_date_prev_year.append(('create_date', '<', prev_year_end))
                
                date_to_text_conv = date_to_conv.strftime('01.01.%Y')
                data['variables']['DateFrom'] = date_to_text_conv
                
            if (date_to):
                #+1Tag
                date_to_conv = self._convert_string_to_date(date_to)
                date_to_test_conv = (date_to_conv + relativedelta(days=1)).strftime('%Y-%m-%d')
                filter_date.append(('create_date', '<', date_to_test_conv))
                
                date_for_report = date_to_conv.strftime('%d.%m.%Y')
                data['variables']['DateTo'] = date_for_report
                
        
        #=======================================================================
        # if (filter_supplier_id > 0):
        #     filter_date.append(('invoice_line.product_id.seller_id.id', '=', filter_supplier_id))        
        #=======================================================================
        
        
        account_invoice_ids = []
        obj_account_invoice= self.pool.get('account.invoice')
        obj_account_invoice_line = self.pool.get('account.invoice.line')
        obj_prod_sales_data= self.pool.get('eq.product.sales.data')
        obj_prod_sales_data_master= self.pool.get('eq.product.sales.data.master')
        
        
        account_invoice_ids  = obj_account_invoice.search(cr, uid, filter_date)
        
        account_invoices = []    
        if (len(account_invoice_ids) > 0):
            account_invoices = obj_account_invoice.browse(cr, uid, account_invoice_ids, context=context)
        else:
            raise osv.except_osv(_('No Data!'),
                            _('There is no data for current filters.'))
            
            
        prod_sales_prev_data = {}
        account_invoice_prev_ids  = []
        if (len(filter_date_prev_year) > 0):
            account_invoice_prev_ids = obj_account_invoice.search(cr, uid, filter_date_prev_year)    
            account_invoices_prev = []  
            if (len(account_invoice_prev_ids) > 0):
                account_invoices_prev = obj_account_invoice.browse(cr, uid, account_invoice_prev_ids, context=context)
                prod_sales_prev_data = self._process_invoice_data(account_invoices_prev, False, filter_supplier_id, filter_category_id)
        
        
        prod_sales_data = self._process_invoice_data(account_invoices, True, filter_supplier_id, filter_category_id)
        if (len(prod_sales_data) == 0):
            raise osv.except_osv(_('No Data!'), _('There is no data for current filters.'))
        
        data_parent_id = obj_prod_sales_data_master.create(cr, uid, {}, context=context)
        data['variables']['Parent_ID'] = data_parent_id        
        if (len(prod_sales_data) > 0):
            for key, record in prod_sales_data.items():
                
                quantity_sale = record['quantity']
                record_data={
                    'parent_id' : data_parent_id,
                    'article_number' : record['article_number'],
                    'ean': record['ean'],
                    'article_desc': record['article_desc'],
                    'supplier' :  record['supplier'],
                    'sale_quantity' : quantity_sale,
                    'sale_sum_total' : record['sum_total'],
                    'sale_quantity_prev_year' : 0,
                    'sale_change' : 0,
                }
                
                quantity_sale_prev_year = 0
                if (key in prod_sales_prev_data):
                    prev_year_data = prod_sales_prev_data[key]
                    if (prev_year_data):
                        quantity_sale_prev_year = prev_year_data['quantity']
                        record_data['sale_quantity_prev_year'] =  quantity_sale_prev_year
                        
                #quantity_sale_prev_year = quantity_sale/2+2#TEST
                record_data['sale_quantity_prev_year'] = quantity_sale_prev_year
                if(quantity_sale_prev_year <> 0):
                    record_data['sale_change'] = (100 * float(quantity_sale-quantity_sale_prev_year)) / quantity_sale_prev_year
                
                # save our result into db, we'll use it in report
                obj_prod_sales_data.create(cr, uid, record_data, context=context)
                
                    
        filters = []
        if (context.get('active_ids', False)):
            filters.append(('id','in', context.get('active_ids', False)))
        
        #=======================================================================
        # obj_model = self.pool.get(model)
        # model_ids = obj_model.search(cr, uid, filters, context=context)        
        # if not model_ids:
        #     raise osv.except_osv(_('No Data!'),
        #                     _('There is no data for current filters.'))
        #=======================================================================
        data['ids'] = []        
        return self.print_report(cr, uid, ids, data, context=context) 
    
              
    def print_report(self, cr, uid, ids, mydata, context=None):
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
             'model': 'eq.product.sales.data',
             #'form': data
             'form': mydata
            } 
        return self.pool['report'].get_action(cr, uid, [], "equitania.eq_product_sales_report", data=datas, context=context)