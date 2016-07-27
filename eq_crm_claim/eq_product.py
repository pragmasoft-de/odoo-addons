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

class eq_product_template(models.Model):
 
    _inherit = 'product.template'
    
    @api.cr_uid_context
    def _get_act_window_dict(self, cr, uid, name, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.xmlid_to_res_id(cr, uid, name, raise_if_not_found=True)
        result = act_obj.read(cr, uid, [result], context=context)[0]
        return result
    
    def _get_claim_ids_for_prod(self, prod_tmpl_id):
        product_obj = self.env['product.product']
        claim_obj = self.env['crm.claim']
        
        prod_refs = claim_obj.search([('ref','ilike','product')])
        res = [] 
        found_prod_ids = False 
        findProds = product_obj.search([('product_tmpl_id','=', prod_tmpl_id)])
        if findProds:    
            res = [x.id for x in prod_refs if x.ref.id in findProds.ids]
            found_prod_ids = findProds.ids
        return res, found_prod_ids
        
    #crm_claim.crm_case_claims_tree_view
    @api.multi
    def action_view_claims_for_product(self):
        prod_ids, found_prod_ids = self._get_claim_ids_for_prod(self.id)
        act_wind = {
            'name': _('Claims'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'crm.claim',
            #'context': {'default_ref': self.id,},
            'type': 'ir.actions.act_window',
            'domain': [["id", "in", prod_ids]],
        }
        
        if found_prod_ids and len(found_prod_ids) > 0:
            act_wind['context'] = {'default_ref':'product.product,' + str(found_prod_ids[0])}
        
        return act_wind
        
    
    def _claim_count(self):        
        product_obj = self.env['product.product']
        claim_obj = self.env['crm.claim']
        
        prod_refs = claim_obj.search([('ref','ilike','product')])
            
        findProds = product_obj.search([('product_tmpl_id','=', self.id)])
        if findProds:    
            gen = [x for x in prod_refs if x.ref.id in findProds.ids]
            if gen:
                self.claim_count = len(gen)    
            
            
    claim_count = fields.Integer(compute="_claim_count", string='# of Claims')
    
class eq_product(models.Model):
 
    _inherit = 'product.product'
    
    def _get_claim_ids_for_prod(self, prod_id):        
        claim_obj = self.env['crm.claim']
        
        prod_refs = claim_obj.search([('ref','ilike','product')])
        res = []  
        
        if prod_refs:    
            res = [x.id for x in prod_refs if x.ref.id == prod_id]
        return res
    
    @api.multi
    def action_view_claims_for_product(self):
        prod_ids = self._get_claim_ids_for_prod(self.id)
        return {
            'name': _('Claims'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'crm.claim',
            'context': {'default_ref': 'product.product,' + str(self.id)},
            'type': 'ir.actions.act_window',
            'domain': [["id", "in", prod_ids]],
        }
    
    def _claim_count(self):            
        claim_ids = self._get_claim_ids_for_prod(self.id)
        if claim_ids:
            self.claim_count = len(claim_ids)  
            
            
    claim_count = fields.Integer(compute="_claim_count", string='# of Claims')