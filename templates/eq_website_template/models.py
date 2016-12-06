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

# definition of your tables and fields goes here

from openerp.tools.translate import _                       # Support für dyn. übersetzung
from openerp import models, fields, api
from openerp.addons.eq_office365 import eq_log              # unser Logger importieren


# Beispiel 1 -> Nur 1 Infotext in der Konsole ausgeben
#eq_log.log("Exchange-Modus")

# Beispiel 2 -> 2 Werte in der Konsole ausgeben
#eq_log.log("Anzahl kontakte:", size_contacts)

# Beispiel 3 -> Mehrere Werte in der Konsole ausgeben
#eq_log.log("Anzahl kontakte:", size_contacts, "Name: ", "Sody", "Modul:", "eq_website")

# class eq_website_template(models.Model):
#     _name = 'eq_website_template.eq_website_template'

#     name = fields.Char()




        