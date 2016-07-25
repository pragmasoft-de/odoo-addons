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
    
     @http.route('/google_shopping_feed/data_at.xml', auth='public', website=True)
     def index_at(self, **kw):
         """ feed for austria """                          
         return self.generate_file("at")

     @http.route('/google_shopping_feed/data_ch.xml', auth='public', website=True)
     def index_ch(self, **kw):
         """ feed for switzerland """                 
         return self.generate_file("ch")
     
     @http.route('/google_shopping_feed/data_de.xml', auth='public', website=True)
     def index_de(self, **kw):   
         """ feed for germany """              
         # ?db=eqwebsite                
         #ensure_db()
         return self.generate_file("de") 
             
     @http.route('/google_shopping_feed/data_en.xml', auth='public', website=True)
     def index_en(self, **kw):
         """ feed for us """                 
         return self.generate_file("en")
     
     @http.route('/google_shopping_feed/data_gb.xml', auth='public', website=True)
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
            'Content-Type': 'text/xml; charset=utf-8',      # signalisiert dem Browser (Chrome), dass es sich bei der übermittelten Datei um eine XML-Datei handelt.
            })
         
        
                  
     def generate_header(self):
         """ generates header for google feed """
         website = http.request.env['website'].browse(1)
         website_name = website.name
         url = request.httprequest.url_root
         date = website.write_date
         xmlTemplate ="""<?xml version="1.0"?>
    <feed xmlns="http://www.w3.org/2005/Atom" xmlns:g="http://base.google.com/ns/1.0">
        <title>[TITLE]</title>
        <link rel="self" href="[URL]"/>
        <updated>[DATE]</updated> 
         """ 
         #20011-07-11T12:00:00Z 
         xmlTemplate = xmlTemplate.replace("[TITLE]", website_name) 
         xmlTemplate = xmlTemplate.replace("[URL]", url)  
         xmlTemplate = xmlTemplate.replace("[DATE]", date)
         
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
             else:
                 return request.httprequest.url_root + "website/image/product.template/" + str(id) + "/image"          #Wenn kein Prodúktvarianten-Bild vorhanden, dann wird das Bild vom Template genommen.

         
         
     def generate_positions(self, contry_code):
         """ generates position for datarow from db """         
         positions = []   
         color = False
         size = False     
         gender = False
         age_group = False
         material = False
         pattern = False
         #item_group_id = False 
         
         #products = http.request.env['product.template'].search([('state', '=', 'sellable')])         # original
         #sql = "SELECT id FROM product_template where state = 'sellable'"
         
         sql = "SELECT id FROM product_template where website_published = True"
         http.request.env.cr.execute(sql)
         products = http.request.env.cr.fetchall()                
         

         #products = http.request.env['product.template'].search([('website_published', '=', True)])                                     # new      
         #for id in products[0].ids:                                                                    # original
         for id in products:                                                                               
            product = http.request.env['product.template'].sudo().browse(id)
            id = product.id                                                 # id
            #attribute_line_ids = product.attribute_line_ids
            
            product_product = http.request.env['product.product'].sudo().search([('product_tmpl_id', '=', id)])
            
            title = product.name                                            # titel
            
            
            description_1 = product.description_sale                        # description - original
            
            description_2 = description_1.replace("%", "&#37;")
            description_3 = description_2.replace("<", "&lt;")
            description_4 = description_3.replace(">", "&gt;")
            description = description_4.replace("&", "&amp;")
            
                       
            if contry_code == 'at' or contry_code == 'ch' or contry_code == 'de':
                if product.eq_google_product_category != False:
                    google_product_category = product.eq_google_product_category    # google_product_category
                else:
                    google_product_category =''
            elif contry_code == 'en' or contry_code == 'gb':
                google_product_category = "Sporting Goods > Exercise & Fitness > Weightlifting Machines"    # google_product_category
                
            #google_product_category = google_product_category.decode('utf-8')
            
            product_type = product.categ_id.name                            # Optional:product_type            
            link = self.generate_link(id)                                   # link
            mobile_link = link                                              # mobile_link
            image_link = self.generate_image_link(id)                       # image_link
            condition = product.eq_condition                                # condition
            availability = "in stock"                                       # availability
            
  
            brand = product.product_brand_id.name                           # brand
            #mpn = product.default_code                                     # mpn
            #shipping = "DE::Standard:0"                                    # shipping
            
            #Product_Product Objekte
            for product_obj in product_product:
                gtin = product_obj.ean13
                if contry_code == 'de':                                                                            #GTIN
                    price = str(product_obj.list_price) + ' EUR'                                                                     #Price  
                    country = 'DE' 
                elif contry_code == 'en':
                    price = str(product_obj.list_price) + ' USD'
                    country ='US'
                availability = product_obj.qty_available                                                            #Stock
                if product_obj.weight_net != False and product_obj.eq_basic.name != False:
                    unit_measure = str(product_obj.weight_net) + ' ' + product_obj.eq_basic.name                    #Grundpreis Maß
                else:
                    unit_measure = ''
                    
                if product_obj.volume != False and product_obj.eq_basic.name != False:
                    basic_unit = str(1.0) + ' ' + product_obj.eq_basic.name                                         #Grundpreiseinheitsmaß
                else:
                    basic_unit = ''
                #basic_price = str(product_obj.eq_basic_price)                                                      #Grundpreiseinheit
                
                shipping_weight = str(product_obj.weight) + ' ' + 'kg'                                              #Bruttogewicht
                
                product_product_attr_values = product_obj.attribute_value_ids
                for product_product_attribute in product_product_attr_values:
                    
                    
                    attribute_value = product_product_attribute.name
                    attribute = product_product_attribute.attribute_id.name
                    google_value = product_product_attribute.attribute_id.eq_google_attribute 
                    if google_value == 'color':
                        color = attribute_value
                    if google_value == 'size':
                         size = attribute_value
#                     if google_value == 'item_group_id':
#                         item_group_id = attribute_value
                    if google_value == 'gender':
                        gender = attribute_value
                    if google_value == 'age_group':
                        age_group = attribute_value
                    if google_value == 'material':
                        material = attribute_value
                    if google_value == 'pattern':
                        pattern = attribute_value
            
            delivery = http.request.env['delivery.carrier'].sudo().search([('id','=',1)])
            shipping_price = str(delivery.normal_price)
            
            
            #Aufbau XML-FEED
            
            line = """<entry>\n"""
            line += """<g:id>[ID]</g:id>\n"""          
            line = line.replace("[ID]", str(id))
            line += """<g:title>[TITLE]</g:title>\n"""
            line = line.replace("[TITLE]", title)
            if description != False:
                line += """<g:description>[DESCRIPTION]</g:description>\n"""
                line = line.replace("[DESCRIPTION]", description)
            else:
                pass
            line += """<g:link>[LINK]</g:link>\n"""
            line = line.replace("[LINK]", link)
            line += """<g:mobile_link>[MOBILE_LINK]</g:mobile_link>\n"""
            line = line.replace("[MOBILE_LINK]", mobile_link)
            if image_link:
                line += """<g:image_link>[IMAGE_LINK]</g:image_link>\n"""
                line = line.replace("[IMAGE_LINK]", image_link)
            else:
                pass
            line += """<g:condition>[CONDITION]</g:condition>\n"""
            line = line.replace("[CONDITION]", condition) 
            if availability > 0:
                line += """<g:availability>[AVAILABILITY]</g:availability>\n"""
                line = line.replace("[AVAILABILITY]", 'in stock')
            else:
                pass
            line += """<g:price>[PRICE]</g:price>\n"""
            line = line.replace("[PRICE]", price)
            
            line += """<g:shipping>\n
            <g:country>[COUNTRY]</g:country>\n
            <g:service>Standard</g:service>\n
            <g:price>[SHIPPING_PRICE]</g:price>\n
            </g:shipping>\n"""  
            line = line.replace("[COUNTRY]", country)
            line = line.replace("[SHIPPING_PRICE]", shipping_price)
            
            
            line += """<g:shipping_weight>[SHIPPING_WEIGHT]</g:shipping_weight>\n"""
            line = line.replace("[SHIPPING_WEIGHT]", shipping_weight)
            
                
#             line += """<g:shipping_label>[SHIPPING_LABEL]</g:shipping_label>"""
#             line = line.replace("[SHIPPING_LABEL]", shipping_label)
            
            if gtin != False:
                line += """<g:gtin>[GTIN]</g:gtin>\n"""
                line = line.replace("[GTIN]", gtin)
            else:
                pass
            if brand != False:
                line += """<g:brand>[BRAND]</g:brand>\n"""
                line = line.replace("[BRAND]", brand)
            else:
                pass
#             if mpn != False:
#                 line += """<g:mpn>[MPN]</g:mpn>\n"""
#                 line = line.replace("[MPN]", mpn)
#             else:
#                 pass
            if google_product_category != '': 
                line += """<g:google_product_category>[GOOGLE_PRODUCT_CATEGORY]</g:google_product_category>\n"""
                line = line.replace("[GOOGLE_PRODUCT_CATEGORY]", google_product_category)
                
            else:
                pass
            
            #line += """<g:product_type>[PRODUCT_TYPE]</g:product_type>\n"""
            #line = line.replace("[PRODUCT_TYPE]", product_type)
            
            #if item_group_id != False:
                #line += """<g:item_group_id>[ITEM_GROUP_ID]</g:item_group_id>\n"""
                #line = line.replace("[ITEM_GROUP_ID]", item_group_id)
                #item_group_id = False
            
            if color != False:
                line += """<g:color>[COLOR]</g:color>\n"""
                line = line.replace("[COLOR]", color)
                color = False
            
            if gender != False:
                line += """<g:gender>[GENDER]</g:gender>\n"""
                line = line.replace("[GENDER]", gender)
                gender = False
            
            if age_group != False:
                line += """<g:age_group>[AGE_GROUP]</g:age_group>\n"""
                line = line.replace("[AGE_GROUP]", age_group)
                age_group = False
            
            if material != False:
                line += """<g:material>[MATERIAL]</g:material>\n"""
                line = line.replace("[MATERIAL]", material)
                material = False
            
            if pattern != False:
                line += """<g:pattern>[PATTERN]</g:pattern>\n"""
                line = line.replace("[PATTERN]", pattern)
                pattern = False
            
            if size != False:
                line += """<g:size>[SIZE]</g:size>\n"""
                line = line.replace("[SIZE]", size)
                size = False
            else:
                pass

            if unit_measure != '':
                line += """<g:unit_pricing_measure>[UNIT_PRICING_MEASURE]</g:unit_pricing_measure>\n"""
                line = line.replace("[UNIT_PRICING_MEASURE]", unit_measure)
            
            if basic_unit != '':
                line += """<g:unit_pricing_base_measure>[UNIT_PRICING_BASE_MEASURE]</g:unit_pricing_base_measure>\n"""
                line = line.replace("[UNIT_PRICING_BASE_MEASURE]", basic_unit)
#             if basic_price != False:
#                 line += """<g:unit_pricing_base_measure>[UNIT_PRICING_BASE_MEASURE]</g:unit_pricing_base_measure>\n"""
#                 line = line.replace("[UNIT_PRICING_BASE_MEASURE]", basic_price)
#             else:
#                 pass
            
            line += """</entry>"""
    
            positions.append(line)
                    
         return positions    