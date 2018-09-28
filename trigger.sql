create trigger tr_type_and_region
   after insert
   on politicians.vibory 
   for each row
   execute procedure politicians.func_type_and_region() ;