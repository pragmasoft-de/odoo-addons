# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2007 Ferran Pegueroles <ferran@pegueroles.com>
#    Copyright (c) 2009 Albert Cervera i Areny <albert@nan-tic.com>
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2013 Camptocamp (<http://www.camptocamp.com>)
#    Copyright (C) 2014 equitania (<http://www.equitania.de>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Report to printer",
    'version': '0.1.2',
    'category': 'Generic Modules/Base',
    'description': """
Report to printer
-----------------
This module allows users to send reports to a printer attached to the server.


It adds an optional behaviour on reports to send it directly to a printer.

* `Send to Client` is the default behavious providing you a downloadable PDF
* `Send to Printer` prints the report on selected printer

Report behaviour is defined by settings.


Settings can be configured:

* globaly
* per user
* per report
* per user and report


After installing enable the "Printing / Print Operator" option under access
rights to give users the ability to view the print menu.


To show all available printers for your server, use
'Settings/Printing/Update Printers' from CUPS wizard.


Then goto the user profile and set the users printing action and default
printer.


Dependencies
------------

This module requires pycups
https://pypi.python.org/pypi/pycups

    """,
    'author': 'inetplus',
    'website': 'http://www.inetplus.de',
    'license': 'AGPL-3',
    "depends": ['base','report'],
    'data': [
        'security/security.xml',
        'printing_data.xml',
        'printing_view.xml',
        'wizard/update_printers.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'external_dependencies': {
        'python': ['cups']
        }
}
