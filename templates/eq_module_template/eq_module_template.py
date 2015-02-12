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

#Old API, Remove New API import if the Old API is used. Otherwise you'll get an import error.
from openerp.osv import fields, osv, orm
#Translation for the Old API. Remove it too.
from openerp.tools.translate import _
#New API, Remove Old API import if the New API is used. Otherwise you'll get an import error.
from openerp import models, fields, api, _

class eq_module_template(osv.Model):
    _name = 'eq_module_template'
    
    _columns = {
                'your_field': fields.char('Your Fieldname', size=64)
                }
    

class eq_module_template_second_class(osv.Model):
    _name = 'eq_module_template.second_class'
    
    _columns = {
                'your_field_of_second_class': fields.char('Your Fieldname', size=64)
                }