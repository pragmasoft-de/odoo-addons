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


class eq_agorum_config(models.TransientModel):
    _name = 'eq.agorum.config'
    _inherit = 'res.config.settings'
    
    eq_agorum_host = fields.Char(string="Agorum Host", required=True)
    eq_agorum_session_service = fields.Char(string="Agorum session service", required=True)
    eq_agorum_object_service = fields.Char(string="Agorum object service", required=True)
    eq_agorum_user = fields.Char(string="Agorum User")
    eq_agorum_pw = fields.Char(string="Agorum Password")
    eq_agorum_token = fields.Char(string="Agorum Token")
    eq_agorum_target_directory = fields.Char(string="Agorum target folder")
    
    """ Agorum config get function """
    @api.multi
    def get_default_eq_ebid_data(self):
        config_parameters = self.env["ir.config_parameter"]
        agorum_host = config_parameters.get_param("eq.agorum.host") or 'http://your-agorum.com'
        agorum_session_service = config_parameters.get_param("eq.agorum.session.service") or 'http://your-agorum.com/api/rest/session/'
        agorum_object_service = config_parameters.get_param("eq.agorum.object.service") or 'http://your-agorum.com/api/rest/object/'
        agorum_token = config_parameters.get_param("eq.agorum.token")
        agorum_target_directory = config_parameters.get_param("eq.agorum.target.directory")
        agorum_user = config_parameters.get_param("eq.agorum.user")
        agorum_pw = config_parameters.get_param("eq.agorum.pw")
            
        return {
                'eq_agorum_host': agorum_host,
                'eq_agorum_session_service': agorum_session_service,
                'eq_agorum_object_service': agorum_object_service,
                'eq_agorum_token': agorum_token,
                'eq_agorum_user': agorum_user,
                'eq_agorum_pw': agorum_pw,
                'eq_agorum_target_directory': agorum_target_directory,
                }
        
    """ Agorum config set function  """    
    @api.multi
    def set_eq_ebid_data(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config_parameters.set_param("eq.agorum.host", record.eq_agorum_host or '',)
            config_parameters.set_param("eq.agorum.session.service", record.eq_agorum_session_service or '',)
            config_parameters.set_param("eq.agorum.object.service", record.eq_agorum_object_service or '',)
            config_parameters.set_param("eq.agorum.token", record.eq_agorum_token or '',)
            config_parameters.set_param("eq.agorum.user", record.eq_agorum_user or '',)
            config_parameters.set_param("eq.agorum.pw", record.eq_agorum_pw or '',)
            config_parameters.set_param("eq.agorum.target.directory", record.eq_agorum_target_directory or '',)
