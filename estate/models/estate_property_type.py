from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'The type of the property.'

    name = fields.Char(required=True)

    _check_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name of the property type must be unique.'
    )