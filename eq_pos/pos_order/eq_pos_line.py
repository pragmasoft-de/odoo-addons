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

from openerp import tools
from openerp import models, fields, api, _
from datetime import datetime, timedelta, date
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT

class eq_pos_order_line(models.Model):
    _auto = False
    _name = 'eq.pos.order.line'
    _rec_name = "eq_pos_id"
    _order = 'eq_date_order desc'
    
    eq_pos_id = fields.Many2one('pos.order', string="Pos Order")
    #eq_customer_name = fields.Char(string="Customer name")
    eq_customer = fields.Many2one('res.partner', string="Customer")
    eq_customer_ref = fields.Char(string="Customer ref")  
    
    eq_date_order = fields.Datetime(string="Order date")
    eq_quantity = fields.Integer(string="Quantity")
    eq_product_id = fields.Many2one('product.product', string="Product")
    eq_product_default_code = fields.Char(string="Product code")
    eq_price_subtotal_incl = fields.Float(string="Price")
    eq_changed_product_text = fields.Char(string = "Changed text")
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'eq_pos_order_line')
        cr.execute("""
        CREATE OR REPLACE VIEW eq_pos_order_line AS (
            SELECT ROW_NUMBER() OVER(ORDER BY eq_pos_id) id,* 
            FROM (
                SELECT po.id as eq_pos_id, po.partner_id as eq_customer, po.date_order as eq_date_order, line.qty as eq_quantity,
                line.product_id as eq_product_id, line.price_subtotal_incl as eq_price_subtotal_incl,
                p.eq_customer_ref as eq_customer_ref,
                pp.default_code as eq_product_default_code,
                line.changed_text as eq_changed_product_text
                FROM pos_order po
                LEFT OUTER JOIN pos_order_line line on po.id = line.order_id
                LEFT OUTER JOIN res_partner p on p.id = po.partner_id
                LEFT OUTER JOIN product_product pp on pp.id = line.product_id
            ) a
        )
            """)