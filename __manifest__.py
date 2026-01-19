# -*- coding: utf-8 -*-
{
    'name': 'Gestion des Garanties Professionnelle',
    'version': '1.1.0',
    'summary': 'Module avancé de gestion des garanties produits avec automatisation et intégration',
    'category': 'Sales',
    'author': 'Manus (Amélioré)',
    'website': 'http://manus.im',
    'depends': ['base', 'sale', 'product', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/cron.xml',
        'views/views.xml',
        'views/product_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
