# -*- coding; utf-8 -*-
import psycopg2


class DbAdmin:
    def __init__(self):
        self.connection = psycopg2.connect(database='politicians',
                                           user='dbuser',
                                           password='1',
                                           host='localhost',
                                           port=5432
                                           )
        self.cursor = self.connection.cursor()

    def start_func(self,
                   vib_url,
                   vib_date,
                   vib_name,
                   vib_type,
                   # cand_name,
                   # birth_date,
                   # party,
                   # vidvizh,
                   # registr,
                   # izbr,
                   # party_name
                   ):
        self.cursor.execute('''select politicians.raw_data(%s::text, %s::date, %s::text, %s::int) ;''', (vib_url, vib_date, vib_name, vib_type,))
        self.connection.commit()
        # self.connection.close()

    def set_func(self):
        self.cursor.execute('''
                START TRANSACTION ;
                
                create or replace function
                politicians.raw_data ( avib_id bigint, 
                                       avib_date date, 
                                       avib_name text, 
                                       avib_type text ) 
                   returns text
                   language plpgsql
                   security definer
                   returns null on null input
                   volatile
                   set search_path = politicians, public
                   as
                $$
                BEGIN
                   INSERT INTO vibory (vib_id, vib_date, vib_name, vib_type) VALUES (avib_id, avib_date, avib_name, avib_type) ;
                   return 0 ;
                END ;
                $$ ;
                
                COMMIT TRANSACTION ;
        ''')
        self.connection.commit()

    def close(self):
        self.connection.close()

