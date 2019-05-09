# -*- coding: utf-8 -*-
{
    'name': "Tickets de compra",

    'summary': """
        Asocia pedidos de comrpa a folios de ticket.""",

    'description': """
        Permite asociar los pedidos de compra con el folio del ticket al que pertenece. Agrega el campo de ticket en el formato de impresión y envío del mismo.
    """,

    'author': "BerrySoft MX",
    'website': "http://www.berrysoft.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_invoice_views.xml',
        'views/purchase_order_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}