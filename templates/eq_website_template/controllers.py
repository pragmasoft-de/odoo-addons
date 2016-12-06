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

from openerp.tools.translate import _                       # Support für dyn. übersetzung
from openerp import http
#from openerp.addons.eq_website_customerportal import eq_log              # unser Logger importieren


# Beispiel 1 -> Nur 1 Infotext in der Konsole ausgeben
#eq_log.log("Exchange-Modus")

# Beispiel 2 -> 2 Werte in der Konsole ausgeben
#eq_log.log("Anzahl kontakte:", size_contacts)

# Beispiel 3 -> Mehrere Werte in der Konsole ausgeben
#eq_log.log("Anzahl kontakte:", size_contacts, "Name: ", "Sody", "Modul:", "eq_website")


# OLD API
#attachments_obj = http.request.registry['ir.attachment'].sudo()

# NEW API
#attachments_obj = http.request.env['ir.attachment'].sudo()


# class EqWebsiteTemplate(http.Controller):
#     @http.route('/eq_website_template/eq_website_template/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eq_website_template/eq_website_template/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('eq_website_template.listing', {
#             'root': '/eq_website_template/eq_website_template',
#             'objects': http.request.env['eq_website_template.eq_website_template'].search([]),
#         })

#     @http.route('/eq_website_template/eq_website_template/objects/<model("eq_website_template.eq_website_template"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eq_website_template.object', {
#             'object': obj
#         })