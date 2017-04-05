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
    _order = 'eq_delivery_date'
    _rec_name = 'eq_product_no'
    
    # Felder
    eq_order_id = fields.Many2one('sale.order', string="Sale Order")
    eq_client_order_ref = fields.Char(string="Client Order Reference")
    eq_customer_no = fields.Char(size=64, string="Customer No")
    eq_customer = fields.Many2one('res.partner', string="Customer")    
    eq_delivery_date = fields.Date(string="Delivery date")
    #eq_pos = fields.Integer(string="Seq")
    eq_quantity = fields.Integer(string="Quantity")
    eq_quantity_left = fields.Integer(string="Quantity left")
    eq_product_no = fields.Many2one('product.product', string="Product number")
    eq_drawing_no = fields.Char(size=100, string="Drawing number")
    
    eq_state = fields.Selection(
                [('cancel', 'Cancelled'),('draft', 'Draft'),('confirmed', 'Confirmed'),('exception', 'Exception'),('done', 'Done')],
                'Status')
    
    
    
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'eq_open_sale_order_line')
        cr.execute("""
        CREATE OR REPLACE VIEW eq_open_sale_order_line AS (
            SELECT 
                --min(main.id) AS id,
                row_number() over (order by main.order_id nulls last) as id,
                main.order_id AS eq_order_id,
                (
                    SELECT
                        sale_order.client_order_ref
                    FROM
                        sale_order
                    WHERE
                        sale_order.id = main.order_id
                ) AS eq_client_order_ref,
                (
                    SELECT
                        res_partner.eq_customer_ref
                    FROM
                        res_partner
                    WHERE res_partner.id = (
                        SELECT
                            sale_order.partner_id
                        FROM
                            sale_order
                        WHERE
                            sale_order.id = main.order_id
                        )
                ) AS eq_customer_no,
                (
                    SELECT
                        sale_order.partner_id
                    FROM
                        sale_order
                    WHERE
                        sale_order.id = main.order_id
                ) AS eq_customer,
                main.eq_delivery_date,
                --main.sequence AS eq_pos,
                (select sum(line2.product_uom_qty) from sale_order_line line2 where line2.order_id = main.order_id and line2.product_id = main.product_id) AS eq_quantity,
                --re.Qleft  as eq_quantity_left,
                (select case when count(sm2.*) = 0 then (select sum(line2.product_uom_qty) from sale_order_line line2 where line2.order_id = main.order_id and line2.product_id = main.product_id)
                else (select sum(SM.product_qty) from stock_move SM
		 join stock_picking sp on sp.id = sm.picking_id
		 where sp.eq_sale_order_id = main.order_id
		 and sm.state::text <> 'done'::text AND sm.state::text <> 'cancel'::text and sm.picking_id IS NOT NULL
		 and sm.product_id = main.product_id)
                end)
                as eq_quantity_left,

                main.product_id AS eq_product_no,
                (
                    SELECT
                        product_template.eq_drawing_number
                    FROM
                        product_template
                    WHERE
                        product_template.id = (
                            SELECT
                                product_product.product_tmpl_id
                            FROM
                                product_product
                            WHERE
                                product_product.id = main.product_id
                            )
                ) AS eq_drawing_no,
                main.state AS eq_state

            FROM
                sale_order_line main

                left outer join stock_picking sp on (sp.eq_sale_order_id = main.order_id and sp.state not in ('cancel','done'))
                left outer join stock_move sm2 on (sm2.picking_id = sp.id and main.product_id = sm2.product_id)
                --left outer join stock_move sm on (sm.picking_id = sp.id and main.product_id = sm.product_id
                --and sm.state::text <> 'done'::text AND sm.state::text <> 'cancel'::text and sm.picking_id IS NOT NULL)
		--where main.order_id = 15966
            GROUP BY
                main.order_id,
                (
                    SELECT
                        sale_order.client_order_ref
                    FROM
                        sale_order
                    WHERE
                        sale_order.id = main.order_id
                ),
                (
                    SELECT
                        res_partner.eq_customer_ref
                    FROM
                        res_partner
                    WHERE
                        res_partner.id = (
                            SELECT
                                sale_order.partner_id
                            FROM
                                sale_order
                            WHERE
                                sale_order.id = main.order_id
                            )
                ),
                (
                    SELECT
                        sale_order.partner_id
                    FROM
                        sale_order
                    WHERE
                        sale_order.id = main.order_id
                ),
                main.eq_delivery_date,
                --main.product_uom_qty ,
                main.product_id,
                (
                    SELECT
                        product_template.eq_drawing_number
                    FROM
                        product_template
                    WHERE
                        product_template.id = (
                            SELECT
                                product_product.product_tmpl_id
                            FROM
                                product_product
                            WHERE
                                product_product.id = main.product_id)
                ),
                 main.state
        )
            """)



    #
    # def init(self, cr):
    #     tools.drop_view_if_exists(cr, 'eq_open_sale_order_line')
    #     cr.execute("""
    #     CREATE OR REPLACE VIEW eq_open_sale_order_line AS (
    #         SELECT
    #             min(main.id) AS id,
    #             main.order_id AS eq_order_id,
    #             (
    #                 SELECT
    #                     sale_order.client_order_ref
    #                 FROM
    #                     sale_order
    #                 WHERE
    #                     sale_order.id = main.order_id
    #             ) AS eq_client_order_ref,
    #             (
    #                 SELECT
    #                     res_partner.eq_customer_ref
    #                 FROM
    #                     res_partner
    #                 WHERE res_partner.id = (
    #                     SELECT
    #                         sale_order.partner_id
    #                     FROM
    #                         sale_order
    #                     WHERE
    #                         sale_order.id = main.order_id
    #                     )
    #             ) AS eq_customer_no,
    #             (
    #                 SELECT
    #                     sale_order.partner_id
    #                 FROM
    #                     sale_order
    #                 WHERE
    #                     sale_order.id = main.order_id
    #             ) AS eq_customer,
    #             main.eq_delivery_date,
    #             main.sequence AS eq_pos,
    #             main.product_uom_qty AS eq_quantity,
    #             re.Qleft  as eq_quantity_left,
    #             main.product_id AS eq_product_no,
    #             (
    #                 SELECT
    #                     product_template.eq_drawing_number
    #                 FROM
    #                     product_template
    #                 WHERE
    #                     product_template.id = (
    #                         SELECT
    #                             product_product.product_tmpl_id
    #                         FROM
    #                             product_product
    #                         WHERE
    #                             product_product.id = main.product_id
    #                         )
    #             ) AS eq_drawing_no,
    #             main.state AS eq_state
    #
    #         FROM
    #             sale_order_line main
    #         LEFT JOIN
    #             (
    #                 SELECT
    #                     sum(SM.product_qty) AS Qleft,
    #                     sale_line_id
    #                 FROM
    #                     procurement_order PO left join stock_move SM on PO.id =  SM.procurement_id
    #                 WHERE
    #                     SM.state::text <> 'done'::text AND SM.state::text <> 'cancel'::text and SM.picking_id IS NOT NULL
    #                     AND PO.state = 'running' AND PO.partner_dest_id IS NOT NULL
    #                 GROUP BY sale_line_id
    #             )
    #             re on  re .sale_line_id=main.id
    #         GROUP BY
    #             main.order_id,re.Qleft,
    #             (
    #                 SELECT
    #                     sale_order.client_order_ref
    #                 FROM
    #                     sale_order
    #                 WHERE
    #                     sale_order.id = main.order_id
    #             ),
    #             (
    #                 SELECT
    #                     res_partner.eq_customer_ref
    #                 FROM
    #                     res_partner
    #                 WHERE
    #                     res_partner.id = (
    #                         SELECT
    #                             sale_order.partner_id
    #                         FROM
    #                             sale_order
    #                         WHERE
    #                             sale_order.id = main.order_id
    #                         )
    #             ),
    #             (
    #                 SELECT
    #                     sale_order.partner_id
    #                 FROM
    #                     sale_order
    #                 WHERE
    #                     sale_order.id = main.order_id
    #             ),
    #             main.eq_delivery_date,
    #             main.sequence ,
    #             main.product_uom_qty ,
    #             main.product_id,
    #             (
    #                 SELECT
    #                     product_template.eq_drawing_number
    #                 FROM
    #                     product_template
    #                 WHERE
    #                     product_template.id = (
    #                         SELECT
    #                             product_product.product_tmpl_id
    #                         FROM
    #                             product_product
    #                         WHERE
    #                             product_product.id = main.product_id)
    #             ),
    #              main.state,
    #              main.id
    #     )
    #         """)