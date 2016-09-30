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

# 
from openerp import fields, models, api, _
from datetime import timedelta
from datetime import datetime, date, timedelta
import time



MAX_VALIDITY = 3650                # Maximale mögliche Gültigkeit für das Ablaufdatum


class pos_coupon(models.Model):
    _name = "pos.coupon"
    _order = "create_date desc"

    @api.multi
    def _get_cust(self):
        users_obj = self.env['res.users'].browse(self._uid)
        company_id = users_obj.company_id.id
        return company_id

    company_id = fields.Many2one('res.company', 'Company', readonly=True, default=_get_cust)
    name = fields.Char('Description', size=128)
    line_ids = fields.One2many('pos.coupon.line', 'coupon_id', 'Lines')
    coupon_history = fields.One2many('pos.coupon.history', 'coupon_id', 'Hostory Lines', readonly=True)
    
class pos_coupon_line(models.Model):
    _name = "pos.coupon.line"

    @api.multi
    def recharge_coupon(self, product_id, validity_days, price):
        
        # zur Sicherheit..falls der Benutzer bei dem Gutschein (im Produkt, auf der Lasche 'Gutscheine' in dem Feld 'Gutschein-Gültigkeitstage''
        # eine sehr größe Nummer eingibt, setzen wir es wieder zurück auf unseren Default
        if validity_days > MAX_VALIDITY:
            validity_days = MAX_VALIDITY
                
        coup_history_obj = self.env['pos.coupon.history']        
        if self.product_id.id == product_id:
            self.date_recharge_line = date.today()            
            self.date_expiry_line = date.today() + timedelta(days=validity_days)
            self.remaining_amt = self.remaining_amt + price
            history_vals = {'name': self.name, 'used_amount': price, 'used_date': date.today(), 'coupon_id': self.coupon_id.id}
            coupon_hist_id = coup_history_obj.create(history_vals)
        else:
            self.date_recharge_line = date.today()                        
            self.date_expiry_line = date.today() + timedelta(days=validity_days)
            self.product_id = product_id
            self.remaining_amt = self.remaining_amt + price
            history_vals = {'name': self.name, 'used_amount': price, 'used_date': date.today(), 'coupon_id': self.coupon_id.id}
            coupon_hist_id = coup_history_obj.create(history_vals)
        return coupon_hist_id and coupon_hist_id.id or False

    @api.one
    def _compute_is_manager_default(self):
        group_id = self.env['ir.model.data'].get_object_reference('eq_pos', 'group_coupon_manager')[1]
        group = self.env['res.groups'].browse(group_id)
        if self.env.user in group.users:
            self.group_coupon_manager = True
            return True
        self.group_coupon_manager = False
        return False

    @api.multi
    def _compute_is_manager(self):
        group_id = self.env['ir.model.data'].get_object_reference('eq_pos', 'group_coupon_manager')[1]
        group = self.env['res.groups'].browse(group_id)
        for res in self:
            if res.env.user in group.users:
                res.group_coupon_manager = True
                return True
            res.group_coupon_manager = False
        return False

    name = fields.Char('Coupon Serial', size=264)
    amount = fields.Float('Amount')
    remaining_amt = fields.Float('Remaining Amount', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    coupon_id = fields.Many2one('pos.coupon', 'Coupon', ondelete="cascade")
    validity = fields.Integer(string="Validity", readonly=True)
    remaining_validity_days = fields.Integer(string="Remaining validity days")
    date_create_line = fields.Date(string="Issue Date", readonly=True)
    date_recharge_line = fields.Date(string="Last Recharge Date", readonly=True)
    date_expiry_line = fields.Date(string="Expiry Date")
    group_coupon_manager = fields.Boolean('Coupon Manager', compute='_compute_is_manager', default=_compute_is_manager_default)

    @api.model
    def create(self, vals):
        if self._context is None:
            self._context = {}
        date_create = time.strftime("%Y:%m:%d")
        date_formatted_create = datetime.strptime(date_create , '%Y:%m:%d')
        rec_date_formatted_create = datetime.strptime(date_create , '%Y:%m:%d')
        validity = vals.get('validity', 0)
        vals['date_create_line'] = date_formatted_create
        vals['date_recharge_line'] = rec_date_formatted_create
        
        # zur Sicherheit..falls der Benutzer bei dem Gutschein (im Produkt, auf der Lasche 'Gutscheine' in dem Feld 'Gutschein-Gültigkeitstage''
        # eine sehr größe Nummer eingibt, setzen wir es wieder zurück auf unseren Default
        if validity > MAX_VALIDITY:
            validity = MAX_VALIDITY
        
        vals['date_expiry_line'] = date_formatted_create + timedelta(days=validity)            
        return super(pos_coupon_line, self).create(vals)
    
pos_coupon_line()


class pos_coupon_history(models.Model):
    _name = "pos.coupon.history"
        
    name = fields.Char('Coupon Serial', size=264)
    used_amount = fields.Float('Used Amount')
    used_date = fields.Date('Used Date')
    coupon_id = fields.Many2one('pos.coupon', 'Coupon')
    pos_order = fields.Char('POS Order')
    
    _defaults = {
        'used_date': lambda *a: time.strftime('%Y-%m-%d')
    }

pos_coupon_history()


class product_template(models.Model):
    _inherit = "product.template"

    is_coupon = fields.Boolean('Is Coupon')


class product_product(models.Model):
    _inherit = "product.product"
    
    validity_days = fields.Integer('Coupon Validity Days', default=MAX_VALIDITY)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: