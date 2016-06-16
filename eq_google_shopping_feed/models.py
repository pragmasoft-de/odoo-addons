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

# definition of your tables and fields goes here

from openerp import models, fields, api

# class eq_website_template(models.Model):
#     _name = 'eq_website_template.eq_website_template'

#     name = fields.Char()

class eq_google_product_product(models.Model):
    _inherit = "product.template"
    
    #Allgemeine Attribute
    eq_google_product_category = fields.Char('Google Product Category')
    eq_condition = fields.Selection([('new', 'New'),('renewed', 'Renewed'),('secondhand','Secondhand')], default='new')
    
    #Preise und Verfügbarkeit
    eq_available_date = fields.Date('Release Date')
    eq_special_offer_price = fields.Float('Special Offer Price')
    eq_special_offer_period = fields.Date('Special Offer Period')

