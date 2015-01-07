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
from openerp import tools

class eq_wizard_valuation_history(osv.osv_memory):
    _inherit = 'wizard.valuation.history'
    
    def open_table(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, context=context)[0]
        ctx = context.copy()
        ctx['history_date'] = data['date']
        ctx['search_default_group_by_product'] = True
        ctx['search_default_group_by_location'] = False
        return {
            'domain': "[('date', '<=', '" + data['date'] + "')]",
            'name': _('Stock Value At Date'),
            'view_type': 'form',
            'view_mode': 'tree,graph',
            'res_model': 'stock.history',
            'type': 'ir.actions.act_window',
            'context': ctx,
        }

class eq_stock_history(osv.osv):
    _inherit = 'stock.history'
    
    _columns = {
                'eq_uom_name': fields.char(string='Unit', readonly=True),
                'eq_lst_price': fields.float(string='Price per Unit (Sale)', readonly=True),
                'price_unit_on_quant': fields.float('Price per Unit (Purchase)', digits_compute=dp.get_precision('Product Price')),
                }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'stock_history')
        cr.execute("""
            CREATE OR REPLACE VIEW stock_history AS (
              SELECT MIN(id) as id,
                move_id,
                location_id,
                company_id,
                product_id,
                product_categ_id,
                SUM(quantity) as quantity,
                date,
                price_unit_on_quant,
                source,
        eq_lst_price,
        (SELECT name FROM product_uom WHERE id = uom_id) as eq_uom_name
                FROM
                ((SELECT
                    stock_move.id::text || '-' || quant.id::text AS id,
                    quant.id AS quant_id,
                    stock_move.id AS move_id,
                    dest_location.id AS location_id,
                    dest_location.company_id AS company_id,
                    stock_move.product_id AS product_id,
                    product_template.categ_id AS product_categ_id,
                    quant.qty AS quantity,
                    stock_move.date AS date,
                    quant.cost as price_unit_on_quant,
                    stock_move.origin AS source,
            product_template.list_price as eq_lst_price,
            product_template.uom_id as uom_id
                FROM
                    stock_quant as quant, stock_quant_move_rel, stock_move
                LEFT JOIN
                   stock_location dest_location ON stock_move.location_dest_id = dest_location.id
                LEFT JOIN
                    stock_location source_location ON stock_move.location_id = source_location.id
                LEFT JOIN
                    product_product ON product_product.id = stock_move.product_id
                LEFT JOIN
                    product_template ON product_template.id = product_product.product_tmpl_id
                WHERE stock_move.state = 'done' AND dest_location.usage in ('internal', 'transit') AND stock_quant_move_rel.quant_id = quant.id
                AND stock_quant_move_rel.move_id = stock_move.id AND ((source_location.company_id is null and dest_location.company_id is not null) or
                (source_location.company_id is not null and dest_location.company_id is null) or source_location.company_id != dest_location.company_id)
                ) UNION
                (SELECT
                    '-' || stock_move.id::text || '-' || quant.id::text AS id,
                    quant.id AS quant_id,
                    stock_move.id AS move_id,
                    source_location.id AS location_id,
                    source_location.company_id AS company_id,
                    stock_move.product_id AS product_id,
                    product_template.categ_id AS product_categ_id,
                    - quant.qty AS quantity,
                    stock_move.date AS date,
                    quant.cost as price_unit_on_quant,
                    stock_move.origin AS source,
            product_template.list_price as eq_lst_price,
            product_template.uom_id as uom_id
                FROM
                    stock_quant as quant, stock_quant_move_rel, stock_move
                LEFT JOIN
                    stock_location source_location ON stock_move.location_id = source_location.id
                LEFT JOIN
                    stock_location dest_location ON stock_move.location_dest_id = dest_location.id
                LEFT JOIN
                    product_product ON product_product.id = stock_move.product_id
                LEFT JOIN
                    product_template ON product_template.id = product_product.product_tmpl_id
                WHERE stock_move.state = 'done' AND source_location.usage in ('internal', 'transit') AND stock_quant_move_rel.quant_id = quant.id
                AND stock_quant_move_rel.move_id = stock_move.id AND ((dest_location.company_id is null and source_location.company_id is not null) or
                (dest_location.company_id is not null and source_location.company_id is null) or dest_location.company_id != source_location.company_id)
                ))
                AS foo
                GROUP BY move_id, location_id, company_id, product_id, product_categ_id, date, price_unit_on_quant, source, eq_lst_price, uom_id
            )""")