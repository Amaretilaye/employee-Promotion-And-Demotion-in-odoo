{
    'name': 'Employee Promotion And Demotion',

    'summary': 'Manage employee promotions in Odoo.',
    'category': 'Human Resources',
    'author': 'Amare Tilaye',
    'depends': ['base', 'hr'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/employee_promotion_views.xml',
        'views/employee_demotion_views.xml',
        'views/res_config_settings_views.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
