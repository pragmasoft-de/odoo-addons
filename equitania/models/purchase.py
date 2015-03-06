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


class purchase_order(models.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    eq_supplier_order_ref = fields.Char('Reference/Description')




class purchase_order_line(models.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    
    @api.one
    @api.depends('order_id.eq_supplier_order_ref')
    def _compute_purchase_supplier_ref(self):
        if self.order_id :
            self.eq_purchase_supplier_order_ref = self.order_id.eq_supplier_order_ref
    
    @api.one
    @api.depends('order_id')
    def _compute_sequence(self):
        if self.order_id :
            self.eq_sequence = self.order_id.id
    
    @api.one
    @api.depends('partner_id.eq_customer_ref')
    def _compute_supplier_nos(self):
        if self.partner_id :
            self.eq_supplier_no = self.partner_id.eq_customer_ref
    
    @api.one
    @api.depends('product_id.product_tmpl_id.eq_drawing_number')
    def _compute_product_tmpl_drawing_nos(self):
        if self.partner_id :
            self.eq_drawing_number = self.product_id.product_tmpl_id.eq_drawing_number
            
            
    @api.one
    @api.depends('procurement_ids')
    def _compute_qty_left(self):
        if self.procurement_ids :
            count = 0
            procurement_order_ids = self.env['procurement.order'].search([('purchase_line_id','=', self.id)])
            stock_move_obj = self.env['stock.move']
            stock_move_ids = stock_move_obj.search([('procurement_id','in',[procurement_order_ids.id]),('state','not in',['done','cancel'])])
            for res in  stock_move_obj.browse(stock_move_ids):
                count += res.product_qty
            self.eq_quantity_left = count
    
    eq_purchase_supplier_order_ref = fields.Char(string="Supplier Order Reference",readonly= True, store= True,compute='_compute_purchase_supplier_ref')
    eq_supplier_no = fields.Char(string="Supplier No",readonly= True, store= True,compute='_compute_supplier_nos')
    eq_drawing_number = fields.Char(string="Drawing number",readonly= True, store= True,compute='_compute_product_tmpl_drawing_nos')
    eq_sequence = fields.Integer(string="Seq",readonly= True, store= True, compute='_compute_sequence')
    eq_quantity_left = fields.Integer(string="Quantity left", readonly=True,store=True,compute="_compute_qty_left")