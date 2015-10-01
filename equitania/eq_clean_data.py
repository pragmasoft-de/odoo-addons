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

from openerp import models, fields, api

class eq_clean_data(models.TransientModel):
    _name = 'eq.clean.data'
    
    @api.model
    def remove_unwanted_data(self):
        cr = self.env.cr
        data_pool = self.pool['ir.model.data']
        cr.execute("""DELTE FROM ir_module_module WHERE state = 'uninstalled'""")
        cr.execute("""SELECT DISTINCT(model) FROM ir_model_data""")
        for (model,) in cr.fetchall():
            if not model:
                continue
            if not self.pool.get(model):
                continue
            cr.execute(
                """
                DELETE FROM ir_model_data
                WHERE model = %%s
                AND res_id IS NOT NULL
                AND NOT EXISTS (
                    SELECT id FROM %s WHERE id=ir_model_data.res_id)
                """ % self.pool[model]._table, (model,))
        print "Update finished!"
        return True