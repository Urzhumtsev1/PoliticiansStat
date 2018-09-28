create or replace function
politicians.raw_data ( avib_url text, 
                       avib_date date, 
                       avib_name text, 
                       avib_type int,
                       avib_region int) 
   returns text
   language plpgsql
   security definer
   returns null on null input
   volatile
   set search_path = politicians, public
   as
$$
BEGIN
   INSERT INTO vibory (vib_url, vib_date, vib_name, vib_type, vib_region) VALUES (avib_url, avib_date, avib_name, avib_type, avib_region) ;
   return 0 ;
END ;
$$ ;