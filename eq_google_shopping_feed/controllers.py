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
    
     @http.route('/eq_google_shopping_feed/data_at.xml', auth='public', website=True)
     def index_at(self, **kw):
         """ feed for austria """                          
         return self.generate_file("at")

     @http.route('/eq_google_shopping_feed/data_ch.xml', auth='public', website=True)
     def index_ch(self, **kw):
         """ feed for switzerland """                 
         return self.generate_file("ch")
     
     @http.route('/eq_google_shopping_feed/data_de.xml', auth='public', website=True)
     def index_de(self, **kw):   
         """ feed for germany """              
         # ?db=eqwebsite                
         #ensure_db()
         return self.generate_file("de") 
             
     @http.route('/eq_google_shopping_feed/data_en.xml', auth='public', website=True)
     def index_en(self, **kw):
         """ feed for us """                 
         return self.generate_file("en")
     
     @http.route('/eq_google_shopping_feed/data_gb.xml', auth='public', website=True)
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
         
         content += self.generate_footer()
        
         
         
         """
         return request.make_response(content,{
            'Cache-Control': 'no-cache', 
            'Content-Type': 'text/xml; charset=utf-8',
            'Access-Control-Allow-Origin':  '*',
            'Access-Control-Allow-Methods': 'GET',
            })
        """
        
         return request.make_response(content,{
            'Cache-Control': 'no-cache', 
            'Content-Type': 'text/xml; charset=utf-8',
            })
         
        
                  
     def generate_header(self):
         """ generates header for google feed """
         xmlTemplate ="""<?xml version="1.0"?>
    <feed xmlns="http://www.w3.org/2005/Atom" xmlns:g="http://base.google.com/ns/1.0">
        <title>Example - Online Store</title>
        <link rel="self" href="http://www.example.com"/>
        <updated>20011-07-11T12:00:00Z</updated> 
         """
         #return "id|title|description|google_product_category|product_type|link|image_link|condition|availability|price|brand|mpn|shipping"      
         return xmlTemplate  
     
     def generate_footer(self):
         """ generates header for google feed """
         xmlTemplate ="""</feed>
         """      
         return xmlTemplate  

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
         #products = http.request.env['product.template'].search([('state', '=', 'sellable')])         # original
         #sql = "SELECT id FROM product_template where state = 'sellable'"
         
         sql = "SELECT id FROM product_template where website_published = True"
         http.request.env.cr.execute(sql)
         products = http.request.env.cr.fetchall()                
         
         #products = http.request.env['product.template'].search([('website_published', '=', True)])                                     # new      
         #for id in products[0].ids:                                                                    # original
         for id in products:                                                                        # new         
            product = http.request.env['product.template'].sudo().browse(id)
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
            
            
            #product_product = http.request.env['product.product'].sudo().search([('product_tmpl_id', '=', id)])
            #gtin = product_product.ean13                                    #GTIN
            
                        
            # generate lines
            #line = "@id|@title|@description|@google_product_category|@product_type|@link|@image_link|@condition|@availability|@price|@brand|@mpn|@shipping"
            line = """<entry>\n"""
            #line += """<g:id>"""+str(id)+"""</g:id>\n"""
            
            line += """<g:id>[ID]</g:id>\n"""          
            line = line.replace("[ID]", str(id))
            line += """<g:title>[TITLE]</g:title>\n"""
            line = line.replace("[TITLE]", title)
            line += """<g:description>[DESCRIPTION]</g:description>\n"""
            #line = line.replace("[DESCRIPTION]", str(description))
            line += """<g:link>[LINK]</g:link>\n"""
            line = line.replace("[LINK]", link)
            line += """<g:image_link>[IMAGE_LINK]</g:image_link>\n"""
            line = line.replace("[IMAGE_LINK]", image_link)
            line += """<g:condition>[CONDITION]</g:condition>\n"""
            line = line.replace("[CONDITION]", condition) 
            line += """<g:availability>[AVAILABILITY]</g:availability>\n"""
            line = line.replace("[AVAILABILITY]", availability)
            line += """<g:price>[PRICE]</g:price>\n"""
            line = line.replace("[PRICE]", str(price))
            line += """<g:shipping>[SHIPPING]</g:shipping>\n"""
            line = line.replace("[SHIPPING]", shipping)
            line += """<g:gtin>[GTIN]</g:gtin>\n"""
            #line = line.replace("[GTIN]", gtin)
            line += """<g:brand>[BRAND]</g:brand>\n"""
            #line = line.replace("[BRAND]", brand)
            line += """<g:mpn>[MPN]</g:mpn>\n"""
            #line = line.replace("[MPN]", mpn)
#            line += """<g:google_product_category>[GOOGLE_PRODUCT_CATEGORY]</g:google_product_category>\n"""
#            line = line.replace("[GOOGLE_PRODUCT_CATEGORY]", google_product_category)
            line += """<g:product_type>[PRODUCT_TYPE]</g:product_type>\n"""
            line = line.replace("[PRODUCT_TYPE]", product_type)
            
            
            
            
#             line = self.set_line_text(line, id, "@id", True)
#             line = self.set_line_text(line, title, "@title", False)
#             line = self.set_line_text(line, description, "@description", False)
#             line = self.set_line_text(line, google_product_category, "@google_product_category", False)
#             line = self.set_line_text(line, product_type, "@product_type", False)
#             line = self.set_line_text(line, link, "@link", False)
#             line = self.set_line_text(line, image_link, "@image_link", False)
#             line = self.set_line_text(line, condition, "@condition", False)
#             line = self.set_line_text(line, availability, "@availability", False)
#             line = self.set_line_text(line, price, "@price", True)
#             #line = self.set_line_text(line, gtin, "@gtin", False)
#             line = self.set_line_text(line, brand, "@brand", False)
#             line = self.set_line_text(line, mpn, "@mpn", False)
#             line = self.set_line_text(line, shipping, "@shipping", False)
    
            line += """</entry>"""
            positions.append(line)
                    
         return positions    