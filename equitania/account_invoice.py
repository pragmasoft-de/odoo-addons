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

# New API, Remove Old API import if the New API is used. Otherwise you'll get an import error.
from openerp import models, fields, api, _

class eq_account_invoice(models.Model):
    _inherit = "account.invoice"
    
    @api.model
    def _prepare_refund(self, invoice, date=None, period_id=None, description=None, journal_id=None):
        res = super(eq_account_invoice, self)._prepare_refund(invoice, date, period_id, description, journal_id)
        res['eq_contact_person_id'] = invoice.eq_contact_person_id.id
        res['user_id'] = invoice.user_id.id
        return res
    
    
    
class eq_account_invoice_line(models.Model):
    _inherit = "account.invoice.line"    
        
    @api.depends('discount', 'price_unit', 'quantity')
    def _compute_discount(self):
        for record in self:
            record.discount_value = record.discount / 100 * record.price_unit * record.quantity
            
    @api.depends('discount', 'discount_value')
    def _compute_discount_display(self):
        currency_symbol = ''
        if (self and self[0].invoice_id):            
            currency_symbol = self[0].invoice_id.currency_id.symbol
                   
        rep_helper_obj = self.env['eq_report_helper']
       
        for record in self:
            discounted_txt = rep_helper_obj.get_price(record.discount, self._context['lang'], 'Product Price', False)
            discounted_value_txt = rep_helper_obj.get_price(record.discount_value, self._context['lang'], 'Product Price', False)
            
            if currency_symbol:
                discounted_value_txt += ' ' + currency_symbol
            
            record.discount_display_text = discounted_txt + " %\n (" + discounted_value_txt + ")"
        
        
    discount_value = fields.Float(compute='_compute_discount', string='Discount value', store=False, readonly=True)
    discount_display_text = fields.Char(compute='_compute_discount_display', string='Discount', store=False, readonly=True)
    