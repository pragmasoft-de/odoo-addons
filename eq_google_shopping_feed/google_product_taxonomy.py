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

from openerp import api,models, fields
import os
import csv

class Eq_google_product_taxonomy(models.Model):
   
    _name = "google.product.taxonomy"
    _description = "all product taxonomy of google"
    _rec_name = "name"
    
    @api.depends("code", "long_name1", "long_name2", "long_name3", "long_name4", "long_name5", "long_name6", "long_name7")
    def _get_name(self):
        for categ in self:
            categorie = [categ.long_name1, categ.long_name2, categ.long_name3, categ.long_name4, categ.long_name5, categ.long_name6, categ.long_name7]
            categorie = [x for x in categorie if x != "" and x]
            name = ' > '.join(categorie)
            if name and categ.code != False:
                categ.name = "[" + categ.code + "]" + name
                
    def _search_name(self, operator, value):
        return ['|', '|', '|', '|', '|', '|', '|', ('code', operator, value), ('long_name1', operator, value), ('long_name2', operator, value), ('long_name3', operator, value), ('long_name4', operator, value), ('long_name5', operator, value), ('long_name6', operator, value), ('long_name7', operator, value)]       
            
            
    
    code = fields.Char('Code', size=10)
    name = fields.Char(string="Complete Category", compute=_get_name, store=False, search="_search_name")
    long_name1 = fields.Char('Categ_1')
    long_name2 = fields.Char('Categ_2')
    long_name3 = fields.Char('Categ_3')
    long_name4 = fields.Char('Categ_4')
    long_name5 = fields.Char('Categ_5')
    long_name6 = fields.Char('Categ_6')
    long_name7 = fields.Char('Categ_7')

    
    def _create_data(self, cr, uid, diff, path, objectname, config_param_obj):
        
        ir_model_data_object = self.pool.get('ir.model.data')
        
        #Version wird gesetzt
        config_param_obj.set_param(cr,uid,'taxonomy.csv.version', diff)    
        
        reader_data = open(path + '/google.product.taxonomy_' + diff +'.csv')
        reader = csv.reader(reader_data,delimiter=',')
        next(reader)
        for row in reader:
            model_data_id = ir_model_data_object.search(cr, uid, [('name', '=', str(row[0])),('model', '=', 'google.product.taxonomy' )])
            if model_data_id:
                # Datensatz überarbeiten 
                model_id = ir_model_data_object.browse(cr, uid, model_data_id)
                self.write(cr, uid, model_id.res_id, {'code' : str(row[0]), 'long_name1' : row[1],'long_name2' : row[2], 'long_name3' : row[3], 'long_name4' : row[4], 'long_name5' : row[5], 'long_name6' : row[6], 'long_name7' : row[7]})
                #self.write(cr, uid, model_id.res_id, {'code' : str(row[0]), 'long_name1' : row[1]})
            else:
                # Datensatz erstellen
                create_id = self.create(cr, uid,{'code' : str(row[0]), 'long_name1' : row[1],'long_name2' : row[2], 'long_name3' : row[3], 'long_name4' : row[4], 'long_name5' : row[5], 'long_name6' : row[6], 'long_name7' : row[7]})
                #create_id = self.create(cr, uid,{'code' : str(row[0]), 'long_name1' : row[1]})
                ir_model_data_object.create(cr, uid,{'name': str(row[0]), 'model' : 'google.product.taxonomy', 'res_id' : create_id})
            print 'CODE:', str(row[0])
          
        return True
    
    @api.cr_uid
    def _eq_load_taxonomy(self, cr, uid):
        config_param_obj = self.pool.get('ir.config_parameter')
        
        dir = os.path.dirname(__file__)
        #path = os.path.join(dir, '/cities')
        path = dir + '/taxonomy'
        #path = '/home/odoo/git/odoo-tools/dlt_germany_cities/cities' #TODO
        
        objects = os.listdir(path)
        objects.sort()
        
        for objectname in objects:
            version = config_param_obj.get_param(cr, uid, 'taxonomy.csv.version', "0")
            diffunderscore = objectname.split('_')[1]
            diff = diffunderscore.split('.')[0]
            #Wenn eine Version vorhanden ist und diese kleiner ist als die Version der Datei, dann werden die Daten eingespielt
            if version:
                if int(diff) > int(version):
                   self._create_data(cr, uid, diff, path, objectname, config_param_obj)   
            #Sollte keine Version eingetragen sein, werden die Daten alle eingespielt
            else:
               self._create_data(cr, uid, diff, path, objectname, config_param_obj)
