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

from openerp import http, SUPERUSER_ID
from openerp.http import request

class EqGoogleShoppingFeed(http.Controller):
    
     @http.route('/eq_google_shopping_feed/data_at.txt', auth='public', website=True)
     def index_at(self, **kw):
         """ feed for austria """                          
         return self.generate_file("at")

     @http.route('/eq_google_shopping_feed/data_ch.txt', auth='public', website=True)
     def index_ch(self, **kw):
         """ feed for switzerland """                 
         return self.generate_file("ch")
     
     @http.route('/eq_google_shopping_feed/data_de.txt', auth='public', website=True)
     def index_de(self, **kw):   
         """ feed for germany """              
         # ?db=eqwebsite                
         #ensure_db()
         return self.generate_file("de") 
             
     @http.route('/eq_google_shopping_feed/data_en.txt', auth='public', website=True)
     def index_en(self, **kw):
         """ feed for us """                 
         return self.generate_file("en")
     
     @http.route('/eq_google_shopping_feed/data_gb.txt', auth='public', website=True)
     def index_gb(self, **kw):
         """ feed for uk """                 
         return self.generate_file("gb")
             
     def generate_file(self, contry_code):
         """ generate txt file and send it to client """
                  
         # 1.generate header
         header = self.generate_header()                  
         content = header + "\n\n"
         
         # 2. generate positions
         positions = self.generate_positions(contry_code)
         for position in positions:     
             content += position + "\n"         
         
         mimetype ='application/text;charset=utf-8'
         return http.request.make_response(content)
                  
     def generate_header(self):
         """ generates header for google feed """
         return "id|title|description|google_product_category|product_type|link|image_link|condition|availability|price|brand|mpn|shipping"         

     def set_line_text(self, line, value, placeholder, convert_to_string):
         """ generates line text from oour template """                
         if value is not False:
             if convert_to_string:
                line = line.replace(placeholder, str(value))
             else:
                line = line.replace(placeholder, value)
                
         else:
             line = line.replace(placeholder, "")
        
         return line
    
     def generate_link(self, id):
         """ generates article link """
         return request.httprequest.url_root + "shop/product/" + str(id)                           
     
     def generate_image_link(self, id):
         """ generates image link for our article """                                    
         products = http.request.env['product.product'].search([('product_tmpl_id', '=', id)]),
         product = products[0]         
         for id in product.ids:
             product = http.request.env['product.product'].browse(id)
             if product.image_variant is not None:
                 return request.httprequest.url_root + "website/image/product.product/" + str(id) + "/image"

         return ""
         
     def generate_positions(self, contry_code):
         """ generates position for datarow from db """         
         positions = []         
         products = http.request.env['product.template'].search([('state', '=', 'sellable')])         # original
         #products = http.request.env['product.template'].search([])                                     # new         
         #for id in products[0].ids:                                                                    # original
         for id in products.ids:                                                                        # new         
            product = http.request.env['product.template'].browse(id)
            id = product.id                                                 # id
            title = product.name                                            # titel
            description = product.description_sale                          # description
                        
            if contry_code == 'at' or contry_code == 'ch' or contry_code == 'de':
                google_product_category = "Sportartikel > Sportübungen & Fitness > Krafttrainingsgeräte"    # google_product_category
            elif contry_code == 'en' or contry_code == 'gb':
                google_product_category = "Sporting Goods > Exercise & Fitness > Weightlifting Machines"    # google_product_category
                
            google_product_category = google_product_category.decode('utf-8')
            
            product_type = "todo"                                           # product_type            
            link = self.generate_link(id)                                   # link
            image_link = self.generate_image_link(id)                       # image_link
            condition = "new"                                               # condition
            availability = "in stock"                                       # availability
            price = product.list_price                                      # price            
            brand = "todo"                                                  # brand
            mpn = "todo"                                                    # mpn
            shipping = "DE::Standard:0"                                     # shipping
                        
            # generate lines
            line = "@id|@title|@description|@google_product_category|@product_type|@link|@image_link|@condition|@availability|@price|@brand|@mpn|@shipping"
            line = self.set_line_text(line, id, "@id", True)
            line = self.set_line_text(line, title, "@title", False)
            line = self.set_line_text(line, description, "@description", False)
            line = self.set_line_text(line, google_product_category, "@google_product_category", False)
            line = self.set_line_text(line, product_type, "@product_type", False)
            line = self.set_line_text(line, link, "@link", False)
            line = self.set_line_text(line, image_link, "@image_link", False)
            line = self.set_line_text(line, condition, "@condition", False)
            line = self.set_line_text(line, availability, "@availability", False)
            line = self.set_line_text(line, price, "@price", True)
            line = self.set_line_text(line, brand, "@brand", False)
            line = self.set_line_text(line, mpn, "@mpn", False)
            line = self.set_line_text(line, shipping, "@shipping", False)
            
            positions.append(line)
        
         return positions    