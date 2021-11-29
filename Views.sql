-- Views would be created manually using the below script for future change/update based on business requirements.
--1 How did the name Ida change period-over-period nationally?
CREATE OR REPLACE VIEW "Ida_Changed_Period" AS
	select "Name", "Year",
        	max(case when ("Gender"='F') then "Count" else 0 end) as "F_Count",
        	max(case when ("Gender"='M') then "Count" else 0 end) as "M_Count"
        	from "NationalNames" 
			where "Name" like 'Ida'
        	group by "Name", "Year"
        	order by "Year" asc;
		 
--2 How did the name Ida change period-over-period in California?
CREATE OR REPLACE VIEW "Ida_Changed_Period_California" AS
	select "Name", "Year",
         	max(case when ("Gender"='F') then "Count" else 0 end) as "F_Count",
         	max(case when ("Gender"='M') then "Count" else 0 end) as "M_Count"
         	from "StateNames" 
		 	where "Name" like 'Ida' and "State" like 'CA'
         	group by "Name", "Year"
         	order by "Year" asc;

--3 What name is most unisex?
CREATE OR REPLACE VIEW "Unisex_Name" AS
	select
    	"Name",
    	sum("Count") filter(where "Gender" = 'M' ) "M_Count",
		sum("Count") filter(where "Gender" = 'F' ) "F_Count",
		coalesce(sum("Count") filter(where "Gender" = 'M' ), 0) +
 			coalesce(sum("Count") filter(where "Gender" = 'F' ),0) as "Total_Births",
		sum("Count") filter(where "Gender" = 'M' ) /
			cast(sum("Count") filter(where "Gender" = 'M' ) +
			 	sum("Count") filter(where "Gender" = 'F' ) as float) as "M_Prop",
		sum("Count") filter(where "Gender" = 'F' ) /
			cast(sum("Count") filter(where "Gender" = 'M' ) +
			 	sum("Count") filter(where "Gender" = 'F' ) as float) as "F_Prop",
		abs(sum("Count") filter(where "Gender" = 'F' ) /
	 		cast(sum("Count") filter(where "Gender" = 'M' ) +
			 	sum("Count") filter(where "Gender" = 'F' ) as float) - 0.5) as "Measure"
from "NationalNames"
    group by "Name"
    having 	abs(sum("Count") filter(where "Gender" = 'F' ) /
	 		    cast(sum("Count") filter(where "Gender" = 'M' ) +
			 	    sum("Count") filter(where "Gender" = 'F' ) as float) - 0.5) > 0
    order by "Measure" asc;


--4 What names on the national level are too scarce on the state level?
CREATE OR REPLACE VIEW "National_Scarce_On_State" AS
	select "Name", SUM("Count") as "SUM" from "StateNames"
	where "Name" in (Select Distinct "Name" from "NationalNames")
	group by "StateNames"."Name"
	order by "SUM" asc;