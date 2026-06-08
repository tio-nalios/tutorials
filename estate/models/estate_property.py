from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
                ('north', 'North'),
                ('south', 'South'),
                ('east', 'East'),
                ('west', 'West')
            ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection = [
                ('new', 'New'),
                ('offer_received', 'Offer Received'),
                ('offer_accepted', 'Offer Accepted'),
                ('sold', 'Sold'),
                ('cancelled', 'Cancelled')
            ],
        required=True,
        copy=False,
        default='new'
    )

    property_type_id = fields.Many2one(comodel_name='estate.property.type')
    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer',
        copy=False
    )
    salesperson_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', copy=False)

    best_price = fields.Float(compute='_compute_best_price', string='Best Offer')

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.mapped('offer_ids.price') or [0])

    total_area = fields.Float(compute='_compute_total_area', string='Total Area')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'

    @api.ondelete(at_uninstall=False)
    def _ondelete_check_state(self):
        if any(record.state not in ['new', 'cancelled'] for record in self):
            raise UserError('You can only delete properties that are new or cancelled.')

    def action_sold(self):
        for record in self:
            if record.state != 'offer_accepted':
                raise UserError('Only properties with an accepted offer can be sold.')
            record.state = 'sold'
        return True
    
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be cancelled.')
            record.state = 'cancelled'
        return True
    
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.'
    )
    # Not necessary anymore because selling_price can already not be lower than 90% of expected_price but I'm leaving it as an example
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price cannot be negative.'
    )
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.selling_price < 0.9 * record.expected_price:
                raise ValidationError('The selling price cannot be lower than 90% of the expected price.')