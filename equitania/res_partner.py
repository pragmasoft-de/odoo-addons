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
    
    
    eq_delivery_date_type_purchase = fields.Selection([('cw', 'Calendar week'), ('date', 'Date')], string="Delivery Date Purchase", help="If nothing is selected, the default from the settings will be used.")
    eq_delivery_date_type_sale = fields.Selection([('cw', 'Calendar week'), ('date', 'Date')], string="Delivery Date Sale", help="If nothing is selected, the default from the settings will be used.")    
    eq_complete_description = fields.Char(compute='_generate_complete_description', store=True)        
    eq_prospective_customer = fields.Boolean(string="Prospective user",required=False, default=False)
    eq_unlocked_for_webshop = fields.Boolean(string="Unlocked for webshop",required=False, default=False)    
    eq_lead_referred_id = fields.Many2one('eq.lead.referred', 'Referred By') # field extended from eq_lead_referred.py
    eq_foreign_ref = fields.Char('Foreign reference') # field extended from eq_foreign_ref.py
    
    

    @api.model
    def name_get(self):
        """
            Extension of default name_get function
            @return: Name to be displayed
        """
        
        context = self.env.context        
        res = []        
        for record in self:
            name = record.name
            
            if record.parent_id and not record.is_company:
                name =  "%s, %s" % (record.parent_id.name, name)
                
                if record.type == 'contact':
                    name = "%s, %s %s %s" % (record.parent_id.name, (record.title.name if record.title else ''), (record.eq_firstname if record.eq_firstname else ''), record.name)
                    
                if context.get('show_address_only'):
                    name = self._display_address(cr, uid, record, without_company=True, context=context)
                    
                if context.get('show_address'):
                    name = name + "\n" + self._display_address(cr, uid, record, without_company=True, context=context)
            
            name = name.replace('\n\n','\n')
            name = name.replace('\n\n','\n')
            
       
            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            
            res.append((record.id, name))
        
        return res
    
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
                                
    """ method extended from  eq_lead_referred.py  """    
    @api.multi
    def write(self, vals):                
        """
            Override of write function - save customer flag also for each contact
            @vals: values to be set
            @return: super call            
        """
        res_partner_obj = self.env['res.partner'].sudo()
        
        if "customer" in vals:            
            res_partners = res_partner_obj.search([('parent_id', '=', self._ids[0])])
            if res_partners:
                for partner in res_partners:
                    partner.customer = vals["customer"]            
                        
        return super(res_partner, self).write(vals)
        
    """ method extended from eq_address_extension_new_api.py """
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        
        ir_values_obj = self.env['ir.values']
        
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = ['|','|',('name', operator, name),('eq_customer_ref', 'ilike', name),('eq_creditor_ref', 'ilike', name)] + args
        if ir_values_obj.get_default('sale.order', 'default_search_only_company'):
            if self.env.context.has_key('main_address'):
                args += [('is_company', '=', True)]
            elif self.env.context.has_key('default_type'):
                if self.env.context['default_type'] in ['delivery', 'invoice']:
                    args += [('type', '!=', 'contact')]
        elif self.env.context.get('active_model', False) == 'sale.order':
            args = [x for x in args if 'is_company' not in x]
        categories = self.search(args, limit=limit)
        res = categories.name_get()
        
        if self.env.context is None:
            self.env.context = {}
        if self.env.context.has_key('active_model'):
            partner_ids = [r[0] for r in res]
            new_res = []
            
            show_address = ir_values_obj.get_default('sale.order', 'default_show_address')

            for partner_id in self.browse(partner_ids):
                #Company name
                company_name = partner_id.parent_id and partner_id.parent_id.name + ' ; ' or ''
                #Street City
                street = partner_id.street if partner_id.street else ''
                city = partner_id.city if partner_id.city else ''
                #customer/creditor number
                deb_num = ''
                if partner_id.eq_customer_ref != 'False' and partner_id.eq_customer_ref and partner_id.eq_creditor_ref != 'False' and partner_id.eq_creditor_ref:
                    deb_num = '[' + partner_id.eq_customer_ref + '/' + partner_id.eq_creditor_ref + '] '
                elif partner_id.eq_customer_ref != 'False' and partner_id.eq_customer_ref:
                    deb_num = '[' + partner_id.eq_customer_ref + '] '
                elif partner_id.eq_creditor_ref != 'False' and partner_id.eq_creditor_ref:
                    deb_num = '[' + partner_id.eq_creditor_ref + '] '
                if partner_id.is_company:
                    if show_address:
                        new_res.append((partner_id.id, deb_num + company_name + partner_id.name + ' / ' + _('Company') + ' // ' + street + ', ' + city))
                    else:
                        new_res.append((partner_id.id, deb_num + company_name + partner_id.name + ' / ' + _('Company')))
                else:
                    type = partner_id.type
                    if partner_id.type == 'contact':
                        type = _('contact')
                    elif partner_id.type == 'invoice':
                        type = _('invoice')
                    elif partner_id.type == 'delivery':
                        type = _('delivery')
                    elif partner_id.type == 'default':
                        type = _('default')
                    elif partner_id.type == 'other':
                        type = _('other')
                    if show_address:
                        new_res.append((partner_id.id, "%s %s %s %s" % ( deb_num + company_name, (partner_id.title.name if partner_id.title else ''), (partner_id.eq_firstname if partner_id.eq_firstname else ''), partner_id.name + ' / ' + type + ' // ' + street + ', ' + city)))
                    else:
                        new_res.append((partner_id.id, "%s %s %s %s" % ( deb_num + company_name, (partner_id.title.name if partner_id.title else ''), (partner_id.eq_firstname if partner_id.eq_firstname else ''), partner_id.name + ' / ' + type)))
            return new_res
        return res 