# -*- coding: utf-8 -*-

def post_init_hook(env):
    """Hook appelé après l'installation du module"""
    # Vérifier si la séquence existe déjà
    sequence = env['ir.sequence'].search([('code', '=', 'gestion.garantie')], limit=1)
    
    if not sequence:
        # Créer la séquence
        env['ir.sequence'].create({
            'name': 'Numéro de Garantie',
            'code': 'gestion.garantie',
            'prefix': 'GAR/%(year)s/',
            'padding': 5,
            'number_next': 1,
            'number_increment': 1,
            'implementation': 'standard',
        })
        print("✅ Séquence 'gestion.garantie' créée avec succès !")
    else:
        print("ℹ️ La séquence 'gestion.garantie' existe déjà.")