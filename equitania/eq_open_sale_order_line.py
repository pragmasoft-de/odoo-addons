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

class eq_open_sale_order_line(models.Model):
    _auto = False
    _name = 'eq_open_sale_order_line'
    
    # Felder
    eq_order_id = fields.Many2one('sale.order', string="Sale Order")
    eq_framework_agreement_id = fields.Many2one('eq_framework_agreement', string="Framework Agreement")
    eq_customer_no = fields.Char(size=64, string="Customer No")
    eq_customer = fields.Many2one('res.partner', string="Customer")    
    eq_delivery_date = fields.Date(string="Delivery date")
    eq_pos = fields.Integer(string="Seq")
    eq_quantity = fields.Integer(string="Quantity")
    eq_quantity_left = fields.Integer(string="Quantity left")
    eq_product_no = fields.Many2one('product.product', string="Product number")    
    eq_description = fields.Text(string="Description")
    eq_drawing_no = fields.Char(size=100, string="Drawing number")
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'eq_open_sale_order_line')
        cr.execute("""
            CREATE OR REPLACE VIEW eq_open_sale_order_line AS (
            (SELECT MIN(id) as id,
            order_id as eq_order_id,
            eq_agreement_id as eq_framework_agreement_id,
            (select eq_customer_ref from res_partner where id = (select partner_id from sale_order where id = order_id)) as eq_customer_no,
            (select partner_id from sale_order where id = order_id) as eq_customer,
            eq_delivery_date,
            sequence as eq_pos,
            product_uom_qty as eq_quantity,
            (select SUM(product_qty) from stock_move where procurement_id = (select id from procurement_order where sale_line_id = main.id) and state != 'done') as eq_quantity_left,
            product_id as eq_product_no,
            (select description_sale from product_template where id = (select product_tmpl_id from product_product where id = product_id)) as eq_description,
            (select eq_drawing_number from product_template where id = (select product_tmpl_id from product_product where id = product_id)) as eq_drawing_no
            FROM sale_order_line as main
            Group by eq_order_id, eq_agreement_id, eq_customer_no, eq_customer, eq_delivery_date, eq_pos, eq_quantity, eq_product_no, eq_description, eq_drawing_no, main.id))""")