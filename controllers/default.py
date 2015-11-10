# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from gluon import utils as gluon_utils
import json
import time

@auth.requires_login()
def index():
    draft_id = gluon_utils.web2py_uuid()
    return dict(message_id=draft_id)

@auth.requires_signature()
def add_msg():
    db.post.update_or_insert((db.post.message_id == request.vars.msg_id),
            message_id=request.vars.msg_id,
            message_content=request.vars.msg,
            is_draft=json.loads(request.vars.is_draft))
    return "ok"

@auth.requires_signature()
def load_messages():
    """Loads all messages for the user."""
    rows = db(db.post.author == auth.user_id).select()
    # d = {}
    # for r in rows:
    #     d[r.message_id] = {'message_content': r.message_content}
    d = {r.message_id: {'message_content': r.message_content} for r in rows}
    time.sleep(3)
    return response.json(dict(msg_dict=d))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


