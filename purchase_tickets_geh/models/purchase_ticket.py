# Copyright <2019> <BerrySoft MX>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

class Ticket(models.Model):
    _name = "purchase.ticket"

    name = fields.Char(string='Folio')
    date = fields.Datetime(string='Fecha de realización')
    company_id = fields.Many2one(comodel_name='res.company', string="Compañía",
                                 related='create_uid.company_id')
