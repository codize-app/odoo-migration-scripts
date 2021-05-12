#!/usr/bin/python
# encoding: utf-8

import xmlrpclib

usernameFrom = 'admin'                  # Odoo From user
pwdFrom = 'admin'                       # Odoo From password
dbFrom = 'odoo'                         # Odoo From base de datos
urlFrom = 'http://localhost:8069'       # Odoo From URL

usernameTo = 'admin'                    # Odoo To user
pwdTo = 'admin'                         # Odoo To password
dbTo = 'odoo'                           # Odoo To base de datos
urlTo = 'http://localhost:8069'         # Odoo To URL

valsFrom = {'fields': ['name', 'street', 'street', 'city', 'state_id', 'country_id']}

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
    from_partner = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'res.partner', 'read', [partner_id], valsFrom)

    print(from_partner[0])

    if from_partner[0]['state_id']:
        state_id = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'res.country.state', 'search', [[['name', '=', from_partner[0]['state_id'][1]]]], {'limit': 1})
    else:
        state_id = False

    if from_partner[0]['country_id']:
        country_id = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'res.country', 'search', [[['name', '=', from_partner[0]['country_id'][1]]]], {'limit': 1})
    else:
        country_id = False

    to_partner = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'res.partner', 'create', [{
        'name': from_partner['name'],
        'street': from_partner['street'],
        'street2': from_partner['street2'],
        'city': from_partner['city'],
        'state_id': state_id[0],
        'country_id': country_id[0]
    }])
    print(to_partner)
