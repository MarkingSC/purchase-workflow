# Copyright <2019> <BerrySoft MX>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

class AccountInvoice(models.Model):

    _inherit ="account.invoice"

    ticket_ids = fields.Many2many(string="tickets",
                                  comodel_name='purchase.ticket')

    # Load all unsold PO lines (Replaced function)
    @api.onchange('purchase_id')
    def purchase_order_change(self):
        purchase_id = False
        if self.purchase_id:
            purchase_id = self.purchase_id
        res = super(AccountInvoice, self).purchase_order_change()
        if purchase_id:
            self.ticket_ids += purchase_id.ticket_ids
        return res