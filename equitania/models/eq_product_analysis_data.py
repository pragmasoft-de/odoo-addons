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


import time
from openerp import models, fields, api, _

class eq_product_analysis_data_master(models.TransientModel):
    
    _name = 'eq.product.analysis.data.master'
    


class eq_product_analysis_data(models.TransientModel):
    
    _name = 'eq.product.analysis.data'
    
    parent_id = fields.Many2one('eq.product.analysis.data.master', string='Parent ID', ondelete='cascade', required=True)
    
    article_number = fields.Char(string="Article number")
    ean = fields.Char(string="EAN")
    article_desc = fields.Char(string="Article description")
    supplier = fields.Char(string="Supplier")
    
    gross_profit = fields.Float(string="Gross profit")
    gross_margin = fields.Float(string="Gross margin")
    #===========================================================================
    # sale_quantity = fields.Float(string="Sale quantity")
    # sale_sum_total = fields.Float(string="Sum total")
    # sale_quantity_prev_year = fields.Float(string="Sale quantity previous year")
    #===========================================================================
    #===========================================================================
    # sale_change = fields.Float(string="Change")
    #===========================================================================
    