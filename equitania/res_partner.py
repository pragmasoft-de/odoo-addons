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

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def _address_fields(self):
        res = super(res_partner, self)._address_fields()
        res.extend(("eq_house_no", "eq_citypart"))
        return res
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """ name_search(name='', args=None, operator='ilike', limit=100) -> records

        Search for records that have a display name matching the given
        ``name`` pattern when compared with the given ``operator``, while also
        matching the optional search domain (``args``).

        This is used for example to provide suggestions based on a partial
        value for a relational field. Sometimes be seen as the inverse
        function of :meth:`~.name_get`, but it is not guaranteed to be.

        This method is equivalent to calling :meth:`~.search` with a search
        domain based on ``display_name`` and then :meth:`~.name_get` on the
        result of the search.
        
        Extends the original method!!!
        If eq_filter_prod_sup in the context is true, then only the suppliers
        which sell all of the products from the purchase order lines 
        (eq_order_line in context) are returned.

        :param str name: the name pattern to match
        :param list args: optional search domain (see :meth:`~.search` for
                          syntax), specifying further restrictions
        :param str operator: domain operator for matching ``name``, such as
                             ``'like'`` or ``'='``.
        :param int limit: optional max number of records to return
        :rtype: list
        :return: list of pairs ``(id, text_repr)`` for all matching records.
        """
        if self._context.get('eq_filter_prod_sup') and self._context.get('eq_order_line'):
            product_ids = []
            purchase_line_obj = self.env['purchase.order.line']
            for line_data in self._context.get('eq_order_line'):
                if line_data[0] == 6:
                    product_ids.append(line_data[2]['product_id'])
                elif line_data[0] == 4:
                    purchase_order_line = purchase_line_obj.browse(line_data[1])
                    product_ids.append(purchase_order_line.product_id.id)
                elif line_data[0] == 1:
                    if 'product_id' in line_data[2]:
                        product_ids.append(line_data[2]['product_id'])
                    else:
                        purchase_order_line = purchase_line_obj.browse(line_data[1])
                        product_ids.append(purchase_order_line.product_id.id)
            
            if product_ids:
                sql_query = """select product_tmpl_id, name from product_supplierinfo where product_tmpl_id in %s""" % (str(tuple(product_ids)))
                self._cr.execute(sql_query)
                supplierinfo = self._cr.fetchall()
                
                prod_sup_mapping = {}
                
                for product_id, sup_id in supplierinfo:
                    if sup_id in prod_sup_mapping:
                        prod_sup_mapping[sup_id].append(product_id)
                    else:
                        prod_sup_mapping[sup_id] = [product_id]
                        
                suppliers = []
                for supplier_id, prod_list in prod_sup_mapping.iteritems():
                    if set(product_ids) <= set(prod_list):
                        suppliers.append(supplier_id)
                    
                if args == None:
                    args = []
                args.append(['id', 'in', suppliers])
        res = super(res_partner, self).name_search(name, args=args, operator=operator, limit=limit)
        return res

    def _sale_quotation_count(self):
        # The current user may not have access rights for sale orders
        for partner in self:
            partner.eq_sale_quotation_count = len(partner.sale_order_ids.filtered(lambda record: record.state in ('draft', 'sent', 'cancel'))) + len(partner.mapped('child_ids.sale_order_ids').filtered(lambda record: record.state in ('draft', 'sent', 'cancel')))
            partner.sale_order_count = len(partner.sale_order_ids.filtered(lambda record: record.state not in ('draft', 'sent', 'cancel'))) + len(partner.mapped('child_ids.sale_order_ids').filtered(lambda record: record.state not in ('draft', 'sent', 'cancel')))

    
    eq_delivery_date_type_purchase = fields.Selection([('cw', 'Calendar week'), ('date', 'Date')], string="Delivery Date Purchase", help="If nothing is selected, the default from the settings will be used.")
    eq_delivery_date_type_sale = fields.Selection([('cw', 'Calendar week'), ('date', 'Date')], string="Delivery Date Sale", help="If nothing is selected, the default from the settings will be used.")    
    eq_complete_description = fields.Char(compute='_generate_complete_description', store=True)    
    
    eq_prospective_customer = fields.Boolean(string="Prospective user",required=False, default=False)
    eq_unlocked_for_webshop = fields.Boolean(string="Unlocked for webshop",required=False, default=False)
    eq_sale_quotation_count = fields.Integer(compute="_sale_quotation_count", string='# of Quotations')
    sale_order_count = fields.Integer(compute="_sale_quotation_count", string='# of Orders')
    
    
    @api.one
    @api.depends('name', 'eq_firstname')
    def _generate_complete_description(self):
        for record in self:
            if record.is_company is False:
                result = ""
                if record.name is not False:
                    result = record.name
                    
                if record.eq_firstname is not False:
                    if len(result) > 0:
                        result += ", " + record.eq_firstname 
                    else:
                        result = record.eq_firstname

                record.eq_complete_description = result  
            else:
                record.eq_complete_description = record.name
                
    
    @api.onchange('title', 'name', 'lang')
    def onchange_title_to_letter_salutation(self):
        
        title = self.title.name
        name = self.name
        lang = self.lang
    
        if lang == 'de_DE':   
            if title and name:
                if title == 'Frau' or title == 'Frl.':
                    self.eq_letter_salutation = 'Sehr geehrte ' + title + " " + name + ","
                else:
                    self.eq_letter_salutation = 'Sehr geehrter ' + title + " " + name + ","
            elif title is False and name is False:
                salutation= 'Sehr geehrte Damen und Herren,'
                self.eq_letter_salutation = salutation
            elif title is False and name: 
                salutation= 'Sehr geehrte Damen und Herren,'
                self.eq_letter_salutation = salutation
            elif title and name is False:
                if title == 'Frau' or title == 'Frl.':
                    self.eq_letter_salutation = 'Sehr geehrte ' + title + ","
                else:
                    self.eq_letter_salutation = 'Sehr geehrter ' + title + ","
        elif self.lang == 'en_US':
            self.eq_letter_salutation = "Dear " 

        
        