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
    
    def _set_group_for_users(self, cr, uid, ids=None, context= None):
        #Group purchase_in_products
        sql_exists_query = """
        select exists(select * from res_groups_users_rel where gid = (select res_id from ir_model_data where name = 'purchase_in_products' and module = 'equitania'))
        """
        cr.execute(sql_exists_query)
        if not cr.fetchone()[0]:
            sql_insert_query = """
            insert into res_groups_users_rel
            select (select res_id from ir_model_data where name = 'purchase_in_products' and module = 'equitania') as gid, id as uid  from res_users 
            where id not in 
            (select uid from res_groups_users_rel where gid = (select res_id from ir_model_data where name = 'purchase_in_products' and module = 'equitania'))
            """
            cr.execute(sql_insert_query)
            cr.commit()
        #Group supplier_in_account
        sql_exists_query = """
        select exists(select * from res_groups_users_rel where gid = (select res_id from ir_model_data where name = 'supplier_in_account' and module = 'equitania'))
        """
        cr.execute(sql_exists_query)
        if not cr.fetchone()[0]:
            sql_insert_query = """
            insert into res_groups_users_rel
            select (select res_id from ir_model_data where name = 'supplier_in_account' and module = 'equitania') as gid, id as uid  from res_users 
            where id not in 
            (select uid from res_groups_users_rel where gid = (select res_id from ir_model_data where name = 'supplier_in_account' and module = 'equitania'))
            """
            cr.execute(sql_insert_query)
            cr.commit()
        return True
        
    def _set_paper_format(self, cr, uid, ids=None, context=None):
        """
        eu_a4_reports = self.pool.get('ir.actions.report.xml').search(cr, uid, ['|', '|', '|',('report_name', '=', 'purchase.report_purchaseorder'), ('report_name', '=', 'purchase.report_purchasequotation'), ('report_name', '=', 'account.report_invoice'), ('report_name', '=', 'sale.report_saleorder')])
        
        for report in eu_a4_reports:
            val = {'paperformat_id': 1,}
            self.pool.get('ir.actions.report.xml ').write(cr, uid, ids, val)
        """
        
        paperformat_obj = self.pool.get('report.paperformat')
        report_obj = self.pool.get('ir.actions.report.xml')
        
        if len(paperformat_obj.search(cr, uid, [('name', '=', 'EQ European A4')])) == 0:
            eq_a4_report_ids = report_obj.search(cr, uid, [('model', 'in', ('sale.order', 'account.invoice', 'purchase.order', 'eq_framework_agreement', 'stock.picking'))])
            
            eu_a4 = {
                     'page_width': 0,
                     'orientation': 'Portrait', 
                     'header_line': False, 
                     'default': True, 
                     'format': 'A4', 
                     'header_spacing': 49, 
                     'margin_right': 17, 
                     'margin_top': 49, 
                     'margin_left': 17, 
                     'margin_bottom': 23, 
                     'page_height': 0, 
                     'display_name': 'EQ European A4', 
                     'report_ids': [(6, 0, eq_a4_report_ids)], 
                     'dpi': 90, 
                     'name': 'EQ European A4'}
            eu_a4_intern_id = paperformat_obj.create(cr, uid, eu_a4)
               
        if len(paperformat_obj.search(cr, uid, [('name', '=', 'EQ European A4 Intern')])) == 0:
            eu_a4_intern_report_ids = report_obj.search(cr, uid, [('model', 'in', ('eq_open_sale_order_line', 'mrp.bom', 'eq_calculation.data'))])
                   
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
                     'display_name': 'EQ European A4 Intern', 
                     'report_ids': [(6, 0 , eu_a4_intern_report_ids)], 
                     'dpi': 90, 
                     'name': 'EQ European A4 Intern'}
            
            eu_a4_intern_id = paperformat_obj.create(cr, uid, eu_a4_intern)
            
        if len(paperformat_obj.search(cr, uid, [('name', '=', 'EQ European A4 Intern Fertigung')])) == 0:
            eu_a4_intern_mrp_report_ids = report_obj.search(cr, uid, [('model', 'in', ('mrp.production',))])
               
            eu_a4_intern_mrp = {
                     'page_width': 0,
                     'orientation': 'Portrait', 
                     'header_line': False, 
                     'default': True, 
                     'format': 'A4', 
                     'header_spacing': 30, 
                     'margin_right': 17, 
                     'margin_top': 35, 
                     'margin_left': 17, 
                     'margin_bottom': 24, 
                     'page_height': 0, 
                     'display_name': 'EQ European A4 Intern Fertigung', 
                     'report_ids': [(6, 0, eu_a4_intern_mrp_report_ids)], 
                     'dpi': 90, 
                     'name': 'EQ European A4 Intern Fertigung'}
            
            eu_a4_intern_id = paperformat_obj.create(cr, uid, eu_a4_intern_mrp)
        
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
           
    def _update_localization(self, newstring, translation_id, ir_translation_obj, cr, uid):
        # prepare new value for our text
        vals = {
                        'value': newstring,
                        'state': 'translated',
                }
        
        # update it..doesn't matter if for one or multiple records
        ir_translation_obj.write(cr, uid, translation_id, vals)

    
    def _localize_backend(self, valid_entries, ir_translation_obj, ir_ui_view_obj, cr, uid):
        """
            U code:    EXAMPLE
                    #. module: equitania
                    #: code:addons/equitania/stock.py:136
                    #, python-format
                    msgid "Change date done"
                    msgstr "Lieferdatum ändern"
                    
            U selection:    EXAMPLE
                    #. module: equitania
                    #: selection:eq_open_sale_order_line,eq_state:0
                    msgid "Cancelled"
                    msgstr "Abgebrochen"
                    * dont need res_id                    

            U help:    EXAMPLE (type = help, value = our new text, name = "sale.order.line,eq_agreement_id")
                    #. module: eq_framework_agreement
                    #: help:sale.order.line,eq_agreement_id:0
                    msgid "Framework Agreement"
                    msgstr "Rahmenauftrag"
                    * dont need res_id
            
            U view:    EXAMPLE (type = view, value = our new text, name = "eq_open_sale_order_line")
                    #. module: equitania
                    #: view:eq_open_sale_order_line:equitania.eq_open_sale_order_line_search_view
                    #: view:purchase.order.line:equitania.eq_purchase_order_line_search_inherit
                    msgid "Frameworkagreement"
                    msgstr "Rahmenauftrag"           
            
            U field:    EXAMPLE (type = field, value = our new text, name = "eq_framework_agreement.pos,eq_agreement_id")
                    #. module: equitania
                    #: field:eq_framework_agreement.pos,eq_agreement_id:0
                    * dont need res_id

            U model:    EXAMPLE (type = model, value = our new text, name = "ir.actions.act_window,name")
                    #. module: equitania
                    #: model:ir.actions.act_window,name:eq_framework_agreement.eq_framework_agreement_action
        """
        try:        
            for entry in valid_entries:            
                #print "############################################"
                result = entry.comment.split(":")
                module = result[1].strip()
                #print "module", module
                #print "############################################"
                
                for occurence in entry.occurrences:
                        #print "occurence", occurence
                        occurence_split = occurence[0].split(':')
                        #print "occurence_split", occurence_split
                        record_type = occurence_split[0]
                        if occurence_split[1] != 'website':
                            name = occurence_split[1]                                                                                
                            msgid = entry.msgid
                            msgstr = entry.msgstr
                            lang = "de_DE"
                            state = "translated"
                                                    
                            #print "name", name   
                            #print "type", record_type
                            #print "lang", lang
                            #print "module", module
                            #print "source", msgid  
                            #print "value", msgstr                                                                                                                                                                    
                            #print "--------------------------------------------------------------------------------"                          
                            translation_id = ir_translation_obj.search(cr, uid, [('src', '=', entry.msgid), ('name', '=', name), ('module', '=', module), ('lang', '=', 'de_DE')])
                            #print "translation_id", translation_id
                            if len(translation_id) > 0:
                                self._update_localization(entry.msgstr, translation_id, ir_translation_obj, cr, uid)
                            else:
                                self._insert_localization()
        except:
            pass
                                                       
    def _load_translation(self, cr, uid, ids=None, context=None, eval=None):
        """
            Localization helper
            - reads all terms from german po file
            - updates / created terms in ir_translation table
            
            @cr: cursor
            @uid: user id
            @ids: ids
            @context: context
        """    
        
        # extract module name from function call EVAL from extern modules (the call is in each view)
        actual_module = 'equitania'        
        if ids is not None:
            actual_module = ids
        
        addon_folder = get_module_path(actual_module)
        #print "#### actual_module", actual_module
        #print "#### addon_folder", addon_folder        
        
        # german langauage
        german_lang = self.pool.get('res.lang').search(cr, uid, [('code', '=', 'de_DE')])
        if len(german_lang) != 0:
            po = polib.pofile(addon_folder + '/i18n/de.po')
            valid_entries = [e for e in po if not e.obsolete]
            ir_translation_obj = self.pool.get('ir.translation')
            ir_ui_view_obj = self.pool.get('ir.ui.view')
            ir_translation_obj.clear_caches()
                        
            # start localization for everything else than view:website
            self._localize_backend(valid_entries, ir_translation_obj, ir_ui_view_obj, cr, uid)
            
            for entry in valid_entries:            
                for occurence in entry.occurrences:
                    occurence_split = occurence[0].split(':')
                    #Views
                    if occurence_split[0] == 'view':                        
                        #website reports
                        if occurence_split[1] == 'website':
                            report_id = occurence_split[2].split('.')[-1]
                            model_name = occurence_split[2].split('.')[0]
                            model_ids = self.pool.get('ir.model.data').search(cr, uid, [('module', '=', model_name), ('model', '=', 'ir.ui.view')]) 
                            if len(ir_ui_view_obj.search(cr, uid, [('name', 'ilike', report_id), ('type', '=', 'qweb'), ('model_data_id', 'in', model_ids)])) != 0 and len(model_ids):
                                view_id = ir_ui_view_obj.search(cr, uid, [('name', 'ilike', report_id), ('type', '=', 'qweb'), ('model_data_id', 'in', model_ids)])[0]
                                translation_id = ir_translation_obj.search(cr, uid, [('src', '=', entry.msgid), ('res_id', '=', view_id), ('name', '=', occurence_split[1]), ('lang', '=', 'de_DE')])                                                                
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
                                            'value': entry.msgstr,
                                            'type': occurence_split[0],
                                            }
                                    ir_translation_obj.create(cr, uid, vals)                                    
        return True