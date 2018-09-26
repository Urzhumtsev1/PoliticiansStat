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
                   avib_id,
                   avib_date,
                   avib_name,
                   avib_type,
                   # cand_name,
                   # birth_date,
                   # party,
                   # vidvizh,
                   # registr,
                   # izbr,
                   # party_name
                   ):
        self.cursor.execute('''select politicians.raw_data(%s::bigint, %s::date, %s::text, %s::text) ;''', (avib_id, avib_date, avib_name, avib_type,))
        self.connection.commit()
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
        #self.connection.close()

    def delete_single(self, table, column, parameter):
        self.cursor.execute('''DELETE FROM {0} WHERE {1} = {2}'''.format(table, column, parameter))
        return self.connection.commit()

    def delete(self, table, parameter):
        self.cursor.execute('''DELETE FROM {0} WHERE {1}'''.format(table, parameter))
        return self.connection.commit()

    def insert(self, tablecolumns, values):
        self.cursor.execute("""INSERT INTO {0} VALUES {1};""".format(tablecolumns, values))
        return self.connection.commit()

    def update(self, table, values, condition):
        self.cursor.execute("""UPDATE {0} SET {1} WHERE {2}""".format(table, values, condition))
        return self.connection.commit()

    def close(self):
        self.connection.close()

