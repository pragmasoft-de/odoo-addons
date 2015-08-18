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
from openerp.osv import osv
from datetime import datetime

class eq_sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    
    eq_optional = fields.Boolean(string="Optional")
    
    @api.multi
    def remove_production(self):
        return True
    
    def create_order_line_del_message(self):
        message_vals = {
                        'body': _('<div><b>Position Storniert</p></div><div>Product: ' + (self.product_id.name if self.product_id.name else self.name) + '\nMenge: ' + str(self.product_uom_qty)),
                        'date': datetime.now(),
                        'res_id': self.order_id.id,
                        'record_name': self.order_id.name,
                        'model': 'sale.order',
                        'type': 'comment',
                        }
        self.env['mail.message'].create(message_vals)
    
    @api.multi
    def unlink(self):
        #When a order line where an order is already done is removed, the apropriate stock move is canceled
        proc_obj = self.env['procurement.order']
        for rec in self:
            if rec.state in ['confirmed']:
                procurements = proc_obj.search([('sale_line_id', '=', rec.id), ('production_id', '=', False)])
                if any(proc.state in ('done') for proc in procurements):
                    raise osv.except_osv(_('Lieferung durchgeführt!'), _('Eine Teillieferung/Lieferung wurde für das Produkt "%s" mit der Menge "%s" bereits durchgeführt.') %(rec.product_id.name, rec.product_uom_qty))
                else:
                    rec.remove_production()
                    for proc in procurements:
                        proc.cancel()
                        move = self.env['stock.move'].search([('procurement_id', '=', proc.id)])
                        move.unlink()
                    rec.state = 'cancel'
                    rec.order_id.signal_workflow('ship_recreate')
            rec.create_order_line_del_message()
        return super(eq_sale_order_line, self).unlink()
    
class eq_sale_order(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    def action_button_confirm_optional(self):
        warning_msgs = False
        for line in self.order_line:
            if line.eq_optional:
                warning_msgs = True


        if warning_msgs:
            vals = {
                    'eq_info_text': _("All the optional positions will be removed."),
                    'eq_sale_id': self.id,
                    }
            new_popup = self.env['eq_info_optional'].create(vals)
            view = self.env.ref('equitania.eq_info_optional_form_view')
            return {
                'name': _('Not enough stock !'),
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view.id,
                'res_model': 'eq_info_optional',
                'context': "{}",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'res_id': new_popup.id,
            }
        else:
            return super(eq_sale_order, self).action_button_confirm()
        
class eq_info_optional(models.TransientModel):
    _name = 'eq_info_optional'
    
    eq_info_text = fields.Text()
    eq_sale_id = fields.Many2one('sale.order')
    
    @api.multi
    def action_done(self):
        for line in self.eq_sale_id.order_line:
            if line.eq_optional:
                line.unlink()
        self.eq_sale_id.action_button_confirm()
        return True