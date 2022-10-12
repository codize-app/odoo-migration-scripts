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

model = 'blog.post'                     # Modelo de Odoo a migrar

valsFrom = {'fields': ['blog_id', 'visits', 'name', 'subtitle', 'author_id', 'create_date', 'post_date', 'content', 'published_date', 'write_date', 'tag_ids', 'website_meta_keywords', 'website_meta_title', 'website_meta_description']}

commonFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlFrom))
commonFrom.version()
uidFrom = commonFrom.authenticate(dbFrom, usernameFrom, pwdFrom, {})

commonTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlTo))
commonTo.version()
uidTo = commonTo.authenticate(dbTo, usernameTo, pwdTo, {})

modelsFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlFrom))
modelsTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlTo))
ids_from = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, model, 'search', [[]], {'order': 'id asc'})   # Ajustar dominio de búsqueda de acuerdo a las necesidades

print(ids_from)

for id_from in ids_from:
    from_id = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, model, 'read', [id_from], valsFrom)
    blog_id_to = False
    author_id_to = False
    if from_id[0]['blog_id']:
        blog_id_from = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'blog.blog', 'read', [from_id[0]['blog_id'][0]], {'fields': ['name']})
        blog_id_to = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'blog.blog', 'search', [[('name', '=', blog_id_from[0]['name'])]])[0]
    if from_id[0]['author_id']:
        author_id_from = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'res.partner', 'read', [from_id[0]['author_id'][0]], {'fields': ['name']})
        author_id_to = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'res.partner', 'search', [[('name', '=', author_id_from[0]['name'])]])[0]

    tags = []

    for tag_id in from_id[0]['tag_ids']:
        tag_id_from = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'blog.tag', 'read', [tag_id], {'fields': ['name']})
        tag_id_to = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'blog.tag', 'search', [[('name', '=', tag_id_from[0]['name'])]])
        tags.append(tag_id_to[0])

    to_id = modelsTo.execute_kw(dbTo, uidTo, pwdTo, model, 'create', [{
        'blog_id': blog_id_to,
        'name': from_id[0]['name'],
        'content': from_id[0]['content'],
        'visits': from_id[0]['visits'],
        'subtitle': from_id[0]['subtitle'],
        'author_id': author_id_to,
        'create_date': from_id[0]['create_date'],
        'post_date': from_id[0]['post_date'],
        'published_date': from_id[0]['published_date'],
        'write_date': from_id[0]['write_date'],
        'is_published': True,
        'tag_ids': tags,
        'website_meta_keywords': from_id[0]['website_meta_keywords'],
        'website_meta_title': from_id[0]['website_meta_title'],
        'website_meta_description': from_id[0]['website_meta_description'],
    }])
