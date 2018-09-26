START TRANSACTION ;

create schema if not exists politicians ;

create table politicians.vibory (
   num bigserial not null,
   vib_id bigint not null unique,
   vib_date date not null,
   vib_name text not null,
   vib_type text not null,
   constraint vibory_pkey primary key (vib_date, vib_name)
) ;


create table politicians.candidates (
   num bigserial not null,
   vib_id bigint not null,
   cand_id bigint not null unique,
   cand_name text not null,
   birth_date date not null,
   party text not null,
   vidvizh text not null,
   registr text,
   izbr text,
   constraint candidates_pkey primary key (cand_name, birth_date),
   constraint candidates_fkey
      foreign key (vib_id)
      references politicians.vibory(vib_id)
) ;

create table politicians.party (
   num bigserial not null primary key,
   vib_id bigint not null references politicians.vibory(vib_id),
   cand_id bigint not null references politicians.candidates(cand_id),
   party_name text not null 
   /*constraint party_fkey
      foreign key (vib_id, cand_id)
      references politicians.vibory(vib_id), references politicians.candidates(cand_id)*/
) ;


COMMIT TRANSACTION ;