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
from datetime import datetime, timedelta, date
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT

class eq_open_sale_order_line(models.Model):
    _name = 'eq_open_sale_order_line'
    
    """ hier wird noch der rest implementiert """
    
    # Felder
    eq_order_id = fields.Many2one('sale.order', string="Sale Order")
    eq_customer_no = fields.Char(size=64, string="Customer No")
    eq_customer = fields.Many2one('res.partner', string="Customer")    
    eq_delivery_date = fields.Date(string="Delivery date")
    eq_pos = fields.Integer(string="Seq")
    eq_quantity = fields.Integer(string="Quantity")
    eq_quantity_left = fields.Integer(string="Quantity left")    
    eq_product_no = fields.Many2one('product.product', string="Product number")    
    eq_description = fields.Char(size=300, string="Description")
    eq_drawing_no = fields.Char(size=100, string="Drawing number")
    
    def generate_statement(self):
        """ hier wird der Statement gespeichert und kann später geändert werden """
        sql = "todo"
        return sql
        