grant all on schema politicians to dbuser ;
grant all on all sequences in schema politicians to dbuser ;
grant select, insert, update, delete on all tables in schema politicians to dbuser ;

START TRANSACTION ;

create schema if not exists politicians ;

/*create table politicians.vibory (
   num bigserial not null,
   vib_url text not null unique,
   vib_date date not null,
   vib_name text not null,
   vib_type int not null,
   vib_region int not null,
   constraint vibory_pkey primary key (vib_date, vib_name)
) ;*/


create table politicians.candidates (
   num bigserial not null primary key,
   vib_url text references politicians.vibory (vib_url),
   cand_url text not null,
   cand_name text,
   birth_date date not null,
   party text not null,
   vidvizh text not null,
   registr text,
   izbr text
) ;

-- ROLLBACK TRANSACTION ;
COMMIT TRANSACTION ;