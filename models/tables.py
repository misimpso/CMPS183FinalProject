#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

from json import loads, dumps
db.define_table('player',
                Field('player_id'),
                Field('waiting', 'boolean'),
                Field('ingame', 'boolean'),
                )

db.define_table('deck',
                Field('players'),
                Field('deck_id'),
                Field('players_cards')
                )
db.define_table('hands',
                Field('deck_id'),
                Field('last_played_hand'),
                Field('players_hands')
                )
db.deck.players_cards.filter_in = lambda obj, dumps=dumps: dumps(obj)
db.deck.players_cards.filter_out = lambda txt, loads=loads: loads(txt)
db.hands.players_hands.filter_in = lambda obj, dumps=dumps: dumps(obj)
db.hands.players_hands.filter_out = lambda txt, loads=loads: loads(txt)
