START TRANSACTION ;
create or replace function 
politicians.func_type_and_region() returns trigger
   security definer
   called on null input
   volatile
   language plpgsql
   set search_path = politicians, public
   as

$$
BEGIN
   with 
   one as (
      select 
            tmp.vib_type   as type,
            tmp.vib_region as region
         from temp01 as tmp
   ),

   two as (
      select
            vib_type,
            vib_region
         from politicians.vibory 
   )

   update politicians.vibory
      set vib_type    = one.type,
          vib_region  = one.region
      where two.vib_type = 0 ;
      
   return null ;
END ;
$$ ;
COMMIT TRANSACTION ;