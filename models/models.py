# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class GestionGarantie(models.Model):
    _name = 'gestion.garantie'
    _description = 'Gestion des Garanties'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(
        string='Numéro de Garantie',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        tracking=True,
        help='Le client concerné par la garantie'
    )

    product_id = fields.Many2one(
        'product.product',
        string='Produit',
        required=True,
        tracking=True,
        help='Le produit sous garantie'
    )

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Bon de Commande',
        store=False,
        help='La vente liée à cette garantie'
    )

    serial_number = fields.Char(
        string='Numéro de Série',
        required=True,
        tracking=True,
        help='Numéro de série unique du produit'
    )

    purchase_date = fields.Date(
        string='Date d\'Achat',
        required=True,
        default=fields.Date.today,
        tracking=True,
        help='La date à laquelle le produit a été acheté'
    )

    duration_months = fields.Integer(
        string='Durée de Garantie (Mois)',
        required=True,
        default=12,
        tracking=True,
        help='La durée de la garantie en mois'
    )

    expiration_date = fields.Date(
        string='Date d\'Expiration',
        compute='_compute_expiration_date',
        store=True,
        readonly=True,
        tracking=True,
        help='Date calculée de fin de garantie'
    )

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
        tracking=True,
        help='État actuel de la garantie'
    )

    problem_description = fields.Text(
        string='Description du Problème',
        help='Description du défaut ou du problème en cas de réclamation'
    )

    _sql_constraints = [
        ('serial_number_unique', 'UNIQUE(serial_number)', 
         'Le numéro de série doit être unique !'),
        ('duration_positive', 'CHECK(duration_months > 0)', 
         'La durée de garantie doit être positive !'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('gestion.garantie') or _('New')
        return super(GestionGarantie, self).create(vals_list)

    @api.depends('purchase_date', 'duration_months')
    def _compute_expiration_date(self):
        for record in self:
            if record.purchase_date and record.duration_months:
                record.expiration_date = record.purchase_date + relativedelta(
                    months=record.duration_months
                )
            else:
                record.expiration_date = False

    @api.constrains('purchase_date')
    def _check_purchase_date(self):
        for record in self:
            if record.purchase_date and record.purchase_date > fields.Date.today():
                raise ValidationError(_("La date d'achat ne peut pas être dans le futur !"))

    def action_validate(self):
        """Valider la garantie avec vérification de sécurité pour la base de données."""
        self.env.cr.execute("SELECT column_name FROM information_schema.columns WHERE table_name='gestion_garantie' AND column_name='sale_order_id'")
        column_exists = self.env.cr.fetchone()
        
        today = fields.Date.today()
        for record in self:
            # Si la colonne n'existe pas encore, on évite de charger le record complet
            if not column_exists:
                # Logique simplifiée sans charger les champs potentiellement manquants
                self.env.cr.execute("UPDATE gestion_garantie SET state='valid' WHERE id=%s", (record.id,))
                continue

            if not record.expiration_date:
                record._compute_expiration_date()
            
            if record.expiration_date and record.expiration_date < today:
                record.write({'state': 'expired'})
            else:
                record.write({'state': 'valid'})
        return True

    def action_mark_expired(self):
        self.write({'state': 'expired'})
        return True

    def action_create_claim(self):
        self.ensure_one()
        if not self.problem_description:
            raise ValidationError(
                _("Veuillez décrire le problème avant de créer une réclamation !")
            )
        self.write({'state': 'claim'})
        return True

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
        return True

    @api.model
    def _cron_check_expiration(self):
        """Méthode appelée par le cron pour expirer les garanties automatiquement."""
        today = fields.Date.today()
        expired_garanties = self.search([
            ('state', '=', 'valid'),
            ('expiration_date', '<', today)
        ])
        if expired_garanties:
            expired_garanties.write({'state': 'expired'})
            for garantie in expired_garanties:
                garantie.message_post(body=_("La garantie a expiré automatiquement le %s.") % today)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    garantie_ids = fields.One2many(
        'gestion.garantie', 
        'product_id', 
        string='Garanties Associées'
    )
    garantie_count = fields.Integer(
        compute='_compute_garantie_count', 
        string='Nombre de Garanties'
    )

    def _compute_garantie_count(self):
        for record in self:
            record.garantie_count = self.env['gestion.garantie'].search_count([
                ('product_id.product_tmpl_id', '=', record.id)
            ])

    def action_view_garanties(self):
        self.ensure_one()
        return {
            'name': _('Garanties'),
            'type': 'ir.actions.act_window',
            'res_model': 'gestion.garantie',
            'view_mode': 'list,form',
            'domain': [('product_id.product_tmpl_id', '=', self.id)],
            'context': {'default_product_id': self.env['product.product'].search([('product_tmpl_id', '=', self.id)], limit=1).id},
        }

class ResPartner(models.Model):
    _inherit = 'res.partner'

    garantie_ids = fields.One2many(
        'gestion.garantie', 
        'partner_id', 
        string='Garanties'
    )
    garantie_count = fields.Integer(
        compute='_compute_garantie_count', 
        string='Nombre de Garanties'
    )

    def _compute_garantie_count(self):
        for record in self:
            record.garantie_count = len(record.garantie_ids)

    def action_view_garanties(self):
        self.ensure_one()
        return {
            'name': _('Garanties'),
            'type': 'ir.actions.act_window',
            'res_model': 'gestion.garantie',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }
