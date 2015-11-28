# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from gluon import utils as gluon_utils
import json
import time
import random

def index():
    deck = []
    suit = ["diamond", "club", "heart", "spade"]
    value = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
    for x in value:
        for y in suit:          #populates the deck
            deck.append([x, y])
    print len(deck)

    temp = []
    for i in range(len(deck)):  #shuffles the deck
        el = random.choice(deck)
        deck.remove(el)
        temp.append(el)
    deck = temp

    numpeople = 0
    for i in db(db.auth_user.id).select():
        numpeople += 1
    print numpeople

    players = []
    player0 = []
    player1 = []
    player2 = []
    player3 = []

    if numpeople == 3:
        players = [player0, player1, player2]
    elif numpeople == 4:
        players = [player0, player1, player2, player3]

    player_index = 0
    for i in deck:              #deals the deck
        if player_index == len(players):
            player_index = 0
        players[player_index].append(i)
        player_index += 1


    print "player0 = ", player0
    print "player1 = ", player1
    print "player2 = ", player2
    if numpeople == 4:
        print "player3 = ", player3


    return dict(deck=deck)


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


