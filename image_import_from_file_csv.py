#!/usr/bin/python
# encoding: utf-8

# Load image PNG / JPG to Odoo existing product searching by SKU (default_code) using CSV file

import xmlrpclib
import base64
import csv

usernameFrom = 'admin'                  # Odoo From user
pwdFrom = 'admin'                       # Odoo From password
dbFrom = 'odoo'                         # Odoo From base de datos
urlFrom = 'http://localhost:8069'       # Odoo From URL

file_csv_route = ''
images_route = ''

commonFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlFrom))
commonFrom.version()
uidFrom = commonFrom.authenticate(dbFrom, usernameFrom, pwdFrom, {})

modelsFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlFrom))

with open(file_csv_route + '.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(row)
        if row[1] != '':
            p_id = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'product.template', 'search', [[['default_code', '=', str(row[0])]]])
            if p_id:
                with open(images_route + str(row[1]) + ".png", "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    print(encoded_string)
                    modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'product.template', 'write', [p_id[0], {'image_1920': encoded_string}])
