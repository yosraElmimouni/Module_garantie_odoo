# -*- coding: utf-8 -*-
{
    'name': 'Gestion des Garanties',
    'version': '1.0.0',
    'summary': 'Module de gestion des garanties produits',
    'category': 'Sales',
    'author': 'Yosra El Mimouni',
    'website': 'http://votresite.com',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/views.xml',
    ],
    'post_init_hook': 'post_init_hook',  
    'installable': True,
    'application': True,
}