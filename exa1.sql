grant all on schema politicians to dbuser ;
grant all on all sequences in schema politicians to dbuser ;
grant select, insert, update, delete on all tables in schema politicians to dbuser ;

START TRANSACTION ;

create schema if not exists politicians ;

create table  politicians.vibory (
   num bigserial not null,
   vib_url text not null unique,
   vib_date date not null,
   vib_name text not null,
   vib_type int not null,
   constraint vibory_pkey primary key (vib_date, vib_name)
) ;


create table politicians.candidates (
   num bigserial not null,
   vib_url text not null,
   cand_url text not null unique,
   cand_name text not null,
   birth_date date not null,
   party text not null,
   vidvizh text not null,
   registr text,
   izbr text,
   constraint candidates_pkey primary key (cand_name, birth_date),
   constraint candidates_fkey
      foreign key (vib_url)
      references politicians.vibory(vib_url)
) ;


create or replace function
politicians.raw_data ( avib_url text, 
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
   INSERT INTO vibory (vib_url, vib_date, vib_name, vib_type) VALUES (avib_url, avib_date, avib_name, avib_type) ;
   return 0 ;
END ;
$$ ;

-- ROLLBACK TRANSACTION ;
COMMIT TRANSACTION ;