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

from openerp.osv import fields, osv, orm
import openerp.addons.decimal_precision as dp

class eq_info_for_product_product(osv.osv):
    _inherit = "product.product"
    
    _columns = {
        'weight': fields.float('Gross Weight', digits_compute=dp.get_precision('Stock Weight'), help="The gross weight in Kg."),
        'weight_net': fields.float('Net Weight', digits_compute=dp.get_precision('Stock Weight'), help="The net weight in Kg."),
        'volume': fields.float('Volume', help="The volume in m3."),
        'seller_ids': fields.one2many('product.supplierinfo', 'product_tmpl_id', 'Supplier'),
        'seller_delay': fields.related('seller_ids','delay', type='integer', string='Supplier Lead Time',
            help="This is the average delay in days between the purchase order confirmation and the receipts for this product and for the default supplier. It is used by the scheduler to order requests based on reordering delays."),
        'seller_qty': fields.related('seller_ids','qty', type='float', string='Supplier Quantity',
            help="This is minimum quantity to purchase from Main Supplier."),
        'seller_id': fields.related('seller_ids','name', type='many2one', relation='res.partner', string='Main Supplier',
            help="Main Supplier who has highest priority in Supplier List."),

    }