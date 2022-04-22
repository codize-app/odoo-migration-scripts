#!/usr/bin/python
# encoding: utf-8

import xmlrpclib
import base64
import requests

def get_as_base64(url):
        return base64.b64encode(requests.get(url).content)

usernameFrom = 'admin'                  # Odoo From user
pwdFrom = 'admin'                       # Odoo From password
dbFrom = 'odoo'                         # Odoo From base de datos
urlFrom = 'http://localhost:8069'       # Odoo From URL

usernameTo = 'admin'                    # Odoo To user
pwdTo = 'admin'                         # Odoo To password
dbTo = 'odoo'                           # Odoo To base de datos
urlTo = 'http://localhost:8069'         # Odoo To URL

model = 'product.template'              # Modelo de Odoo a migrar

valsFrom = {'fields': ['id', 'name']}

commonFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlFrom))
commonFrom.version()
uidFrom = commonFrom.authenticate(dbFrom, usernameFrom, pwdFrom, {})

commonTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlTo))
commonTo.version()
uidTo = commonTo.authenticate(dbTo, usernameTo, pwdTo, {})

modelsFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlFrom))
modelsTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlTo))
# Ajustar dominio de búsqueda de acuerdo a las necesidades
ids_from = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, model, 'search', [[('image', '!=', False)]])

for id_from in ids_from:
    print(id_from)
    from_id = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, model, 'read', [id_from], valsFrom)
    if from_id:
        print(from_id[0]['name'])
        to_id = modelsTo.execute_kw(dbTo, uidTo, pwdTo, model, 'search', [[('name', '=', from_id[0]['name'])]])
        if to_id:
            image = get_as_base64(urlFrom + '/web/image/product.template/'+ str(id_from) +'/image')
            product_write = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'product.template', 'write', [[to_id[0]], {'image_1920': image}])
