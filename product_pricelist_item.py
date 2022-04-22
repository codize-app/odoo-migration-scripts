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

model = 'product.pricelist.item'        # Modelo de Odoo a migrar

valsFrom = {'fields': ['applied_on', 'product_tmpl_id', 'price', 'fixed_price']}

commonFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlFrom))
commonFrom.version()
uidFrom = commonFrom.authenticate(dbFrom, usernameFrom, pwdFrom, {})

commonTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlTo))
commonTo.version()
uidTo = commonTo.authenticate(dbTo, usernameTo, pwdTo, {})

modelsFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlFrom))
modelsTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlTo))
# Ajustar dominio de búsqueda de acuerdo a las necesidades, en este caso el ID 4 será el ID de la lista de precios a importar
ids_from = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, model, 'search', [[('pricelist_id', '=', 4)]])

for id_from in ids_from:
    from_id = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, model, 'read', [id_from], valsFrom)
    if from_id[0]['applied_on'] == '1_product':
        prev_product = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'product.template', 'read', [from_id[0]['product_tmpl_id'][0]], {'fields': ['name']})
        if prev_product:
            product = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'product.template', 'search', [[('name', '=', prev_product[0]['name'])]])
            if product:
                print(product)
                pricelist_item = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'product.pricelist.item', 'create', [{
                    'applied_on': '1_product',
                    'product_tmpl_id': product[0],
                    'fixed_price': from_id[0]['fixed_price'],
                    'pricelist_id': 2 # Este ID 2 es el ID de la lista de precios de recepción
                }])
