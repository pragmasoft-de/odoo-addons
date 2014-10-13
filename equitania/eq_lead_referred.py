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

from openerp.osv import fields, osv, orm

class eq_lead(osv.osv):
    _inherit = 'crm.lead'
    
    _columns = {
        'eq_lead_referred_id': fields.many2one('eq.lead.referred', 'Referred By'),
    }
        
eq_lead()


class eq_lead_referred(osv.osv):
    _name = "eq.lead.referred"
    _rec_name = "eq_description"
    
    _columns = {
        'eq_description': fields.char('Description'),        
    }

eq_lead_referred()