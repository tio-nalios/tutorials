{
    'name': 'Real Estate',
    'category': 'Sales/Real Estate',
    'installable': True,
    'application': True,
    'author': 'Tim Olde',
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        
        # put menus last because actions need to be defined first
        'views/estate_property_menus.xml',
    ]
}