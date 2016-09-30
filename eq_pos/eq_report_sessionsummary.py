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
from openerp.osv import osv
from openerp.report import report_sxw
from openerp import SUPERUSER_ID


class eq_report_sessionsummary(report_sxw.rml_parse):

    # variables for save of all possible vat categories
    vat_0   = 0        # 0% MwSt
    vat_7   = 0        # 7% MwSt
    vat_19  = 0        # 19% Mwst
    vat_total = 0      # 0% MwSt + 7% MwSt + 19%MwSt

    def __init__(self, cr, uid, name, context):
        """
            Initialization of all functions that can be called from our report
            @cr: cursor
            @uid: user id
            @name: name
            @context: context
        """
        
        super(eq_report_sessionsummary, self).__init__(cr, uid, name, context=context)        
        
        self.localcontext.update({
            'get_cash_turnover': self.get_cash_turnover,
            'get_taking': self.get_taking,
            'get_withdrawal': self.get_withdrawal,
            'get_goods_turnover': self.get_goods_turnover,
            'get_saled_vouchers': self.get_saled_vouchers,
            'get_vat_sum': self.get_vat_sum,
            'get_vat_sum_19': self.get_vat_sum_19,
            'get_vat_sum_7': self.get_vat_sum_7,
            'get_vat_sum_0': self.get_vat_sum_0,
            'get_taxed_turnover': self.get_taxed_turnover,
            'get_cash_only_turnover': self.get_cash_only_turnover,
            'get_cash_movement': self.get_cash_movement,
        })


    def _format_price(self, pos_session_price, language, currency):
        """
            Format price
            @pos_session_price: price to be formated
            @language: lanuage
            @currency: currency
            @return: formated price with currency symbol
        """
        return self.pool.get("eq_report_helper").get_standard_price(self.cr, self.uid, pos_session_price, language, currency)

    def _get_cash_turnover_value(self, pos_session):
        """
            Get turnover as float value - Umsatz
            @pos_session: actual pos session
            @return: formated turnover with currency symbol
        """
        result = 0
        for pos in pos_session.order_ids:
            for line in pos.lines:
                result += line.price_subtotal_incl# price_unit #geändert 14.04.2016

        return result

    def get_cash_turnover(self, pos_session):
        """
            Get turnover and convert it to string- Umsatz
            @pos_session: actual pos session
            @return: formated turnover with currency symbol
        """
        result_value = self._get_cash_turnover_value(pos_session)
        return self._format_price(result_value, pos_session.user_id.lang, pos_session.currency_id)

    def get_cash_only_turnover(self, pos_session):
        """
            Get cash only turnover -> Baremumsatz = [Gesamtumsatz_BAR] + ([Entnahme] - [Einzahlung])
            @pos_session: actual session
            @return: Formatted cash only turnover together wird currency         
        """
        result_value = self._get_cash_only_turnover_value(pos_session)
        return self._format_price(result_value, pos_session.user_id.lang, pos_session.currency_id)
 
    def _get_cash_only_turnover_value(self, pos_session):
        """
            Get cash only turnover -> Baremumsatz = [Gesamtumsatz_BAR] + ([Entnahme] - [Einzahlung])
            @pos_session: actual session
            @return: Cash only turnover         
        """                
        result = 0        
        # 1. zuerst Gesamtum satz von BAR holen
        cash_only_value = 0                 # Gesamtumsatz - nur BAR
        #coupon_journal = self.pool.get('account.journal').search(self.cr, self.uid, [('code', '=', 'TCSH')])                            # old version
        
        # nicht mehr Case sensitive
        coupon_journal = self.pool.get('account.journal').search(self.cr, self.uid, ['|', ('code', '=', 'TCSH'), ('code', 'ilike', 'BAR')])    #HIER
        #print "* coupon_journal: ", coupon_journal
        bank_account_statment_obj = self.pool.get("account.bank.statement")                
        if len(coupon_journal) > 0:
            line_ids = bank_account_statment_obj.search(self.cr, self.uid, [('pos_session_id', '=', pos_session.id), ('journal_id', '=', coupon_journal[0])], None)
            for line_id in line_ids:
                line = bank_account_statment_obj.browse(self.cr, self.uid, line_id, None)
                cash_only_value += line.total_entry_encoding            # Gesamtumsatz - nur BAR
        
            #print "* Gesamtumsatz - nur BAR: ", cash_only_value
            
            # 2. Einzahlung
            taking = self._get_taking_value(pos_session.cash_register_id, True)
            #print "* Einzahlungen: ", taking
            
            # 3. Entnahme
            withdrawal = self._get_taking_value(pos_session.cash_register_id, False) * -1
            #print "* Entnahme: ", withdrawal
            
            # 4. Barumsatz = Gesamtumsatz + (Entnahme - Einzahlung)
            #print "Barumsatz = Gesamtumsatz + (Entnahme - Einzahlung)"
            result = cash_only_value + (withdrawal - taking)
            
        #print "* Barumsatz: ", result
        return result
    
    def get_cash_movement(self, pos_session):
        """
            Get cash movement -> Kassenbewegung = Barenumsatz - (Entnahme - Einzahlung)
            @pos_session: actual session
            @return: Formatted cash movement together wird currency
        """
        result_value = self._get_cash_movement_value(pos_session)
        return self._format_price(result_value, pos_session.user_id.lang, pos_session.currency_id)
    
    def _get_cash_movement_value(self, pos_session):
        """
            Get cash movement -> Kassenbewegung = Barenumsatz - (Entnahme - Einzahlung)
            @pos_session: actual session
            @return: cash movement together wird currency
        """        
        # 1. Barenumsatz
        cash_only_turnover = self._get_cash_only_turnover_value(pos_session)
        #print "* Barenumsatz: ", cash_only_turnover
                         
        # 2. Einzahlung
        taking = self._get_taking_value(pos_session.cash_register_id, True)
        #print "* Einzahlungen: ", taking
        
        # 3. Entnahme
        withdrawal = self._get_taking_value(pos_session.cash_register_id, False) * -1
        #print "* Entnahme: ", withdrawal
        
        # 4. Kassenbewegung = Barenumsatz - (Entnahme - Einzahlung)
        #print "Kassenbewegung = Barenumsatz - (Entnahme - Einzahlung)"
        result =  cash_only_turnover - (withdrawal - taking)
        #print "* Kassenbewegung: ", result
        return result      
         
        
    def _get_taking_value(self, statement_id, get_taking_values):
        """
            Get taking value as float (Einnahme / Entnahme)
            @statement_id: statement_id link in account_bank_statement_line table
            @get_taking_values: true => get positive values (Einnahme)
            @return: Total sum
        """
        result = 0
        line_obj = self.pool.get("account.bank.statement.line")
        line_ids = line_obj.search(self.cr, self.uid, [('statement_id', '=', statement_id.id)], None)
        for line_id in line_ids:
            line = line_obj.browse(self.cr, self.uid, line_id, None)
            if get_taking_values:                                                   # only "Einnahme"
                if line.amount > 0 and line.pos_statement_id.id is False:
                    result += line.amount
            else:
                if line.amount < 0 and line.pos_statement_id.id is False:           # only "Entnahme"
                    result += line.amount

        return result

    def get_taking(self, pos_session):
        """
            Get taking value and convert it to string (Einnahme / Entnahme)
            @pos_session: actual pos_session object
            @return: total sum coverted to string together with currency
        """
        result_value = self._get_taking_value(pos_session.cash_register_id, True)
        return self._format_price(result_value, pos_session.user_id.lang, pos_session.currency_id)

    def get_withdrawal(self, pos_session):
        """
            Get withdrawal (Entnahme)
            @pos_session: actual pos_session object
            @return: total sum coverted to string together with currency
        """
        result_value = self._get_taking_value(pos_session.cash_register_id, False)
        return self._format_price(result_value, pos_session.user_id.lang, pos_session.currency_id)

    def _get_saled_vouchers_value(self, pos_session):
        """
            Summ of all saled vouchers as float - Gutscheinverkauf
            @pos_session: actual pos session
            @return: total price of all saled vouchers
        """
        result = 0
        # traverse all pos_order_lines and check if linked product is a voucher
        for pos in pos_session.order_ids:
            for line in pos.lines:
                if line.product_id.product_tmpl_id.is_coupon:       # check if linked position..and it's product is defined as voucher
                  #print "line: ", line
                  result += line.price_subtotal_incl #line.price_unit; geändert 14.04.

        return result

    def get_saled_vouchers(self, pos_session):
        """
            Summ of all saled vouchers converted into string - Gutscheinverkauf
            @pos_session: actual pos session
            @return: total price of all saled vouchers
        """
        result_value = self._get_saled_vouchers_value(pos_session)
        return self._format_price(result_value, pos_session.user_id.lang, pos_session.currency_id) 

    def get_redeem_vouchers(self, pos_session):
        """
            Get sum of all reddemed vouchers as float - Gutscheineinlösung
            @pos_session: actual pos session
            @return: sum of all reddemed vouchers
        """
        result = 0
        #coupon_journal = self.pool.get('account.journal').search(self.cr, self.uid, [('code', '=', 'CPNJ')])                                                # old version
        coupon_journal = self.pool.get('account.journal').search(self.cr, self.uid, [ '|', ('code', '=', 'CPNJ'), ('code', '=', 'GuEin')])  #HIER                   # new version
        
        bank_account_statment_obj = self.pool.get("account.bank.statement")
        line_ids = bank_account_statment_obj.search(self.cr, self.uid, [('pos_session_id', '=', pos_session.id), ('journal_id', '=', coupon_journal[0])], None)
        for line_id in line_ids:
            line = bank_account_statment_obj.browse(self.cr, self.uid, line_id, None)
            result += line.total_entry_encoding

        return result

    def get_goods_turnover(self, pos_session):
        """
            Get and calculate goods turnover - Warenumsatz
            This value is calculated like with this formel:
            Warenumsatz = Kassenumsatz + Gutschriftseinlösung - Gutscheinverkauf
            @pos_session: actual pos session
            @return: formated goods turnover with currency symbol
        """
        turnover = self._get_cash_turnover_value(pos_session)
        #print "Kassenumsatz: ", turnover
        voucher_redem = self.get_redeem_vouchers(pos_session)       # Gutscheineinlösung
        #print "Gutschriftseinlösung: ", voucher_redem
        voucher_sale = self._get_saled_vouchers_value(pos_session)        # Gutscheinverkauf
        #print "Gutscheinverkauf: ", voucher_sale
        #print "Warenumsatz = Kassenumsatz + Gutschriftseinlösung - Gutscheinverkauf"
        goods_turnover_result = turnover + voucher_redem - voucher_sale
        #print "**** Warenumsatz: ", goods_turnover_result
        return self._format_price(goods_turnover_result, pos_session.user_id.lang, pos_session.currency_id)

    def _check_if_product_is_voucher(self, product_id):
        """
            Check if actual product is defined as voucher
            @product_id: actual product
            @return: True => yes, it's defined as voucher
        """        
        return product_id.product_tmpl_id.is_coupon
        
    def get_vat_sum(self, pos_session):
        """
            Get all vat values (for 19%, 7% and 0%) and calculate sum (Umsätze - Gesamtverkäufe)
            ! Ignore voucher position !
            Bruttoumsatz mit 19% MwSt
            Bruttoumsatz mit 7% MwSt
            Steuerfreie Lieferung 0% MwSt
            @pos_session: actual pos session
            @return: total vat sum 
        """
        
        for pos in pos_session.order_ids:
            use_as_position_with_0 = False
            if pos.partner_id.id is not False:
                use_as_position_with_0 = True            
                
            for line in pos.lines:            
                position_is_voucher = self._check_if_product_is_voucher(line.product_id)    # check if actual position is defined as voucher
                if position_is_voucher is False:                                            # ok it's normal position, so you can use prices and all stuff
                    if use_as_position_with_0 is False:
                        if line.product_id.taxes_id.eq_price_percentage == "19":            # check vat category - it's 19%
                            self.vat_19 += line.price_subtotal_incl#.price_unit
                        elif line.product_id.taxes_id.eq_price_percentage == "7":           # check vat category - it's 7%
                            self.vat_7 += line.price_subtotal_incl#.price_unit
                    else:
                        self.vat_0 += line.price_subtotal_incl#.price_unit                                       # it's 0%                
            
        #print "* vat_19: ", self.vat_19
        #print "* vat_7: ", self.vat_7
        #print "* vat_0: ", self.vat_0                
        return -1       # it's ok, we'fre not using the return value here so be cool...it's just to be sure

    def get_vat_sum_19(self, pos_session):
        """
            Get 19% VAT sum, convert it to string and add currency symbol (Umsatz 19%)
            @pos_session: actual pos_session
            @return: 19%VAT formated as string together with currency symbol
        """        
        return self._format_price(self.vat_19, pos_session.user_id.lang, pos_session.currency_id)    

    def get_vat_sum_7(self, pos_session):
        """
            Get 7% VAT sum, convert it to string and add currency symbol (Umsatz 7%)
            @pos_session: actual pos_session
            @return: 7%VAT formated as string together with currency symbol
        """
        return self._format_price(self.vat_7, pos_session.user_id.lang, pos_session.currency_id)

    def get_vat_sum_0(self, pos_session):
        """
            Get 0% VAT sum for all customers from world (ignored eu), convert it to string and add currency symbol (Umsatz 19%)
            @pos_session: actual pos_session
            @return: 0%VAT formated as string together with currency symbol
        """
        if self.vat_0 == 0 or self.vat_7 == 0 or self.vat_19 == 0: 
            self.get_vat_sum(pos_session)
            
        return self._format_price(self.vat_0, pos_session.user_id.lang, pos_session.currency_id)

    def get_taxed_turnover(self, pos_session):
        """
            Get taxed turnover (sum of all vats), convert it to string and add currency symbol (versteuerter Umsatz)
            @pos_session: actual pos_session
            @return: total sum of all taxed turnovers
        """
        vat_total = self.vat_0 + self.vat_7 + self.vat_19
        return self._format_price(vat_total, pos_session.user_id.lang, pos_session.currency_id)


class report_lunchorder(osv.AbstractModel):
    _name = 'report.point_of_sale.report_sessionsummary'
    _inherit = 'report.abstract_report'
    _template = 'point_of_sale.report_sessionsummary'
    _wrapped_report_class = eq_report_sessionsummary
    
    
class report_lunchorder_short(osv.AbstractModel):
    _name = 'report.eq_pos.eq_report_sessionsummary_short'
    _inherit = 'report.abstract_report'
    _template = 'eq_pos.eq_report_sessionsummary_short'
    _wrapped_report_class = eq_report_sessionsummary    