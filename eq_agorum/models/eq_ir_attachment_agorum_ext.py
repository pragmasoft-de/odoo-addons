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
from openerp.osv import osv
import base64
from openerp.addons.eq_agorum import eq_agorum_functions

class eq_ir_attachment_agorum_ext(osv.Model):
    _inherit = 'ir.attachment'
    
    #res_model = fields.Char(string="Model")
    #res_id = fields.Char(string="Res ID")
    agorum_uuid = fields.Char(string="Agorum UUID")
    datas = fields.Binary(string = "File Content", compute='_data_get', inverse='_data_set')
    
    
    @api.model 
    def get_agorum_settings(self, uid=0):
        """
        Loads the settings needed to connect to Agorum
        @param uid: ID of the user 
        """
        
        try:
            config_params = self.env['ir.config_parameter']
            session_service = config_params.get_param("eq.agorum.session.service",False)
            object_service = config_params.get_param("eq.agorum.object.service",False)
            token = config_params.get_param("eq.agorum.token",False)
            user_name = config_params.get_param("eq.agorum.user",False)
            pw = config_params.get_param("eq.agorum.pw",False)
            target_directory = config_params.get_param("eq.agorum.target.directory",False) 
            
            if (session_service and not session_service.endswith('/')):
                session_service += '/'
            if (object_service and not object_service.endswith('/')):
                object_service += '/'
                
                
            if (uid > 0):
                user = self.env['res.users'].browse(uid)
                if (user and user.eq_agorum_password):
                    #Todo: use Token; password optional
                    if (user.eq_agorum_user):
                        user_name = user.eq_agorum_user
                    else:
                        user_name = user.login
                    if (user.eq_agorum_password):
                        pw = user.eq_agorum_password
                        
            settings = eq_agorum_functions.agorum_settings(session_service, object_service, target_directory, user_name, pw, token)   
            return settings
        except Exception, e:
            print 'Fehler: ' +  str(e.message)
    
    def check_settings(self, agorum_settings):
        settings_ok = agorum_settings and agorum_settings.user and agorum_settings.object_service and agorum_settings.session_service and agorum_settings.target_directory
        return settings_ok
    
    @api.model 
    def create(self, values):
        #return super(eq_ir_attachment_agorum_ext, self).create(values) #für Tests; bis Agorumfunktionalität freigegeben werden kann
        """
        Uploads a document to Agorum and returns the uuid of the document.
        """
        agorum_settings = self.get_agorum_settings(self._uid)
        settings_ok = self.check_settings(agorum_settings)
        
        if ('datas_fname' not in values):
            #sonst Fehler
            return super(eq_ir_attachment_agorum_ext, self).create(values)
        
        if (settings_ok):
            try:
                file_values = {
                               'filename':values['datas_fname']
                               }
                
                if ('datas' in values and values['datas']):
                    file_data = base64.b64decode(values['datas'])
                    file_values.update({'file_data' : file_data})
                else:
                    #TODO: Fehler
                    return
                agorum_handler = eq_agorum_functions.eq_agorum_functions(agorum_settings)
                
                #Todo: get login data
                
                login_settings = {
                                  'agorum_user':agorum_settings.user,
                                  'agorum_password':agorum_settings.pw,
                                   #'as_user':'p.exler'
                                  }
                """
                TODO: Login über Token
                try:
                    create_token_result = agorum_handler.create_token(login_settings)
                except Exception, e:
                    print 'Error in create: ' + e.message
                    return
                
          
                if (not create_token_result or not create_token_result.success):
                    #TODO: Error
                    #print 'return'
                    return
                   
                login_settings = {
                                  'agorum_user':'o.hercht',
                                  'agorum_token': create_token_result.token,
                                  'as_user':'h.bischoff'
                                  }
                """
                login_with_token_result = agorum_handler.login(login_settings)
                session_id = login_with_token_result.sessionID
                upload_result = agorum_handler.upload_file(file_values, session_id)
                uuid = '';
                if (upload_result):
                    if (upload_result.success):
                        uuid = upload_result.uuid
                        values.update({'agorum_uuid' : uuid})
                    else:
                        print 'upload_result.message: ' + upload_result.message
                        #show error
                        return False
                                
                
             
                #file_exists = agorum_handler.file_exists(uuid, session_id)
                #if (file_exists):
                #    print 'file exists'
                
                #für insert
                return super(eq_ir_attachment_agorum_ext, self).create(values)
                
                """
                if (uuid):
                    metadata_elements = {
                        '~Test':'1234',
                    }
                    print 'set metadata'
                    agorum_handler.set_metadata(uuid, metadata_elements, session_id)
                """    
                
            
            except Exception, e:
                print 'error in create2: ' + e.message
                
        else:
            print 'settings missing'
            return super(eq_ir_attachment_agorum_ext, self).create(values)
    
    
    """
    @api.model 
    def read(self, ids, fields_to_read):
        print 'read'
    """
    
    @api.one
    def _data_get(self):
        """
        Overridden function to set additional parameter 
        """
        for attach in self:#.browse(ids):
            if attach.store_fname:
                attach.datas = self._file_read(attach.store_fname, attach.id, attach.agorum_uuid, False)
            else:
                attach.datas = attach.db_datas
        return True
    
    @api.one
    def _data_set(self):
        return super(eq_ir_attachment_agorum_ext, self)._data_set(False, self.datas, False)
    
    
    @api.model
    def _file_read(self, fname, id, agorum_uuid, bin_size=False):
        """
        If an Agorum uuid is set for the attachment, the document is loaded from Agorum
        """
        
        if (agorum_uuid):
            agorum_settings = self.get_agorum_settings(self._uid);
            settings_ok = self.check_settings(agorum_settings)
            if (settings_ok):
                agorum_handler = eq_agorum_functions.eq_agorum_functions(agorum_settings)
                
                #user = 'p.exler'
                
                login_settings = {
                                  'agorum_user':agorum_settings.user,
                                  'agorum_password':agorum_settings.pw,
                                  #'as_user':user
                                  }
                """
                TODO: login with token
                try:
                    create_token_result = agorum_handler.create_token(login_settings)
                except Exception, e:
                    print 'Error in create: ' + e.message
                    return
                
          
                if (not create_token_result or not create_token_result.success):
                    #TODO: Error
                    print 'return'
                    return
                   
                login_settings = {
                                  'agorum_user':user,
                                  'agorum_token': create_token_result.token,
                                  }
                """
                
                login_with_token_result = agorum_handler.login(login_settings)
                session_id = login_with_token_result.sessionID
                get_file_result = agorum_handler.get_file(agorum_uuid, session_id)
                if (get_file_result and (get_file_result.success)):
                    file_data = get_file_result.content
                    enc_data = base64.b64encode(file_data)
                    return enc_data
                else:
                    #Show error
                    print 'Error: ' + get_file_result.message
                    return super(eq_ir_attachment_agorum_ext, self)._file_read(fname, bin_size)
            else:
                return super(eq_ir_attachment_agorum_ext, self)._file_read(fname, bin_size)    
        else:
            return super(eq_ir_attachment_agorum_ext, self)._file_read(fname, bin_size)
    
    @api.one
    def unlink(self):
        
        for attach in self:#.browse(ids):
            fname = attach.store_fname
            id = attach.id
            uuid = attach.agorum_uuid
            
            delete_ok = True
            if (uuid):
                delete_ok = self._file_delete(id, uuid)
            if (delete_ok):
                super(eq_ir_attachment_agorum_ext, self).unlink()
       
    
    @api.model
    def _file_delete(self, id, agorum_uuid = False):
        delete_ok = True
        if (agorum_uuid):
            delete_ok = False
            agorum_settings = self.get_agorum_settings(self._uid);
            settings_ok = self.check_settings(agorum_settings)
            if (settings_ok):
                agorum_handler = eq_agorum_functions.eq_agorum_functions(agorum_settings)
                
                #user = 'p.exler'
                
                login_settings = {
                                  'agorum_user':agorum_settings.user,
                                  'agorum_password':agorum_settings.pw,
                                  #'as_user':user
                                  }
                
                login_with_token_result = agorum_handler.login(login_settings)
                session_id = login_with_token_result.sessionID
                delete_result = agorum_handler.delete_file(agorum_uuid, session_id)
                if (delete_result and (delete_result.success or not delete_result.object_found)):
                    delete_ok = True
        return delete_ok
    
    def file_exists(self, uuid):
        pass
    
    
    
    