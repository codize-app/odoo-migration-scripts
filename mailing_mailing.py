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

valsFrom = {'fields': ['subject', 'preview', 'body_html', 'state', 'sent_date']}

commonFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlFrom))
commonFrom.version()
uidFrom = commonFrom.authenticate(dbFrom, usernameFrom, pwdFrom, {})

commonTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(urlTo))
commonTo.version()
uidTo = commonTo.authenticate(dbTo, usernameTo, pwdTo, {})

modelsFrom = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlFrom))
modelsTo = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(urlTo))
mailing_ids_from = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'mailing.mailing', 'search', [[('state', '=', 'done')]], {'order': 'id asc'})   # Ajustar dominio de búsqueda de acuerdo a las necesidades

print(mailing_ids_from)

for mail in mailing_ids_from:
    print(mail)
    from_id = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'mailing.mailing', 'read', [mail], valsFrom)
    to_mail = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'mailing.mailing', 'create', [{
        'subject': from_id[0]['subject'],
        'preview': from_id[0]['preview'],
        'sent_date': from_id[0]['sent_date'],
        'body_html': from_id[0]['body_html'],
        'body_arch': from_id[0]['body_html'],
        'state': from_id[0]['state'],
    }])
    mailings =  modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'mailing.trace', 'search', [[('mass_mailing_id', '=', mail)]])
    for mass_mail in mailings:
        prev_mail = modelsFrom.execute_kw(dbFrom, uidFrom, pwdFrom, 'mailing.trace', 'read', [mass_mail], {'fields': ['email', 'sent', 'opened', 'clicked', 'message_id', 'res_id', 'state']})
        new_mail = modelsTo.execute_kw(dbTo, uidTo, pwdTo, 'mailing.trace', 'create', [{
            'email': prev_mail[0]['email'],
            'sent_datetime': prev_mail[0]['sent'],
            'open_datetime': prev_mail[0]['opened'],
            'links_click_datetime': prev_mail[0]['clicked'],
            'mass_mailing_id': to_mail,
            'message_id': prev_mail[0]['message_id'],
            'model': 'mailing.contact',
            'trace_type': 'mail',
            'res_id': prev_mail[0]['res_id'],
            'trace_status': prev_mail[0]['state'].replace('opened', 'open').replace('ignored', 'sent') # En odoo 16 state se llama trace_status y tiene valores distintos, ajustar a cada necesidad
        }])
