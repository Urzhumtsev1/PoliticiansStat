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
   create temporary table temp01 (
      vib_type int,
      vib_region int
    )  ;
   
   INSERT INTO temp01 (vib_type, vib_region) VALUES (avib_type, avib_region) ;

   return 0 ;
END ;
$$ ;
