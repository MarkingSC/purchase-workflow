# Copyright <2019> <BerrySoft MX>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    ticket_id = fields.Many2one(comodel_name="purchase.ticket")

    @api.multi
    def write(self, values):
        """ Asocia los tickets de la línea de pedido a la orden al modificar
        lineas de pedido"""
        res = super(PurchaseOrderLine, self).write(values)
        self._compute_order_tickets(values)
        return res

    @api.model
    def create(self, values):
        """ Asocia los tickets de la línea de pedido a la orden al crear lineas
         de pedido"""
        record = super(PurchaseOrderLine, self).create(values)
        record._compute_order_tickets(values)
        return record

    @api.one
    def _compute_order_tickets(self, values):
        if 'ticket_id' in values:
            self.order_id.ticket_ids = self.order_id.order_line.mapped(
                'ticket_id'
            )


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    ticket_ids = fields.Many2many(string="tickets",
                                  comodel_name='purchase.ticket')

