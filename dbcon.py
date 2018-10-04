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

    def vibory_insert(self,
                      vib_url,
                      vib_date,
                      vib_name,
                      vib_type,
                      vib_region
                      ):
        self.cursor.execute('''
            select politicians.raw_data(%s::text, 
                                        %s::date, 
                                        %s::text, 
                                        %s::int, 
                                        %s::int
                                        ) ;''', (vib_url,
                                                 vib_date,
                                                 vib_name,
                                                 vib_type,
                                                 vib_region
                                                 )
                            )
        self.connection.commit()

    def candidates_insert(self,
                          vib_url,
                          cand_url,
                          cand_name,
                          birth_date,
                          party,
                          vidvizh,
                          registr,
                          izbr
                          ):
        self.cursor.execute('''
            select politicians.raw_candidates(%s::text, 
                                              %s::text, 
                                              %s::text, 
                                              %s::date, 
                                              %s::text, 
                                              %s::text, 
                                              %s::text, 
                                              %s::text
                                              ) ;''',  (vib_url,
                                                        cand_url,
                                                        cand_name,
                                                        birth_date,
                                                        party,
                                                        vidvizh,
                                                        registr,
                                                        izbr
                                                        )
                            )
        self.connection.commit()

    def temp_table(self, vib_type, vib_region):
        self.cursor.execute('''
            select politicians.func_type_and_region_temp(%s::int, 
                                                         %s::int
                                                         ) ;''', (vib_type,
                                                                  vib_region
                                                                  )
                            )
        self.connection.commit()

    def close(self):
        self.connection.close()

