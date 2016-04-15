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

from openerp import http
from openerp import models, fields, api, _
import os
import base64
import cStringIO
from PIL import Image
import PIL
from openerp.tools import image_save_for_web, image_resize_image, eq_image_resize_image
from openerp.http import request

class ImageHelper(http.Controller):
    
    @http.route('/reset_images/', auth='public')
    def reset_images(self):
        self._reset_reference_images()                
        return "Done"
    
    def _resize_image(self, original_image):
        """
            Resize an image and ignore strange records in illingen hats DB
            @original_image: original image loaded from db
            @return: resized image or None
        """
        if "FileStorage:" not in original_image:
            return eq_image_resize_image(original_image, (1024, 1024), "base64", None, False)
        else:
            print "* Skipping wrong data format *"
            return None
    
    def _reset_reference_images(self):
        """
            Reset (resize all reference images)
        """
        print "* START of _reset_reference_images *"
        cr, uid, context = request.cr, request.uid, request.context
        res_partner_obj = http.request.env['res.partner'].sudo()
        sql = "select id from res_partner where eq_ref_image_a is not null or eq_ref_image_b is not null or eq_ref_image_c is not null"
        http.request.cr.execute(sql)
        for result in cr.fetchall():        
            partner = res_partner_obj.browse(result[0])
            if partner.eq_ref_image_a is not None:
                resized_image = self._resize_image(partner.eq_ref_image_a)
                if resized_image  is not None:                
                    partner.eq_ref_image_a = resized_image 
            
            if partner.eq_ref_image_b is not None:    
                resized_image = self._resize_image(partner.eq_ref_image_b)
                if resized_image  is not None:                
                    partner.eq_ref_image_b = resized_image
            
            if partner.eq_ref_image_c is not None:    
                resized_image = self._resize_image(partner.eq_ref_image_c)
                if resized_image  is not None:                
                    partner.eq_ref_image_c = resized_image
        
        print "* END of _reset_reference_images *"
            
    """
    @http.route('/test_image/', auth='public')
    def test_image(self):        
        print "*** test_image ****"
        PATH_PRODUCT_IMAGES = '/home/odoo/git/odoo-addons/eq_imagehelper/testimages/'                
        for subdir, dirs, files in os.walk(PATH_PRODUCT_IMAGES):
            for file in files:
                file_path = os.path.join(subdir, file)
                print "file_path: ", file_path
                
                if file_path:
                    with open(file_path, "rb") as image_file:
                        image_data = image_file.read()
                        encoded_image = base64.b64encode(image_data)         # encode image to base64
                        
                        # resize image - fires resize image + image_resize_and_sharpen
                        resized_image = eq_image_resize_image(encoded_image, (1000, 1000), "base64", None, False)
                                                
                        # 5702
                        template_obj = http.request.env['product.template'].sudo()
                        template = template_obj.browse(5702)
                        template.image_medium = resized_image       # fires 3 functions image_resize_image_big, image_resize_image_medium and image_resize_image_small

        return "DONE..."
    """