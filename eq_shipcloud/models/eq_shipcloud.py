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
from openerp.exceptions import Warning
from openerp.osv import osv
import logging
import webbrowser
import ast
_logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    _logger.warning('requests library not found')    



"""
http status codes

When talking to our API you can receive the following status codes:
Code     Name             Description
200     ok             Everything went fine.
204     no content     There is no message body. You'll get this code when deleting a shipment was successful.
400     bad request     Your request was not correct. Please see the response body for more detailed information.
402     payment required     You've reached the maximum of your current plan. Please upgrade to a higher plan.
404     not found     The api endpoint you were trying to reach can't be found.
422     unprocessable entity     Your request was well-formed but couldn't be followed due to semantic errors. Please see the response body for more detailed information.
500     internal server error     Something has seriously gone wrong. Don't worry, we'll have a look at it.
502     bad gateway     Something has gone wrong while talking to the carrier backend. Please see the response body for more detailed information.
504     gateway timeout     Unfortunately we couldn't connect to the carrier backend. It is either very slow or not reachable at all. If you want to stay informed about the carrier status, 
        follow our developer twitter account at @shipcloud_devs.  """
        


class eq_shipcloud(models.Model):

    _name = "eq.shipcloud"
    _description = "This module helps to integrate Odoo with shipcloud api"
    
    _rec_name = "eq_id"
    
    _order = "create_date desc"
    
    create_date = fields.Datetime(string="Creation Date")
    eq_id =  fields.Char(string="Shipment ID",copy=False,help= "Shipcloud shipments ID",required=True)
    eq_carrier_tracking_no =  fields.Char(string="Carrier tracking nos",copy=False,help= "shipments tracking nos")
    eq_tracking_url =  fields.Text(string="Tracking URL",copy=False,help= "shipments tracking URL")
    eq_label_url = fields.Text(string="Label URL",copy=False,help="Label URL")
    eq_price = fields.Float(string="Price",help="Price")
    eq_package = fields.Many2one('stock.quant.package',string="Package",help="Denote the shipment related package")
    
    
    _sql_constraints = [
        ('eq_id_package_unique', 'unique(eq_id, eq_package)',
            'Shipments ID and Package must be unique!'),
    ]
    
    
    @api.multi
    def eq_opentrack_url(self):
        if self.eq_tracking_url:
            webbrowser.open(self.eq_tracking_url)
        
        
    @api.multi
    def eq_openlabel_url(self):
        if self.eq_label_url:
            webbrowser.open(self.eq_label_url)
        
        
    @api.v7
    def eq_check_pack_valid(self,cr,uid,pack_operation_data,context):
        if pack_operation_data.result_package_id.ul_id.height <=0  or pack_operation_data.result_package_id.ul_id.length <=0 or \
                    pack_operation_data.result_package_id.ul_id.width <=0 or pack_operation_data.eq_gross_weight <= 0:
            return False
        
        return True
    
    
    @api.v7
    def eq_create_shipcloud(self,cr,uid,result,context=None):
        
        if result:
            """ Converting unicode string dictionary into dictionary in python """
            
            for res in result:
                d = ast.literal_eval(res.get('response').text)
                
                if d.get('id') == None:
                    return False
                data={
                    'eq_id' : d.get('id') or None,
                    'eq_carrier_tracking_no': d.get('carrier_tracking_no') or None,
                    'eq_tracking_url': d.get('tracking_url') or None,
                    'eq_label_url' :  d.get('label_url') or None,
                    'eq_price' : d.get('price') or None,
                    'eq_package' : res.get('package_id') or None
                              
                }
                eq_shipcloud_id  = self.create(cr,uid,data,context=None)

        return True
    

    @api.v7
    def eq_shipcloud_service_url(self,cr,uid,context=None):
        """         
            Get the shipcloud service url 
        """
        url = self.pool.get('ir.config_parameter').get_param(cr,uid,"eq.shipcloud.service.url",False) or None
        return url
    
    
    @api.v7
    def eq_shipcloud_api_key(self,cr,uid,context=None):
        """         
            Get the shipcloud apikey 
        """
        config_obj = self.pool.get('ir.config_parameter')
        if config_obj.get_param(cr,uid,"eq.is.sandbox.apikey",False) == 'True':
            key = config_obj.get_param(cr,uid,"eq.shipcloud.sandbox.apikey",False)
        else:
            key = config_obj.get_param(cr,uid,"eq.shipcloud.apikey",False)
        return key

    @api.v7
    def _get_to_data(self, cr, uid, picking_data):
        res = {}
        partner = picking_data.partner_id
        
        if not partner.eq_house_no:
            raise (_('Error!'), _('The house no. for the delivery address is not defined.'))            
        
        if partner.type in ('default', 'delivery', 'pobox', 'other'):
            if partner.eq_name2:
                res["to[company]"] = partner.name
                res["to[last_name]"] = partner.eq_name2                                
            else:
                res["to[last_name]"] = partner.name
        elif partner.type == "contact":
            if partner.eq_name2:
                res["to[company]"] = partner.eq_name2
                res["to[first_name]"] = partner.eq_firstname
                res["to[last_name]"] = partner.name    
        
        if partner.use_parent_address:
           res["to[street]"] = partner.street or None,
           res["to[street_no]"] = partner.eq_house_no or None,
           res["to[city]"] = partner.city or None,
           res["to[zip_code]"] = partner.zip or None,
           res["to[country]"] = partner.country_id.name or None,  
        else:
           res["to[street]"] = partner.parent_id.street or None,
           res["to[street_no]"] = partner.parent_id.eq_house_no or None,
           res["to[city]"] = partner.parent_id.city or None,
           res["to[zip_code]"] = partner.parent_id.zip or None,
           res["to[country]"] = partner.parent_id.country_id.name or None,  
        return res

    @api.v7
    def _get_from_data(self, cr, uid, picking_data):
        
        company = picking_data.company_id
        
        if not company.eq_house_no:
            raise Warning(_('The house no. for the company is not defined.'))
             
        res = {
            "from[last_name]": company.name or None,
            "from[street]": company.street or None,
            "from[street_no]": company.eq_house_no or None,
            "from[city]": company.city or None,
            "from[zip_code]": company.zip or None,
            "from[country]": company.country_id.name or None,
            }
        
        return res

    @api.v7
    def eq_create_shipments(self,cr,uid,picking_id,context=None):
        """
            If Delivery order has no package, then shipments will not be created.
        """
        data = {}
        result = {}
        final_result=[]
        count = 0
        if picking_id:
#             Get the shipcloud apikey
            api_key = self.eq_shipcloud_api_key(cr,uid,context=None)
            if api_key == None:
                 raise osv.except_osv(_('Error!'), _('Please provide shipcloud apikey.'))
            stock_pick_obj = self.pool.get("stock.picking")
            stock_quant_package_obj = self.pool.get('stock.quant.package')
            shipcloud_deliverymethod_obj = self.pool.get('eq.shipcloud.deliverymethod')
            picking_data = stock_pick_obj.browse(cr,uid,picking_id,context=None)
            
            delivery_ids = shipcloud_deliverymethod_obj.search(cr,uid,[('eq_deliverymethod_id','=',picking_data.carrier_id.id)],context=None)
            if delivery_ids:
                delivery_data = shipcloud_deliverymethod_obj.browse(cr,uid,delivery_ids,context=None)[0]

                if (not delivery_data.eq_sc_carrier) or  (not  delivery_data.eq_sc_service_id):
                     raise osv.except_osv(_('Error!'), _(' Only when a delivery method is connected with shipcloud carrier and Service a shipment at shipcloud is created.'))
            else: 
                raise osv.except_osv(_('Error!'), _(' Only when a delivery method is connected with shipcloud carrier and Service a shipment at shipcloud is created.'))
            
            
            if picking_data.pack_operation_ids:
                for pack_operation_data in picking_data.pack_operation_ids:
                    
#                     If the Delivery Order has no destination package - throws exception
                    if not pack_operation_data.result_package_id  :
                        raise osv.except_osv(_('Error!'), _('Please provide Destination packages for Shipments.'))
                    
#                     Check valid package dimensions
                    is_package_valid = self.eq_check_pack_valid(cr,uid,pack_operation_data,context=None)
                    if not is_package_valid:
                        raise osv.except_osv(_('Error!'), _('Please provide valid dimensions values for packages.'))
                    
#                     Avoid creating duplicate entries
                    if stock_quant_package_obj.browse(cr,uid,pack_operation_data.result_package_id.id,context=None).eq_is_processed :
                        continue
                          
                    data = {
                            
                            "carrier": delivery_data.eq_sc_carrier or None,
                            "package[weight]": pack_operation_data.result_package_id.eq_gross_weight_changed or pack_operation_data.result_package_id.eq_gross_weight ,
                            "package[length]": pack_operation_data.result_package_id.ul_id.length,
                            "package[width]": pack_operation_data.result_package_id.ul_id.width,
                            "package[height]": pack_operation_data.result_package_id.ul_id.height,
                            "service": delivery_data.eq_sc_service_id.eq_name or None,
                            "create_shipping_label": 'true',
                           
                            }
                    
                    to_data = self._get_to_data(cr, uid, picking_data)
                    from_data = self._get_from_data(cr, uid, picking_data)
                    
                    data.update(to_data)
                    data.update(from_data)
                    
                    #Creating a shipment
                    try:
                        #Get the shipcloud serice url
                        service_url = self.eq_shipcloud_service_url(cr,uid,context=None)
                        res = requests.post(service_url+'/v1/shipments', data=data,auth=(api_key, ''))
                        count +=1
                        #adding package id to the result
                        result= {'package_id':pack_operation_data.result_package_id.id,
                                 'response':res,
                                 'picking_id':picking_id,
                               }
                        
                        final_result.append(result)
                        stock_quant_package_obj.write(cr, uid, pack_operation_data.result_package_id.id,{'eq_is_processed':True},context=context)
                    
                    except Exception, e:
                        _logger.exception(e)
                    

                stock_pick_obj.write(cr, uid, picking_id,{'eq_is_shipped': True,'eq_is_processed':True},context=context)
                return final_result
        
        return False      