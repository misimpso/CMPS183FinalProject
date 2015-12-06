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

db.define_table('player',
                Field('player_id'),
                Field('waiting', 'boolean'),
                Field('ingame', 'boolean'),
                )

db.define_table('deck',
                Field('players'),
                Field('deck_id'),
                Field('deck_cards')
                )

db.define_table('player_hand',
                Field('player_id', default=auth.user_id),
                Field('player_cards'),
                Field('parent_deck', 'reference deck'),
                Field('winner', default=False)
                )