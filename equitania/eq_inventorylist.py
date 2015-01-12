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

from openerp.osv import fields, osv

index_product_id = 5
index_quantity = 7
index_price_unit_on_quant = 9
index_einkaufspreis = 10
index_lagerwert = 15


class eq_inventorylist(osv.osv):
    _name = "eq_inventorylist"
    result = []
            
    def change_none_to_zero(self, value):
        """ kleine Hilfsfunktion, die aus dem None einen 0 Wert macht """
        if value is None:
            return 0
        return value
        
    def correct_price(self, record):
        """
        Der preis muss immer korrigiert werden - sicher ist sicher :-)
        Man soll Immer den Wert aus der Spalte price_unit_on_quant nehmen. Falls da der Wert 0 ist, soll den Wert aus der Spalte Einkaufspreis verwendet werden.
        
        Lagerwert = quantity * preis
        """
        quantity = record[index_quantity]
        price_unit_on_quant = record[index_price_unit_on_quant]
        einkaufspreis = record[index_einkaufspreis]
        
        quantity = self.change_none_to_zero(quantity);
        price_unit_on_quant = self.change_none_to_zero(price_unit_on_quant);
        einkaufspreis = self.change_none_to_zero(einkaufspreis);
                
        lagerwert = 0
        if price_unit_on_quant > 0:
            lagerwert = float(quantity) * float(price_unit_on_quant)
        else:
            lagerwert = float(quantity) * float(einkaufspreis)
                
        # lagewert setzten
        record[index_lagerwert] =  lagerwert
                     
        return record
        
    def check_for_double_positions(self, originalList, actualRecord):
        """
        Berechnet gesammtwert von Menge, Preis und Lagerwert
        """
        quantity_total = 0
        stockvalue_total = 0            
        articleId = actualRecord[index_product_id]
        
        for tuple_record in originalList:            
            record = list(tuple_record)
            if record[index_product_id] == actualRecord[index_product_id]:        # nur den datensatz holen, der gleich product_id hat

                # zuerst muss der Preis korrigiert werden            
                self.correct_price(record)
            
                # jetzt wird die gesammsumme von menge und lagewert berechnet
                quantity_total += record[index_quantity]
                stockvalue_total += record[index_lagerwert]                               
        
                
        # jetzt wird das ergebnis gesetzt
        actualRecord[index_quantity] = quantity_total
        actualRecord[index_lagerwert] = stockvalue_total
        
        """    
        if articleId == 58760:                                         
            print "-------"
            print actualRecord
            print "-------"
            print "articleId: " + str(articleId) + ", quantity_total: " + str(quantity_total) + ", stockvalue_total: " + str(stockvalue_total)
            print "-------"
        """
        
        return actualRecord
    
    def generate_statement(self, dateFrom, dateUntil):       
        """ bereitet unser sql statement vor """ 
        sql = """SELECT MIN(id) as id,
               move_id,
               location_id,
               lagerort,
               company_id,
               product_id,
               product_categ_id,
               SUM(quantity) as quantity,               
               date,
               price_unit_on_quant,
               (SELECT prop.value_float FROM ir_property AS prop WHERE prop.res_id = 'product.template,' || to_char(product_template_id, 'FM9999999')) as Einkaufspreis,
               source,
        eq_lst_price,
        default_code as Produktnummer,
        product_name,
        (price_unit_on_quant * quantity) as lagerwert,
        (SELECT uom.name FROM product_uom AS uom WHERE uom.id = uom_po_id) AS Einkaufseinheit      
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
                   product_template.uom_id as uom_id,
                   product_template.id as product_template_id,
                   product_template.name as product_name,
                   product_product.default_code as default_code,
                   dest_location.name as lagerort,
                   product_template. uom_po_id as uom_po_id
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
                   product_template.uom_id as uom_id,
                   product_template.id as product_template_id,
                   product_template.name as product_name,
                   product_product.default_code as default_code,
                   dest_location.name as lagerort,
                   product_template. uom_po_id as uom_po_id
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
               where date between '%s' and  '%s'
               GROUP BY move_id, location_id, company_id, product_id, product_categ_id, date, price_unit_on_quant, source, eq_lst_price, uom_id, default_code, lagerwert, product_name, lagerort, product_template_id, uom_po_id
               order by default_code
            """ % (dateFrom, dateUntil)
            
        return sql
    
    def build_finalList(self, actualRecord):
        """
        Bildet finale Liste mit allen Daten - keine doppelte datensätze hinzufügen
        """        
        existing_position = False
        if len(self.result) > 0:
            for record in self.result:
                product_id_in_list = record[index_product_id]
                product_id = actualRecord[index_product_id]
                if product_id_in_list == product_id:
                    existing_position = True
                    
        if existing_position == False:                        
            self.result.append(actualRecord)                        
                                                 
    def get_inventorylist(self, cr, uid, dateFrom, dateUntil):
        self.result = []
        
        #print "----"
        #print "dateFrom " + dateFrom
        #print "dateUntil " + dateUntil
        #print "----"
        
        """
        Diese Funktion wird von aussen über XML-RPC ausgeführt und ermittelt Lagerwerte aus der DB
        """   
        # 1. alle Daten aus der DB holen
        sql = self.generate_statement(dateFrom, dateUntil) 
        cr.execute(sql)
                                        
        # 2. Daten korrigieren        
        data = cr.fetchall()
        #print "fetchall() - length: " + str(len(data))
        
        for record in data:            
            record_as_list = list(record)
            actualRecord = self.check_for_double_positions(data, record_as_list)
            articleId = actualRecord[index_product_id]
            self.build_finalList(actualRecord)
            
            """
            articleId = actualRecord[index_product_id]
            quantity_total = actualRecord[index_quantity]
            stockvalue_total = actualRecord[index_lagerwert]
            if articleId == 58760:                                         
                print "-------"
                print actualRecord
                print "-------"
                print "articleId: " + str(articleId) + ", quantity_total: " + str(quantity_total) + ", stockvalue_total: " + str(stockvalue_total)
                print "-------"
            """
                
        #print "self.result - length: " + str(len(self.result))
        
        # 3. Dictionary mit allen daten erzeugen und zurück schicken
        # muster template
        #res = {'row1': {'move_id': 1, 'test': 'xyz'}, 'row2': {'move_id': 2, 'test': 'xyz'} }
        
        # felder für sub-dictionary
        keys  = ['id', 'move_id', 'location_id', 'lagerort', 'company_id', 'product_id', 'product_categ_id', 'quantity', 'date', 'price_unit_on_quant', 'einkaufspreis', 'source', 'eq_lst_price', 'produktnummer', 'produkt_name', 'lagerwert', 'Einkaufseinheit']
                
        finalResult = {}
        rowId = 0
        for row in self.result:  
            index = 0
            datarow = {}
            for cellvalue in row:  
                if cellvalue is None:
                    datarow[keys[index]] = ""
                else:
                    datarow[keys[index]] = cellvalue
                    
                index = index + 1

            rowId = rowId + 1
            recordName = "row" + str(rowId)
            finalResult[recordName] = datarow
                
                           
        return finalResult        