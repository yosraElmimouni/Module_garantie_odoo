# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class GestionGarantie(models.Model):
    _name = 'gestion.garantie'
    _description = 'Gestion des Garanties'
    _order = 'create_date desc'

    # Champs de base
    name = fields.Char(
        string='Numéro de Garantie',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default='/'
    )

    # Relations
    partner_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        help='Le client concerné par la garantie'
    )

    product_id = fields.Many2one(
        'product.product',
        string='Produit',
        required=True,
        help='Le produit sous garantie'
    )

    # Champs de garantie
    serial_number = fields.Char(
        string='Numéro de Série',
        required=True,
        help='Numéro de série unique du produit'
    )

    purchase_date = fields.Date(
        string='Date d\'Achat',
        required=True,
        default=fields.Date.today,
        help='La date à laquelle le produit a été acheté'
    )

    duration_months = fields.Integer(
        string='Durée de Garantie (Mois)',
        required=True,
        default=12,
        help='La durée de la garantie en mois'
    )

    expiration_date = fields.Date(
        string='Date d\'Expiration',
        compute='_compute_expiration_date',
        store=True,
        readonly=True,
        help='Date calculée de fin de garantie'
    )

    # Statut et description
    state = fields.Selection(
        [
            ('draft', 'Brouillon'),
            ('valid', 'Valide'),
            ('expired', 'Expirée'),
            ('claim', 'Réclamation en cours'),
        ],
        string='Statut',
        default='draft',
        required=True,
        help='État actuel de la garantie'
    )

    problem_description = fields.Text(
        string='Description du Problème',
        help='Description du défaut ou du problème en cas de réclamation'
    )

    # Contraintes SQL
    _sql_constraints = [
        ('serial_number_unique', 'UNIQUE(serial_number)', 
         'Le numéro de série doit être unique !'),
        ('duration_positive', 'CHECK(duration_months > 0)', 
         'La durée de garantie doit être positive !'),
    ]

    def _get_or_create_sequence(self):
        """Récupère ou crée la séquence pour les numéros de garantie"""
        IrSequence = self.env['ir.sequence'].sudo()
        
        # Chercher la séquence existante
        sequence = IrSequence.search([('code', '=', 'gestion.garantie')], limit=1)
        
        # Si elle n'existe pas, la créer
        if not sequence:
            sequence = IrSequence.create({
                'name': 'Numéro de Garantie',
                'code': 'gestion.garantie',
                'implementation': 'standard',
                'active': True,
                'prefix': 'GAR/%(year)s/',
                'padding': 5,
                'number_next': 1,
                'number_increment': 1,
            })
        
        return sequence

    @api.model_create_multi
    def create(self, vals_list):
        """Générer automatiquement le numéro de garantie"""
        for vals in vals_list:
            if not vals.get('name') or vals.get('name') == '/':
                # Récupérer ou créer la séquence
                sequence = self._get_or_create_sequence()
                
                # Générer le numéro
                vals['name'] = sequence._next()
                
        return super(GestionGarantie, self).create(vals_list)

    @api.depends('purchase_date', 'duration_months')
    def _compute_expiration_date(self):
        """Calcule la date d'expiration basée sur la date d'achat et la durée."""
        for record in self:
            if record.purchase_date and record.duration_months:
                record.expiration_date = record.purchase_date + relativedelta(
                    months=record.duration_months
                )
            else:
                record.expiration_date = False

    @api.constrains('purchase_date')
    def _check_purchase_date(self):
        """Vérifie que la date d'achat n'est pas dans le futur"""
        for record in self:
            if record.purchase_date and record.purchase_date > fields.Date.today():
                raise ValidationError("La date d'achat ne peut pas être dans le futur !")



    def action_validate(self):
        """Valider la garantie."""
        today = fields.Date.today()
        for record in self:
            if record.expiration_date and record.expiration_date < today:
                raise ValidationError("Impossible de valider une garantie expirée !")
            record.write({'state': 'valid'})
        return True

    def action_mark_expired(self):
        """Marquer la garantie comme expirée."""
        self.write({'state': 'expired'})
        return True

    def action_create_claim(self):
        """Créer une réclamation pour la garantie."""
        self.ensure_one()
        if not self.problem_description:
            raise ValidationError(
                "Veuillez décrire le problème avant de créer une réclamation !"
            )
        self.write({'state': 'claim'})
        return True

    def action_reset_to_draft(self):
        """Réinitialiser la garantie au statut brouillon."""
        self.write({'state': 'draft'})
        return True