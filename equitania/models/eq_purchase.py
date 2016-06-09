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

class eq_open_purchase_order(models.Model):
    _inherit = "purchase.order"
    
    eq_filter_prod_sup = fields.Boolean()

class eq_open_purchase_order_line(models.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    
    @api.one
    @api.depends('order_id.partner_ref')
    def eq_compute_purchase_supplier_ref(self):
        if self.order_id :
            self.eq_purchase_supplier_order_ref = self.order_id.partner_ref
    
    @api.one
    @api.depends('order_id')
    def eq_compute_sequence(self):
        if self.order_id :
            self.eq_sequence = self.order_id.id
    
    @api.one
    @api.depends('partner_id.eq_creditor_ref')
    def eq_compute_supplier_nos(self):
        if self.partner_id :
            self.eq_supplier_no = self.partner_id.eq_creditor_ref
            
    def eq_search_supplier_nos(self, operator, operand):
        sql_query = """select
            id
        from
            purchase_order_line
        where
            order_id in (
                select 
                    id 
                from 
                    purchase_order 
                where 
                    partner_id in (
                        select 
                            id 
                        from 
                            res_partner 
                        where 
                            eq_creditor_ref %s '%s%s%s'
                        )
                )"""
                
        search_ext = "%%" if operator in ("like", "ilike") else ""
        sql_query = sql_query % (operator, search_ext, operand, search_ext)
        self._cr.execute(sql_query)
        query_result = self._cr.fetchall()
        order_line_ids = [x[0] for x in query_result]
        domain = [('id', 'in', order_line_ids)]
        return domain
    
    @api.one
    @api.depends('product_id.product_tmpl_id.eq_drawing_number')
    def eq_compute_product_tmpl_drawing_nos(self):
        if self.partner_id :
            self.eq_drawing_number = self.product_id.product_tmpl_id.eq_drawing_number
            
            
    @api.one
    @api.depends('move_ids.state')
    def eq_compute_qty_left(self):
        if self.move_ids :
            count = 0
            stock_move_ids = []
            stock_move_ids = self.env['stock.move'].search([('purchase_line_id','in',[self.id]),('state','not in',['done','cancel'])])
            for res in  stock_move_ids:
                count += res.product_qty
            self.eq_qty_left = count
    
    eq_purchase_supplier_order_ref = fields.Char(string="Supplier Order Reference", readonly=True, store=True, compute='eq_compute_purchase_supplier_ref')
    eq_supplier_no = fields.Char(string="Supplier No", readonly=True, store=False, compute='eq_compute_supplier_nos', search="eq_search_supplier_nos")
    eq_drawing_number = fields.Char(string="Drawing number", readonly=True, store=True, compute='eq_compute_product_tmpl_drawing_nos')
    eq_sequence = fields.Integer(string="Seq", readonly= True, store=True, compute='eq_compute_sequence')
    eq_qty_left = fields.Float(string="Quantity left", readonly=True, store=True, compute="eq_compute_qty_left")
    