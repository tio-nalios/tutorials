from odoo import fields, models, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer made by a potential buyer on an estate property.'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date( # equal to False when create_date or validity is not set
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True
    )
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.validity:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = 0

    # Set the state of the property to "offer_received" when an offer is created
    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            offer.property_id.state = 'offer_received'
        return offers

    def action_accept(self):
        for offer in self:
            offer.status = 'accepted'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            # Refuse all other offers
            other_offers = self.search([
                ('property_id', '=', offer.property_id.id),
                ('id', '!=', offer.id)
            ])
            other_offers.write({'status': 'refused'})
        return True
    
    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True
    
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The price must be strictly positive.'
    )