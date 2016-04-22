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