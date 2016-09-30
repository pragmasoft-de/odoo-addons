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

class eq_res_partner(models.Model):
    _inherit = 'res.partner'
    
    def _pos_line_count(self):
        """
        Anzeige der Anzahl der Kassenumsatzpositionen für einen Kunden
        """
        pos_line_obj = self.env['eq.pos.order.line']
        for partner in self:
            partner.eq_pos_line_count = pos_line_obj.search_count([('eq_customer','=',partner.id)])
            

    
    eq_pos_line_count = fields.Integer(compute="_pos_line_count", string='# of lines')