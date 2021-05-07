#!/usr/bin/python

import xmlrpclib

usernameFrom = 'admin'                  # Odoo From user
pwdFrom = 'admin'                       # Odoo From password
dbFrom = 'odoo'                         # Odoo From base de datos
urlFrom = 'http://localhost:8069'       # Odoo From URL

usernameTo = 'admin'                    # Odoo To user
pwdTo = 'admin'                         # Odoo To password
dbTo = 'odoo'                           # Odoo To base de datos
urlTo = 'http://localhost:8069'         # Odoo To URL

commonFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlFrom))
commonFrom.version()
uidFrom = commonFrom.authenticate(dbFrom, usernameFrom, pwdFrom, {})

commonTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlTo))
commonTo.version()
uidTo = commonTo.authenticate(dbTo, usernameTo, pwdTo, {})

modelsFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlFrom))
modelsTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlTo))
partner_ids_from = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'res.partner', 'search', [[]])   # Ajustar dominio de búsqueda de acuerdo a las necesidades

print(partner_ids_from)

for partner_id in partner_ids_from:
    print(partner_id)
    from_partner = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'res.partner', 'read', [partner_id], {'fields': ['name', 'country_id']})
    to_partner = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'res.partner', 'create', [{
        'name': from_partner['name']
    }])
    print(to_partner)