START TRANSACTION ;
create or replace function 
politicians.func_type_and_region() returns trigger
   security definer
   called on null input
   volatile
   language plpgsql
   as

$$
BEGIN
   with 
   vt as (
      select 
            vib_type as type,
            vib_region as region
         from politicians.temp01
         order by query_num desc
         limit 1
   )

   update politicians.vibory
      set vib_type    = vt.type,
          vib_region  = vt.region
      from vt
      where politicians.vibory.vib_type = 0 ;
      
   -- delete from politicians.temp01 ;
   return null ;
END ;
$$ ;
COMMIT TRANSACTION ;