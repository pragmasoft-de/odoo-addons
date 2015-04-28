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

from openerp import models, fields, api, _
from datetime import datetime

class eq_date_done_change(models.TransientModel):
    _name = "eq.date.done.change"
    
    eq_new_date_done = fields.Datetime(string="New Date", required=True)
    eq_reason = fields.Text(string="Reason")
    
    @api.multi
    def create_message(self, description, picking_id, picking_name, old_date, new_date):
        message_vals = {
                        'body': _('<div><b>Changed Delivery Date</p></div><div>From: ' + old_date + ' To: ' + new_date + '<div>Reason: ' + description + '</div>'),
                        'date': datetime.now(),
                        'res_id': picking_id,
                        'record_name': picking_name,
                        'model': 'stock.picking',
                        'type': 'comment',
                        }
        self.env['mail.message'].create(message_vals)
    
    @api.multi
    def confirm_action(self):
        print self.env.context['picking_id']
        values = {
                  'date_done': self.eq_new_date_done,
                  }
        picking = self.env['stock.picking'].browse(self.env.context['picking_id'])
        self.create_message(self.eq_reason, picking.id, picking.name, picking.date_done, self.eq_new_date_done)
        picking.write(values)
        return True
        