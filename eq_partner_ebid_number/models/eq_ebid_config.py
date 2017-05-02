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

class eq_ebid_config(models.TransientModel):
    _name = 'eq.ebid.config'
    _inherit = 'res.config.settings'
    
    eq_ebid_service_match_url = fields.Char(string="Match service", required=True)
    eq_ebid_service_company_url = fields.Char(string="Company service")
    eq_ebid_homepage = fields.Char("Homepage Unternehmensverzeichnis", required=True)
    eq_ebid_user = fields.Char("User", required=True)
    eq_ebid_pw = fields.Char(string ="Password", required=True)
    eq_ebid_acceptance_rate = fields.Integer("Acceptance rate")
    
    """ Ebid get function """
    @api.multi
    def get_default_eq_ebid_data(self):
        config_parameters = self.env["ir.config_parameter"]
        company_url = config_parameters.get_param("eq.ebid.service.company.url") or 'https://matching.unternehmensverzeichnis.org/ws/company/rest/v1.0/'
        match_url = config_parameters.get_param("eq.ebid.service.match.url") or 'https://matching.unternehmensverzeichnis.org/ws/match/rest/v1.0'
        homepage = config_parameters.get_param("eq.ebid.homepage.url") or 'http://www.unternehmensverzeichnis.org/'
        user = config_parameters.get_param("eq.ebid.user")
        pw = config_parameters.get_param("eq.ebid.pw")
        acceptance_rate = config_parameters.get_param("eq.ebid.acceptance.rate") or 90
        return {
                'eq_ebid_service_company_url': company_url,
                'eq_ebid_service_match_url': match_url,
                'eq_ebid_homepage': homepage,
                'eq_ebid_user': user,
                'eq_ebid_pw': pw,
                'eq_ebid_acceptance_rate': int(acceptance_rate),
                }
        
    """ Ebid set function  """    
    @api.multi
    def set_eq_ebid_data(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config_parameters.set_param("eq.ebid.service.company.url", record.eq_ebid_service_company_url or '',)
            config_parameters.set_param("eq.ebid.service.match.url", record.eq_ebid_service_match_url or '',)
            config_parameters.set_param("eq.ebid.homepage.url", record.eq_ebid_homepage or '',)
            config_parameters.set_param("eq.ebid.user", record.eq_ebid_user or '',)
            config_parameters.set_param("eq.ebid.pw", record.eq_ebid_pw or '',)
            config_parameters.set_param("eq.ebid.acceptance.rate", record.eq_ebid_acceptance_rate or 0,)
    