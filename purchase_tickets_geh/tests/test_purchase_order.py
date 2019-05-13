# Copyright <2019> <BerrySoft MX>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime
from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF

import logging

_logger = logging.getLogger(__name__)


class TestTicket(common.TransactionCase):

    def setUp(self):
        super(TestTicket, self).setUp()

        # Set environment variables
        self.TICKET = self.env['purchase.ticket']

        self.res_company_id = self.ref('base.main_company')
        self.today = datetime.today()

        self.purchase_ticket_1_id = self.ref(
            'purchase_tickets_geh.ticket_1_demo')
        self.purchase_ticket_1 = self.env['purchase.ticket'].search(
            [('id', '=', self.purchase_ticket_1_id)])

    def test_00_create_ticket(self):
        # In order to test process of the ticket, create ticket
        self.purchase_ticket_2 = self.TICKET.create(
            {'name': 'hb-prueba-cxp-0002',
             'company_id': self.res_company_id})

        # Validations
        self.assertTrue(self.purchase_ticket_2, 'Ticket: no ticket created')
        self.assertEqual(self.purchase_ticket_2.name, 'hb-prueba-cxp-0002',
                         'Ticket: ticket name is wrong')
        self.assertEqual(self.purchase_ticket_2.company_id.id,
                         self.res_company_id,
                         'Ticket: ticket company is wrong')
        self.assertFalse(self.purchase_ticket_2.date,
                         'Ticket: the ticket must not have a date')

    def test_01_update_ticket(self):
        # In order to test process of the ticket, update ticket adding a date
        self.purchase_ticket_1.write(
            {'date': self.today.strftime(DF)})

        # Validations
        self.assertEqual(self.purchase_ticket_1.date, self.today.strftime(DF),
                         'Ticket: ticket date is wrong')

    def test_02_delete_ticket(self):
        # In order to test process of the ticket, create the ticket
        self.purchase_ticket_2 = self.TICKET.create(
            {'name': 'hb-prueba-cxp-0002',
             'company_id': self.res_company_id})

        # Deleting the ticket
        self.purchase_ticket_2.unlink()

        # Validations
        self.assertFalse(self.purchase_ticket_2.exists(),
                         'Ticket: Ticket must be deleted but it still exists')


class TestPurchaseOrder(common.TransactionCase):
    def setUp(self):
        super(TestPurchaseOrder, self).setUp()

        # Set record variables
        self.product_09_id = self.ref('product.product_product_9')
        self.product_09 = self.env['product.product'].search(
            [('id', '=', self.product_09_id)], limit=1)
        self.product_13_id = self.ref('product.product_product_13')
        self.product_13 = self.env['product.product'].search(
            [('id', '=', self.product_13_id)], limit=1)
        self.res_partner_1_id = self.ref('base.res_partner_1')
        self.res_company_id = self.ref('base.main_company')

        self.purchase_ticket_1_id = self.ref(
            'purchase_tickets_geh.ticket_1_demo')
        self.purchase_ticket_1 = self.env['purchase.ticket'].search(
            [('id', '=', self.purchase_ticket_1_id)])

        self.today = datetime.today()

        # Set environment variables
        self.TICKET = self.env['purchase.ticket']
        self.INVOICE = self.env['account.invoice']
        self.PURCHASE_ORDER = self.env['purchase.order']
        self.PURCHASE_ORDER_LINE = self.env['purchase.order.line']

        self.po_vals = {
            'partner_id': self.res_partner_1_id,
            'order_line': [
                (0, 0, {
                    'name': self.product_09.name,
                    'product_id': self.product_09_id,
                    'product_qty': 5.0,
                    'product_uom': self.product_09.uom_po_id.id,
                    'ticket_id': self.purchase_ticket_1_id,
                    'price_unit': 500.0,
                    'date_planned': datetime.today().strftime(
                        DF),
                }),
                (0, 0, {
                    'name': self.product_13.name,
                    'product_id': self.product_13_id,
                    'product_qty': 5.0,
                    'product_uom': self.product_13.uom_po_id.id,
                    'price_unit': 250.0,
                    'date_planned': datetime.today().strftime(
                        DF),
                })],
        }

    def test_00_create_purchase_order(self):
        # Create a new purchase order with a ticket id in lines

        self.purchase_order_2 = self.PURCHASE_ORDER.create(self.po_vals)

        # Validations
        self.assertTrue(self.purchase_order_2.ticket_ids.filtered(
            lambda r: r.id == self.purchase_ticket_1_id),
            'Ticket: Ticket was not added to ticket ids of '
            'the PO from PO line'
        )


class TestPurchaseOrderLine(common.TransactionCase):
    def setUp(self):
        super(TestPurchaseOrderLine, self).setUp()

        self.res_partner_1_id = self.ref('base.res_partner_1')
        self.product_09_id = self.ref('product.product_product_9')
        self.product_09 = self.env['product.product'].search(
            [('id', '=', self.product_09_id)], limit=1)
        self.product_13_id = self.ref('product.product_product_13')
        self.product_13 = self.env['product.product'].search(
            [('id', '=', self.product_13_id)], limit=1)
        self.purchase_ticket_1_id = self.ref(
            'purchase_tickets_geh.ticket_1_demo')
        self.purchase_ticket_1 = self.env['purchase.ticket'].search(
            [('id', '=', self.purchase_ticket_1_id)])

        # Set environment variables
        self.TICKET = self.env['purchase.ticket']
        self.PURCHASE_ORDER_LINE = self.env['purchase.order.line']
        self.PURCHASE_ORDER = self.env['purchase.order']

        # Values for purchase order
        self.po_vals = {
            'partner_id': self.res_partner_1_id,
            'order_line': [
                (0, 0, {
                    'name': self.product_09.name,
                    'product_id': self.product_09_id,
                    'product_qty': 5.0,
                    'product_uom': self.product_09.uom_po_id.id,
                    'ticket_id': self.purchase_ticket_1.id,
                    'price_unit': 500.0,
                    'date_planned': datetime.today().strftime(
                        DF),
                }),
                (0, 0, {
                    'name': self.product_13.name,
                    'product_id': self.product_13_id,
                    'product_qty': 5.0,
                    'product_uom': self.product_13.uom_po_id.id,
                    'price_unit': 250.0,
                    'date_planned': datetime.today().strftime(
                        DF),
                })],
        }

        self.purchase_order_1 = self.PURCHASE_ORDER.create(
            self.po_vals)
        self.res_company_id = self.ref('base.main_company')
        self.today = datetime.today()

    def test_00_create_purchase_order_line(self):
        # In order to test process of the pol, create pol with ticket id
        self.poline1 = self.PURCHASE_ORDER_LINE.create({
            'name': 'Esto es una linea de pedido de prueba',
            'order_id': self.purchase_order_1.id,
            'product_id': self.product_09_id,
            'ticket_id': self.purchase_ticket_1_id,
            'price_unit': 20.0,
            'product_qty': 10.0,
            'product_uom': self.product_09.uom_po_id.id,
            'date_planned': self.today.strftime(DF)
        })

        # Validations
        self.assertTrue(self.poline1.ticket_id, 'Purchase Order Line: Ticket '
                                                'id was not saved on PO line')

        self.assertTrue(self.poline1.order_id.ticket_ids.filtered(
            lambda r: r.id == self.purchase_ticket_1.id),
            'Ticket: Ticket was not added to ticket ids '
            'of the PO from PO line')
