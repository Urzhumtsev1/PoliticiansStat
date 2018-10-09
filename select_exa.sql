START TRANSACTION ;
with 
vibs as (
select * 
	from politicians.vibory 
	where vib_date > '2011-09-18' 
		and vib_region = 77
		and vib_type = 4
),

cands as (
	select 
		vb.vib_name,
		pc.cand_name,
		pc.birth_date,
		pc.party,
		pc.izbr, 
		vb.vib_region,
		vb.vib_type
	from politicians.candidates as pc
	inner join vibs as vb
		on pc.vib_url = vb.vib_url 
)

select * 
	from cands
	where izbr = 'избр.'
 ;

ROLLBACK TRANSACTION ;