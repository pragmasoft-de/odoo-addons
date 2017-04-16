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
    
class eq_product_ul(models.Model):
    _name = "product.ul"
    _inherit = "product.ul"
    
    _description = "Logistic Unit"
    
    
    @api.model
    def create(self,values):
        if values.has_key('height'):
            if values.get('height') * values.get('width') * values.get('length') <= 0 :
                raise osv.except_osv(_('Error!'), _('Please provide Valid Logistic Unit'))
            
        return super(eq_product_ul, self).create(values)
    
    
    
    @api.multi
    def write(self, vals):
        if vals:
            if vals.get('height') <= 0 and vals.has_key('height') :
                raise osv.except_osv(_('Error!'), _('Please provide Valid Logistic Unit'))
            
            if vals.get('width') <= 0  and vals.has_key('width') :
                raise osv.except_osv(_('Error!'), _('Please provide Valid Logistic Unit'))
            
            if vals.get('length') <= 0  and vals.has_key('length'):
                raise osv.except_osv(_('Error!'), _('Please provide Valid Logistic Unit'))
        
        return super(eq_product_ul, self).write(vals)
    

