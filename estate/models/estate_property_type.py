from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'The type of the property.'
    _order = 'name'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=0)

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    _check_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name of the property type must be unique.'
    )