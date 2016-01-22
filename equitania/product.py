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
from datetime import datetime
from string import replace
from openerp import SUPERUSER_ID
from openerp.tools.translate import _

from openerp import models, api

class eq_product_product_new_api(models.Model):
    _inherit = "product.product"
    
    eq_custom01 = fields.char(size=64) # added this field from eq_company_custom_fields.py
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self._context.get('eq_filter_prod_sup'):
            partner_id = self._context['eq_partner_id']
            sql_query = """select product_tmpl_id from product_supplierinfo where name = %s""" % (partner_id)
            self._cr.execute(sql_query)
            supplierinfo = self._cr.fetchall()
            product_ids = [x[0] for x in supplierinfo]
            if args == None:
                args = []
            args.append(['id', 'in', product_ids])
        res = super(eq_product_product_new_api, self).name_search(name, args=args, operator=operator, limit=limit)
        return res
    
    
class eq_product_category_custom_fields(models.Model):
    _inherit = 'product.category'
    
    eq_custom01 = fields.char(size=64)
