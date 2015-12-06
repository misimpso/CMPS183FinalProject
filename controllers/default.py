# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from gluon import utils as gluon_utils
import json
import time
import random

def index():
    playerQueue = db(db.player).select()
    print playerQueue
    draft_id = gluon_utils.web2py_uuid()
    return dict(playerQueue=playerQueue, draft_id=draft_id)

@auth.requires_signature()
def enterQueue():
    db.player.update_or_insert((db.player.player_id == request.vars.player_id),
                                player_id=request.vars.player_id,
                                waiting=request.vars.waiting,
                                ingame=request.vars.ingame
                                )
    return "ok"

@auth.requires_signature()
def loadQueue():
    rows = db(db.player).select()
    d = [dict(player_id=r.player_id, waiting=r.waiting, ingame=r.ingame)
         for r in rows]
    #print d
    return response.json(dict(playerQueue=d))

@auth.requires_signature()
def enterGame():
    player_ids = json.loads(request.vars.player_id)
    #print "player_ids = ", player_ids
    for player in player_ids:
        #print player
        db.player.update_or_insert((db.player.player_id == player),
                                   waiting=False,
                                   ingame=True
                                   )
    #print player_ids
    deck_id = request.vars.deck_id
    print deck_id
    players_cards = deck_maker(3)
    db.deck.update_or_insert((db.deck.players == player_ids),
                             players=player_ids,
                             deck_id=deck_id,
                             deck_cards=players_cards
                             )

    return "ok"

def deck_maker(numpeople):
    deck = []
    suit = ["diamond", "club", "heart", "spade"]
    value = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
    for x in value:
        for y in suit:          #populates the deck
            deck.append([x, y])
    temp = []
    for i in range(len(deck)):  #shuffles the deck
        el = random.choice(deck)
        deck.remove(el)
        temp.append(el)
    deck = temp

    print numpeople

    players = []
    player0 = []
    player1 = []
    player2 = []
    player3 = []

    if numpeople == 3:
        players = [player0, player1, player2]
    elif numpeople >= 4:
        players = [player0, player1, player2, player3]

    player_index = 0
    for i in deck:              #deals the deck
        if player_index == len(players):
            player_index = 0
        players[player_index].append(i)
        player_index += 1


    print players

    return dict(players=players)

def play():
    deck_id = request.args(0)
    print deck_id
    deck = db(db.deck.deck_id == deck_id).select()
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

def reset():
    db(db.player.id > 0).delete()
    db(db.deck).delete()
    session.flash = T("Database has been reset")
    redirect(URL('default', 'index'))
    return
