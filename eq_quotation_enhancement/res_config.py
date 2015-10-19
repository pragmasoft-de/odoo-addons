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

class eq_sale_config_settings(osv.osv_memory):
    _inherit = 'sale.config.settings'
    
    def set_default_template_id(self, cr, uid, ids, context=None):
        ir_values = self.pool.get('ir.values')
        config = self.browse(cr, uid, ids[0], context)
        ir_values.set_default(cr, uid, 'sale.order', 'template_id', config.default_template_id.id)
        
    def get_default_template_id(self, cr, uid, fields, context=None):
        ir_values = self.pool.get('ir.values')
        default_template_id = ir_values.get_default(cr, uid, 'sale.order', 'template_id')
        return {
                'default_template_id': default_template_id,
                }
    
    _columns = {
                'default_template_id': fields.many2one('sale.quote.template', 'Default quotation template [eq_quotation_enhancement]', help="Default the quotation template which will be used in every new quotation.")
                }
    
    