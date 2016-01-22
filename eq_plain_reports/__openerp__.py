{
    'name': 'EQ Plain Reports',
    'description': 'Reports ohne Header und Footer',
    #'image': 'Clean_description.jpg',
    'category': 'Reports',
    'version': '1.0.0',
    'author': 'Equitania GmbH',
    'depends': ['equitania'],
    'data': [
        #'views/eq_website_templates.xml',
        'views/report_global_footer_plain.xml',
        'views/report_global_plain.xml',
        'views/report_invoice_plain.xml',
        'views/report_sale_order_plain.xml',
    ],
    'application': True,
}
