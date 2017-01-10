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
from datetime import timedelta
from openerp.exceptions import ValidationError

class project_task_work(models.Model):
    _inherit = 'project.task.work'
    
    eq_to_invoice = fields.Many2one(comodel_name='hr_timesheet_invoice.factor', related="hr_analytic_timesheet_id.to_invoice",
                    string='Timesheet Invoicing Ratio', default=1)

    eq_time_start = fields.Float(string='Begin Hour')
    eq_time_stop = fields.Float(string='End Hour')

    @api.constrains('eq_time_stop', 'eq_time_start')
    def _check_time_input(self):
        if self.eq_time_start < 0 or self.eq_time_start >= 24 or self.eq_time_stop < 0 or self.eq_time_stop >= 24:
            raise ValidationError(_("Input for the time must be between 0 and 24 hours"))
        #     return False
        # return True

    # _constraints = [
    #     (_check_time_input, 'Error! You cannot create recursive Categories.', ['eq_time_start','eq_time_stop'])
    # ]




    @api.onchange('eq_time_start', 'eq_time_stop')
    def onchange_hours_start_stop(self):
        """
        Berechnung der geleisteten Zeit anhand des Start- und Endzeitpunktes
        :return:
        """

        #return {'warning': {'title': 'Error!', 'message': 'Something went wrong! Please check your data'}}

        start = timedelta(hours=self.eq_time_start)
        stop = timedelta(hours=self.eq_time_stop)
        if stop < start:
            return
        self.hours = float((stop - start).seconds) / 3600

    @api.model
    def _create_analytic_entries(self, vals):
        """
        overriding from project_timesheet.py um neue Felder zu setzen
        :param vals:
        :return:
        """
        timeline_id = super(project_task_work, self)._create_analytic_entries(vals)  #calls timesheet_obj.create
        if timeline_id:
            timesheet_obj = self.env['hr.analytic.timesheet']
            timeline_rec = timesheet_obj.browse(timeline_id)

            update_vals = {}
            if 'eq_time_start' in vals:
                update_vals['time_start'] = vals['eq_time_start']
                update_vals['aal_time_start'] = vals['eq_time_start']

            if 'eq_time_stop' in vals:
                update_vals['time_stop'] = vals['eq_time_stop']
                update_vals['aal_time_stop'] = vals['eq_time_stop']

            if update_vals:
                timeline_rec.write(update_vals)

        return timeline_id

    @api.multi
    def write(self, vals):
        """

        :param vals:
        :return:
        """
        #führt in project_timesheet.py zu einem write in hr.analytic.timesheet
        #Fehler durch Validierung beim Write falls berechnete Stundenzahl nicht das Ergebnis von Start- und Endzeitpunkt ist
        #Zeiten in account_line müssen ebenfalls gesetzt werden


        #request.session['eq_project_task_work'] = True
        if self.hr_analytic_timesheet_id:
            line_id = self.hr_analytic_timesheet_id.id
            vals_line = {}
            if 'eq_time_start' in vals:
                vals_line['time_start'] = vals['eq_time_start']


            if 'eq_time_stop' in vals:
                vals_line['time_stop'] = vals['eq_time_stop']

            if 'eq_time_start' in vals:
                vals_line['aal_time_start'] = vals['eq_time_start']

            if 'eq_time_stop' in vals:
                vals_line['aal_time_stop'] = vals['eq_time_stop']

            if 'hours' in vals:
                vals_line['unit_amount'] = vals['hours']

            if vals_line:
                try:
                    vals_line['skip_project_task_update'] = True
                    timesheet = self.env['hr.analytic.timesheet'].browse(line_id)

                    diff_found = False
                    if 'eq_time_start' in vals:
                        diff_found = timesheet.aal_time_start != vals['eq_time_start']
                    if not diff_found and 'eq_time_stop' in vals:
                        diff_found = timesheet.aal_time_stop != vals['eq_time_stop']

                    if diff_found:
                        timesheet.write(vals_line)

                        analytic_line = self.env['account.analytic.line'].browse(self.hr_analytic_timesheet_id.line_id.id)
                        analytic_line.write(vals_line)
                        self.hr_analytic_timesheet_id.write(vals_line)
                except:
                    #Erweiterung "hr_timesheet_activity_begin_end" fehlt
                    pass

        return super(project_task_work, self).write(vals)
