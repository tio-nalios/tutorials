from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'The type of the property.'
    _order = 'name'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=0)

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Number of Offers')

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _check_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name of the property type must be unique.'
    )