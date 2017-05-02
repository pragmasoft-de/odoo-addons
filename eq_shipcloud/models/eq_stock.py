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


class eq_stock_package(models.Model):

    _name = "stock.quant.package"
    _inherit = "stock.quant.package"
    
    @api.model
    def eq_get_default_ul_id(self):
        logistic_data = self.env['eq.shipdefault.logistic.unit'].search([]).eq_def_logistic_unit.ids[0]
        return logistic_data
    
    eq_is_processed = fields.Boolean(readonly=False, default=False, copy=False,string='Is Processed',
        help="Denotes whether the package is processed through barcode symbol or not.")
    ul_id = fields.Many2one(default=eq_get_default_ul_id)

    @api.one
    @api.depends('eq_source_pack_delivery.eq_weight_net',\
                 'eq_desi_pack_delivery.eq_weight_net','ul_id.weight')
    def _compute_cal(self):
        weight_net = 0
        gross_weight = 0
        if self.eq_source_pack_delivery or self.eq_desi_pack_delivery :
            for src in self.eq_source_pack_delivery:
                weight_net += src.eq_weight_net
                gross_weight += src.eq_gross_weight
            for des in self.eq_desi_pack_delivery:
                weight_net += des.eq_weight_net
                gross_weight += des.eq_gross_weight
        self.eq_weight_net = weight_net + self.ul_id.weight
        self.eq_gross_weight = gross_weight + self.ul_id.weight
            
     
    eq_source_pack_delivery = fields.One2many('stock.pack.operation','package_id',string='Source Package Delivery')
    eq_desi_pack_delivery = fields.One2many('stock.pack.operation','result_package_id',string='Destination Package Delivery')
    eq_weight_net = fields.Float(string='Package Net weight',readonly=True,store=True,compute='_compute_cal')  
    eq_gross_weight = fields.Float(string='Package Gross weight',readonly=False,store=True,compute='_compute_cal')
    eq_logistic_unit = fields.Char(string="Web display Logistic", related='ul_id.name',help='This field display on website picking window')
    eq_gross_weight_changed = fields.Float('Updated Gross weight')
    
class eq_stock_picking(models.Model):

    _name = "stock.picking"
    _inherit = ['stock.picking']
    
    eq_is_shipped = fields.Boolean(readonly=False, default=False, copy=False,string='Is Shipped',
        help="Denotes whether the delivery order is shipped or not.")
    eq_state = fields.Selection([('eq_shipment_error', 'Shipment Error'), ], 
        string='Shipment State',readonly=True, select=True, copy=False, help="It specifies error in creating shipments")
    eq_is_processed = fields.Boolean(readonly=False, default=False, copy=False,string='Is Processed',
        help="Denotes whether the delivery order is processed or not.")
    eq_is_symbol_transfer = fields.Boolean(readonly=False, default=False, copy=False,string='Is Symbol transfer')
    eq_reason = fields.Text('Exception Reason',copy=False,readonly=True)

    @api.v7
    def action_done_from_ui(self, cr, uid, picking_id, context=None):
        """ 
            Inherited the existing method()
            called when button 'done' is pushed in the barcode scanner UI 
        """
        if not picking_id:
            return {}
        data={}
        is_shipcloud = False
        eq_shipcloud_obj = self.pool.get('eq.shipcloud')
        pack_op_obj = self.pool.get('stock.pack.operation')
        stock_picking_data = self.browse(cr,uid,picking_id,context=context)
        
        for operation in stock_picking_data.pack_operation_ids:
            pack_op_obj.write(cr, uid, operation.id, {'product_qty': operation.qty_done}, context=context)
        res = self.do_transfer(cr, uid, [picking_id], context=context)
        
        #Check the condition, to avoid creating duplicate shipments
        if res and stock_picking_data.eq_is_shipped == False and not stock_picking_data.eq_state == 'eq_shipment_error' \
        and stock_picking_data.eq_is_processed == False:
            result = eq_shipcloud_obj.eq_create_shipments(cr,uid,picking_id,context=None)
            
            #If the condition is true, shipment will be created
            if result:
                is_shipcloud = eq_shipcloud_obj.eq_create_shipcloud(cr,uid,result,context=None)
            
            if not is_shipcloud or not result:
                #current transaction be rollback
                cr.rollback()
                self.action_cancel(cr, uid, picking_id, context=None)
                self.write(cr,uid,picking_id,{'eq_state': 'eq_shipment_error','eq_reason': "CODE " +str(result[0].get('response').status_code )+ ": " + result[0].get('response').reason},context=None)
                cr.commit()
        self.write(cr,uid,picking_id,{'eq_is_symbol_transfer':True},context=None)
        return self.get_next_picking_for_ui(cr, uid, context=context)

class eq_stock_pack_operation(models.Model):
    _name = "stock.pack.operation"
    _inherit = "stock.pack.operation"
    
    @api.one
    @api.depends('product_id','product_qty','result_package_id','package_id')
    def _compute_cal(self):
        if self.result_package_id or self.package_id :
            self.eq_weight_net = self.product_qty * self.product_id.weight_net
            self.eq_gross_weight = self.product_qty * self.product_id.weight_net
    
    
    picking_id = fields.Many2one(string="Delivery Order") #overriden the field label name
    eq_weight_net = fields.Float(string='Net weight',readonly=True,store=True,compute='_compute_cal')  
    eq_gross_weight = fields.Float(string='Gross weight',readonly=False,store=True,compute='_compute_cal')
