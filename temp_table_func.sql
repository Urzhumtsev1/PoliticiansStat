create or replace function 
politicians.func_type_and_region_temp(avib_type int, avib_region int ) 
   returns int
   security definer
   returns null on null input
   volatile
   language plpgsql
   as
$$
BEGIN
   create table if not exists politicians.temp01 (
      query_num bigserial not null,
      vib_type int not null,
      vib_region int not null
    )  ;
   
   INSERT INTO politicians.temp01 (vib_type, vib_region) VALUES (avib_type, avib_region) ;

   return 0 ;
END ;
$$ ;
