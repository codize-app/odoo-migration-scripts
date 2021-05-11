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

model = ''                              # Modelo de Odoo a migrar

valsFrom = {'fields': []}

commonFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlFrom))
commonFrom.version()
uidFrom = commonFrom.authenticate(dbFrom, usernameFrom, pwdFrom, {})

commonTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlTo))
commonTo.version()
uidTo = commonTo.authenticate(dbTo, usernameTo, pwdTo, {})

modelsFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlFrom))
modelsTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlTo))
ids_from = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, model, 'search', [[]])   # Ajustar dominio de búsqueda de acuerdo a las necesidades

print(ids_from)

for id_from in ids_from:
    print(id_from)
    from_id = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, model, 'read', [id_from], valsFrom)
    
    to_id = modelsTo.execute_kw(dbTo, uidTo, pwdTo, model, 'create', [{}])
    print(to_id)
