create or replace function
politicians.raw_candidates ( avib_url text, 
                             acand_url text, 
                             acand_name text, 
                             abirth_date date,
                             aparty text,
                             avidvizh text,
                             aregistr text,
                             aizbr text ) 
   returns text
   language plpgsql
   security definer
   returns null on null input
   volatile
   set search_path = politicians, public
   as
$$
BEGIN
   INSERT INTO candidates (
      vib_url, cand_url, cand_name, birth_date, party, vidvizh, registr, izbr
    ) VALUES (
        avib_url, acand_url, acand_name, abirth_date, aparty, avidvizh, aregistr, aizbr
    ) ;
   return 0 ;
END ;
$$ ;