from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags to categorize and describe estate properties.'

    name = fields.Char(required=True)
    estate_property_ids = fields.Many2many('estate.property', string='Properties')

    _check__name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name of the tag must be unique.'
    )