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

model = 'sale.order'                              # Modelo de Odoo a migrar

valsFrom = {'fields': ['name', 'partner_id', 'order_line', 'date_order', 'state']}

commonFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlFrom))
commonFrom.version()
uidFrom = commonFrom.authenticate(dbFrom, usernameFrom, pwdFrom, {})

commonTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlTo))
commonTo.version()
uidTo = commonTo.authenticate(dbTo, usernameTo, pwdTo, {})

modelsFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlFrom))
modelsTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlTo))
ids_from = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, model, 'search', [[]], {'order': 'id asc'})   # Ajustar dominio de búsqueda de acuerdo a las necesidades

for id_from in ids_from:
    print(id_from)
    from_id = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, model, 'read', [id_from], valsFrom)
    partner_to_id = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'res.partner', 'search', [[('name', '=', from_id[0]['partner_id'][1])]])
    if partner_to_id:
        sale_order = modelsTo.execute_kw(dbTo, uidTo, pwdTo, model, 'create', [{
            'name': from_id[0]['name'],
            'partner_id': partner_to_id[0],
            'date_order': from_id[0]['date_order'],
            'state': from_id[0]['state']
        }])
        if from_id[0]['order_line']:
            for line_id in from_id[0]['order_line']:
                line = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'sale.order.line', 'read', [line_id], {'fields': ['product_id', 'name', 'product_uom_qty', 'price_unit', 'discount']})
                if line[0]['product_id']:
                    product_from = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'product.product', 'read', [line[0]['product_id'][0]], {'fields': ['name']})
                    product_to = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'product.product', 'search', [[('name', '=', product_from[0]['name'])]])
                    if product_to:
                        sale_order_line = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'sale.order.line', 'create', [{
                            'product_id': product_to[0],
                            'name': line[0]['name'],
                            'order_id': sale_order,
                            'price_unit': line[0]['price_unit'],
                            'product_uom_qty': line[0]['product_uom_qty'],
                            'discount': line[0]['discount']
                        }])
