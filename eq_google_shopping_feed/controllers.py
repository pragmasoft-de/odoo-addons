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
     #@http.route('/eq_google_shopping_feed/data_de.txt', website=True, type='http', auth="none")
     @http.route('/eq_google_shopping_feed/data_de.txt', auth='public', website=True)
     def index_de(self, **kw):                 
         # ?db=eqwebsite                
         #ensure_db()
         return self.generate_file("de") 
         



        
     def generate_file(self, language):
         # 1.generate header
         header = self.generate_header()
         
         # 2. generate positions
         data1 = self.generate_position()
         data2 = "261|aeroSlingÂ® HipBag|TrainingsgerÃ¤te von aerobis sind deutsche Produkte die nach hohen Standards in Deutschland und Europa gefertigt werden, um Top-QualitÃ¤t und -FunktionalitÃ¤t bieten zu kÃ¶nnen. Bei der Entwicklung der Produkte steht bei aerobis der effektive und nachhaltige Trainingserfolg des Kunden an erster Stelle. Egal ob AnfÃ¤nger oder Profisportler - join the Functional Movement!   Der hochwertige aeroSlingÂ® HipBag begeistert durch hohe FunktionalitÃ¤t und viele praktische NutzungsmÃ¶glichkeiten! Er ist der optimale Begleiter fÃ¼r das aeroSlingÂ® Slingtraining unterwegs.  'Ich packe meinen aeroSlingÂ®!'  aeroSlingÂ® Slingtrainer lassen sich mÃ¼helos im aeroSlingÂ® HipBag verstauen. FÃ¼r Kleinigkeiten, wie beispielsweise etwas Bargeld, SchlÃ¼ssel, etc., ist ebenso ausreichend Platz vorhanden. HierfÃ¼r sind neben der groÃŸen Fronttasche zwei separate SeitenfÃ¤cher und ein breites Fach am RÃ¼cken angebracht worden.   Quick Facts   Perfektes MaÃŸ   Leichte Handhabung   Viel Platz   Der optimale Trainingsbegleiter fÃ¼r unterwegs|'Sportartikel > SportÃ¼bungen & Fitness > KrafttrainingsgerÃ¤te"
                        
         content = header + "\n\n" + data1 + "\n" + data2    
         mimetype ='application/text;charset=utf-8'
         #return http.request.make_response(content, [('Content-Type', mimetype)])
         return http.request.make_response(content)
         
         
     def generate_header(self):
         """ generates header for google feed """
         return "id|titel|beschreibung|google produktkategorie|produkttyp|link|bildlink|zustand|verfÃ¼gbarkeit|preis|marke|mpn|versand"         

     def generate_position(self):
         """ generates position for datarow from db """
         # id
         # title
         # beschreibung
         # google produktkategorie
         # produkttyp
         # link                - http://localhost:8069/shop/product/aerosling-flex-clip-component-9
         # bildlink            - http://localhost:8069/website/image/product.product/1020/image
         # zustand
         # verfuegbarkeit
         # preis                - list_price
         # marke
         # mpn
         # versand
         positions = []
         
         products = http.request.env['product.template'].search([('state', '=', 'sellable')]),         
         for id in products[0].ids:
            product = http.request.env['product.template'].browse(id)
            id = product.id
            title = product.name
            description = product.description_sale
            category = "todo"
            product_type = "todo"
            link = "todo"
            image_link = "todo"
            state = "todo"
            availability = "todo"
            price = "todo"
            brand = "todo"
            mpn = "todo"
            shipping = "todo"
            
            #line = str(id) + "|" + title + "|" + description + "|" + category + "|" + product_type + "|" +  link + "|" + image_link + "|" +  state + "|" + availability + "|" + price + "|" + brand + "|" + mpn + "|" + shipping
            line = "@id|@title|@description|@category|@product_type|@link|@image_link|@state|@availability|@price|@brand|@mpn|@shipping"
            line = line.replace("@id", id)    
            positions.append(line)
        
         print positions
            
            
         
         
         return "270|blackPack Loading-Bag SAND (leer)|TrainingsgerÃ¤te von aerobis sind deutsche Produkte, die nach hohen Standards in Deutschland und Europa gefertigt werden, um Top-QualitÃ¤t und -FunktionalitÃ¤t bieten zu kÃ¶nnen. Bei der Entwicklung der Produkte steht bei aerobis der effektive und nachhaltige Trainingserfolg des Kunden an erster Stelle. Egal ob AnfÃ¤nger oder Profisportler - join the Functional Movement!   Den blackPackÂ® Loading-Bag SAND fertigen wir fÃ¼r extreme Belastungen. Der aus PVC gefertigte Bag wird nicht nur vernÃ¤ht, sondern zusÃ¤tzlich auch an den NÃ¤hten verschweisst um die Haltbarkeit zu verbessern. Als Verschluss bieten wir einen sehr widerstandsfÃ¤higen Wickelverschluss mit einer stabilen Schnalle.  Komfortabler Einleger fÃ¼r den blackPackÂ® PRO und den blackPackÂ® ESY  Der blackPackÂ® Loading-Bag SAND dient der sicheren und komfortablen Beladung des blackPacksÂ®.    Flexibel beladen und trainieren  Jeder blackPackÂ® Loading-Bag SAND wird unbefÃ¼llt geliefert, um Ihnen Versandkosten zu sparen. Sie sollten mit mÃ¶glichst trockenem Sand befÃ¼llt werden.    Bis zu 3 blackPackÂ® Loading-Bags SAND passen in einen blackPackÂ®  Sie sind aus sehr stabilem PVC gefertigt und mit einem Wickelverschluss ausgestattet. Durch den Wickelverschluss lÃ¤sst sich der Bag auÃŸerdem auf fast jede GrÃ¶ÃŸe anpassen und ist so auch fÃ¼r viele andere Aufgaben einsetzbar.   Quick Facts   LÃ¤nge durch WickelverschluÃŸ flexibel   Gefertigt aus widerstandsfÃ¤higem PVC   NÃ¤hte zusÃ¤tzlich verschweiÃŸt   BefÃ¼llung bis maximal 12,5 kg|'Sportartikel > SportÃ¼bungen & Fitness > KrafttrainingsgerÃ¤te'|#aerobis products|http://www.functional-movement-shop.com/de/blackpack-loading-bag-sand-leer|http://www.functional-movement-shop.com/media/images/popup/1B_P_loading_bag_folded.jpg|new|in stock|29.90|blackPack|52|DE::Standard:0"            