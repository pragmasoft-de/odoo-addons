# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2010-TODAY Tech Receptives (<http://www.techreceptives.com>).
#
#    Authors : Tech Receptives & Win-Soft - Web Solution (http://www.win-soft.ch)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time

from openerp import SUPERUSER_ID
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_voucher(osv.osv):

    _inherit = "account.voucher"

    def default_get(self, cr, user, fields_list, context=None):
        """
        Fix field journal_id on voucher: Unknown journal entry

        Returns default values for fields
        @param fields_list: list of fields, for which default values are required to be read
        @param context: context arguments, like lang, time zone

        @return: Returns a dict that contains default values for fields
        """
        if context is None:
            context = {}
        values = super(account_voucher, self).default_get(
            cr, user, fields_list, context=context)
        if user != SUPERUSER_ID:
            values.update({'journal_id': False})
        return values

    def onchange_journal(self, cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id, context=None):
        '''
        Fix onchange journal id: set period for used date
        '''
        res = super(account_voucher, self).onchange_journal(cr, uid, ids, journal_id,
                                                            line_ids, tax_id, partner_id, date, amount, ttype, company_id, context=context)
        if date and res:
            period_ids = self.pool['account.period'].find(cr, uid, date, context=dict(
                context, company_id=company_id, account_period_prefer_normal=True))
            res['value']['period_id'] = period_ids and period_ids[0] or False
        return res

    def _get_writeoff_amount(self, cr, uid, ids, name, args, context={}):
        if not ids:
            return {}
        currency_obj = self.pool.get('res.currency')
        inv_obj = self.pool.get('account.invoice')
        res = {}
        diff_amount = 0.0
        debit = credit = total_inv_residual = 0.0
        for voucher in self.browse(cr, uid, ids, context=context):
            sign = voucher.type == 'payment' and -1 or 1
            if context.get('invoice_id'):
                inv = inv_obj.browse(cr, uid, context.get('invoice_id'))
                for l in voucher.line_dr_ids:
                    debit += l.amount
    #                 if context.has_key('click_register_payment'):
                    if voucher.payment_option == 'with_writeoff' and (l.move_line_id.invoice.id == context.get('invoice_id') or l.reconcile):
                        l.write(
                            {'reconcile': True, 'amount': l.amount_unreconciled})
                        total_inv_residual += (l.amount >
                                               0 and l.amount_unreconciled - l.amount)
#                     if voucher.payment_option == 'without_writeoff' and (l.move_line_id.invoice.id == context.get('invoice_id') or l.reconcile):
#                         l.write(
#                             {'reconcile': True, 'amount': l.amount_unreconciled})
#                         total_inv_residual += (l.amount >
# 0 and l.amount_unreconciled - l.amount)
                for l in voucher.line_cr_ids:
                    credit += l.amount
                    if context.has_key('click_register_payment'):
                        if voucher.payment_option == 'with_writeoff' and (l.move_line_id.invoice.id == context.get('invoice_id') or l.reconcile):
                            l.write(
                                {'reconcile': True, 'amount': l.amount_unreconciled})
                            total_inv_residual += (l.amount >
                                                   0 and l.amount_unreconciled - l.amount)
                currency = voucher.currency_id or voucher.company_id.currency_id
                write_off_amount = voucher.amount - sign * (credit - debit)
                if context.has_key('click_register_payment'):
                    write_off_amount = total_inv_residual * sign

                res[voucher.id] = currency_obj.round(
                    cr, uid, currency, write_off_amount)
        return res

    _columns = {
        'writeoff_amount': fields.function(_get_writeoff_amount, string='Difference Amount', type='float', readonly=True, help="Computed as the difference between the amount stated in the voucher and the sum of allocation on the voucher lines."),
    }

    def _compute_writeoff_amount(self, cr, uid, line_dr_ids, line_cr_ids, amount, type, context={}):
        # working on context to differentiate the button clicks without affecting the present code
        # Workaround to send context in _compute_writeoff_amount()
        debit = credit = total_inv_residual = 0.0
        sign = type == 'payment' and -1 or 1
        for l in line_dr_ids:
            if isinstance(l, dict):
                debit += l['amount']
                total_inv_residual += (l['amount'] >
                                       0 and l['amount_unreconciled'] - l['amount'])
        for l in line_cr_ids:
            if isinstance(l, dict):
                credit += l['amount']
                total_inv_residual += (l['amount'] >
                                       0 and l['amount_unreconciled'] - l['amount'])
        writeoff_amount = amount - sign * (credit - debit)
        if context.has_key('click_register_payment'):
            writeoff_amount = (total_inv_residual * sign)
        if context.get('default_amount'):
            total = context.get('default_amount')
            equal = (-1 * total)
            if not writeoff_amount == equal and amount > total:
                writeoff_amount = total - amount
        return writeoff_amount

    def onchange_line_ids(self, cr, uid, ids, line_dr_ids, line_cr_ids, amount, voucher_currency, type, context=None):
        # Workaround to send context in _compute_writeoff_amount()
        context = context or {}
        if not line_dr_ids and not line_cr_ids:
            return {'value': {'writeoff_amount': 0.0}}
        line_osv = self.pool.get("account.voucher.line")

        line_dr_ids = resolve_o2m_operations(
            cr, uid, line_osv, line_dr_ids, ['amount'], context)
        line_cr_ids = resolve_o2m_operations(
            cr, uid, line_osv, line_cr_ids, ['amount'], context)

        # compute the field is_multi_currency that is used to hide/display
        # options linked to secondary currency on the voucher
        is_multi_currency = False
        # loop on the voucher lines to see if one of these has a secondary
        # currency. If yes, we need to see the options
        for voucher_line in line_dr_ids + line_cr_ids:
            line_id = voucher_line.get('id') and self.pool.get('account.voucher.line').browse(
                cr, uid, voucher_line['id'], context=context).move_line_id.id or voucher_line.get('move_line_id')
            if line_id and self.pool.get('account.move.line').browse(cr, uid, line_id, context=context).currency_id:
                is_multi_currency = True
                break
        return {'value': {'writeoff_amount': self._compute_writeoff_amount(cr, uid, line_dr_ids, line_cr_ids, amount, type, context=context), 'is_multi_currency': is_multi_currency}}

    def recompute_voucher_lines(self, cr, uid, ids, partner_id, journal_id, price, currency_id, ttype, date, context=None):
        # Workaround to send context in _compute_writeoff_amount()
        """
        Returns a dict that contains new values and context

        @param partner_id: latest value from user input for field partner_id
        @param args: other arguments
        @param context: context arguments, like lang, time zone

        @return: Returns a dict which contains new values, and context
        """
        def _remove_noise_in_o2m():
            """if the line is partially reconciled, then we must pay attention to display it only once and
                in the good o2m.
                This function returns True if the line is considered as noise and should not be displayed
            """
            if line.reconcile_partial_id:
                if currency_id == line.currency_id.id:
                    if line.amount_residual_currency <= 0:
                        return True
                else:
                    if line.amount_residual <= 0:
                        return True
            return False

        if context is None:
            context = {}
        context_multi_currency = context.copy()

        currency_pool = self.pool.get('res.currency')
        move_line_pool = self.pool.get('account.move.line')
        partner_pool = self.pool.get('res.partner')
        journal_pool = self.pool.get('account.journal')
        line_pool = self.pool.get('account.voucher.line')

        # set default values
        default = {
            'value': {'line_dr_ids': [], 'line_cr_ids': [], 'pre_line': False, },
        }

        # drop existing lines
        line_ids = ids and line_pool.search(
            cr, uid, [('voucher_id', '=', ids[0])]) or False
        for line in line_pool.browse(cr, uid, line_ids, context=context):
            if line.type == 'cr':
                default['value']['line_cr_ids'].append((2, line.id))
            else:
                default['value']['line_dr_ids'].append((2, line.id))

        if not partner_id or not journal_id:
            return default

        journal = journal_pool.browse(cr, uid, journal_id, context=context)
        partner = partner_pool.browse(cr, uid, partner_id, context=context)
        currency_id = currency_id or journal.company_id.currency_id.id

        total_credit = 0.0
        total_debit = 0.0
        account_type = 'receivable'
        if ttype == 'payment':
            account_type = 'payable'
            total_debit = price or 0.0
        else:
            total_credit = price or 0.0
            account_type = 'receivable'

        if not context.get('move_line_ids', False):
            ids = move_line_pool.search(cr, uid, [('state', '=', 'valid'), ('account_id.type', '=', account_type), (
                'reconcile_id', '=', False), ('partner_id', '=', partner_id)], context=context)
        else:
            ids = context['move_line_ids']
        invoice_id = context.get('invoice_id', False)
        company_currency = journal.company_id.currency_id.id
        move_lines_found = []

        # order the lines by most old first
        ids.reverse()
        account_move_lines = move_line_pool.browse(
            cr, uid, ids, context=context)

        # compute the total debit/credit and look for a matching open amount or
        # invoice
        for line in account_move_lines:
            if _remove_noise_in_o2m():
                continue

            if invoice_id:
                if line.invoice.id == invoice_id:
                    # if the invoice linked to the voucher line is equal to the invoice_id in context
                    # then we assign the amount on that line, whatever the
                    # other voucher lines
                    move_lines_found.append(line.id)
            elif currency_id == company_currency:
                # otherwise treatments is the same but with other field names
                if line.amount_residual == price:
                    # if the amount residual is equal the amount voucher, we assign it to that voucher
                    # line, whatever the other voucher lines
                    move_lines_found.append(line.id)
                    break
                # otherwise we will split the voucher amount on each line (by
                # most old first)
                total_credit += line.credit or 0.0
                total_debit += line.debit or 0.0
            elif currency_id == line.currency_id.id:
                if line.amount_residual_currency == price:
                    move_lines_found.append(line.id)
                    break
                total_credit += line.credit and line.amount_currency or 0.0
                total_debit += line.debit and line.amount_currency or 0.0

        # voucher line creation
        for line in account_move_lines:

            if _remove_noise_in_o2m():
                continue

            if line.currency_id and currency_id == line.currency_id.id:
                amount_original = abs(line.amount_currency)
                amount_unreconciled = abs(line.amount_residual_currency)
            else:
                # always use the amount booked in the company currency as the
                # basis of the conversion into the voucher currency
                amount_original = currency_pool.compute(
                    cr, uid, company_currency, currency_id, line.credit or line.debit or 0.0, context=context_multi_currency)
                amount_unreconciled = currency_pool.compute(cr, uid, company_currency, currency_id, abs(
                    line.amount_residual), context=context_multi_currency)
            line_currency_id = line.currency_id and line.currency_id.id or company_currency
            rs = {
                'name': line.move_id.name,
                'type': line.credit and 'dr' or 'cr',
                'move_line_id': line.id,
                'account_id': line.account_id.id,
                'amount_original': amount_original,
                'amount': (line.id in move_lines_found) and min(abs(price), amount_unreconciled) or 0.0,
                'date_original': line.date,
                'date_due': line.date_maturity,
                'amount_unreconciled': amount_unreconciled,
                'currency_id': line_currency_id,
            }
            price -= rs['amount']
            # in case a corresponding move_line hasn't been found, we now try to assign the voucher amount
            # on existing invoices: we split voucher amount by most old first,
            # but only for lines in the same currency
            if not move_lines_found:
                if currency_id == line_currency_id:
                    if line.credit:
                        amount = min(amount_unreconciled, abs(total_debit))
                        rs['amount'] = amount
                        total_debit -= amount
                    else:
                        amount = min(amount_unreconciled, abs(total_credit))
                        rs['amount'] = amount
                        total_credit -= amount

            if rs['amount_unreconciled'] == rs['amount']:
                rs['reconcile'] = True

            if rs['type'] == 'cr':
                default['value']['line_cr_ids'].append(rs)
            else:
                default['value']['line_dr_ids'].append(rs)

            if ttype == 'payment' and len(default['value']['line_cr_ids']) > 0:
                default['value']['pre_line'] = 1
            elif ttype == 'receipt' and len(default['value']['line_dr_ids']) > 0:
                default['value']['pre_line'] = 1
            default['value']['writeoff_amount'] = self._compute_writeoff_amount(cr, uid, default[
                                                                                'value']['line_dr_ids'], default['value']['line_cr_ids'], price, ttype, context=context)
        return default

account_voucher()


class invoice(osv.osv):
    _inherit = 'account.invoice'

    def invoice_pay_customer(self, cr, uid, ids, context=None):
        # overriding function to send a special context...
        if not ids:
            return []
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(
            cr, uid, 'account_voucher', 'view_vendor_receipt_dialog_form')

        inv = self.browse(cr, uid, ids[0], context=context)
        return {
            'name': _("Pay Invoice"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'account.voucher',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': {
                'payment_expected_currency': inv.currency_id.id,
                'default_partner_id': self.pool.get('res.partner')._find_accounting_partner(inv.partner_id).id,
                'default_amount': inv.type in ('out_refund', 'in_refund') and -inv.residual or inv.residual,
                'default_reference': inv.name,
                'close_after_process': True,
                'invoice_type': inv.type,
                'invoice_id': inv.id,
                'default_type': inv.type in ('out_invoice', 'out_refund') and 'receipt' or 'payment',
                'type': inv.type in ('out_invoice', 'out_refund') and 'receipt' or 'payment',
                'click_register_payment': True,
            }
        }

invoice()


def resolve_o2m_operations(cr, uid, target_osv, operations, fields, context):
    results = []
    for operation in operations:
        result = None
        if not isinstance(operation, (list, tuple)):
            result = target_osv.read(
                cr, uid, operation, fields, context=context)
        elif operation[0] == 0:
            # may be necessary to check if all the fields are here and get the
            # default values?
            result = operation[2]
        elif operation[0] == 1:
            result = target_osv.read(
                cr, uid, operation[1], fields, context=context)
            if not result:
                result = {}
            result.update(operation[2])
        elif operation[0] == 4:
            result = target_osv.read(
                cr, uid, operation[1], fields, context=context)
        if result != None:
            results.append(result)
    return results
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
