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
    eq_condition = fields.Selection([('new', 'New'),('refurbished', 'Refurbished'),('used','Used')], default='new')
    
    #Preise und Verfügbarkeit
    eq_available_date = fields.Date('Release Date')
    eq_special_offer_price = fields.Float('Special Offer Price')
    eq_special_offer_period = fields.Date('Special Offer Period')
    
    eq_google_product_category = fields.Char('Google Product Category')
    
    taxonomy_id = fields.Many2one('google.product.taxonomy', 
                                   'Taxonomy Search', 
                                   required=False)
    
    
    @api.onchange('taxonomy_id')
    def onchange_taxonomy_id(self): 
# Feld "eq_google_product_category" wird mit dem Namen der Kategorie befüllt   
#         name = str(self.taxonomy_id.name)
#         taxonomy_name = name.split(']')
#         self.eq_google_product_category = taxonomy_name[1]

# Feld "eq_google_product_category" wird mit dem Code der Kategorie befüllt   
# Ausgabe des Codes im XML-Feed (bessere Formatierung)
        name = self.taxonomy_id.name
        if name != False:
            taxonomy_name = name.split('[')
            taxonomy = taxonomy_name[1].split(']')
            self.eq_google_product_category = taxonomy[0]
        
        
class eq_google_product_attribute(models.Model):
    _inherit = "product.attribute"
    
    
    eq_google_attribute = fields.Selection([('color', 'Color'),('gender', 'Gender'),('age_group','Age Group'),('material','Material'),('pattern','Pattern'),('size','Size')])

    

