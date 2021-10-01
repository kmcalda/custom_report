# -*- coding: utf-8 -*-
{
    'name': "Custom Report",
    'summary': """
        Module for report""",
    'author': "Kevin Marvin Calda",
    'category': 'Extra tool',
    'version': '13.0',
    'license': 'AGPL-3',
    'depends': ['base', 'sale_management', 'stock', 'contacts', 'account', ],
    'data': [
        'views/menu.xml',
        'views/web_asset_backend_template.xml',
        'security/security.xml'
    ],
    'qweb': ["static/src/xml/report_view.xml"],
    'application': True,
    'installation': True,
    'auto_install': False,
}
