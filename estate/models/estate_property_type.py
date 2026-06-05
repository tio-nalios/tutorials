from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'The type of the property.'

    name = fields.Char(required=True)