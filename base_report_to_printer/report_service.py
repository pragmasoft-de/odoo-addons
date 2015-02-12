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
import base64
import openerp
from openerp import api
from openerp.osv import osv
from openerp.exceptions import Warning

import logging

_logger = logging.getLogger(__name__)

class Report(osv.Model):
    _inherit = "report"

    @api.v7
    def get_pdf(self, cr, uid, ids, report_name, html=None, data=None, context=None):
        pdf = super(Report, self).get_pdf(cr, uid, ids, report_name,
                                   html=html, data=data, context=context)
        try:
            report_obj = self.pool.get('ir.actions.report.xml')
            report = report_obj.search(cr, uid, [('report_name', '=', report_name)])
            if report:
                report = report_obj.browse(cr, uid, report[0])
                data = report.behaviour()[report.id]
                action = data['action']
                printer = data['printer']
                if action != 'client':
                    report_obj.print_direct(cr, uid, report.id, base64.encodestring(pdf),'pdf', printer)
        except Exception, e:
            _logger.error(e)
        return pdf


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
