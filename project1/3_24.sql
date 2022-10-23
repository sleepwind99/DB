select BT."NAME", count(BT."COURSE_ID") as "COURSE_NUM"
from
(
	select F."NAME", F."ID", C."COURSE_ID", count(CR."STUDENT_ID")/cast(C."MAX_ENROLLEES" as float) as enroll_per, C."PROF_ID", C."YEAR"
	from faculty as F, course as C, course_registration as CR
	where C."COURSE_ID" = CR."COURSE_ID" and F."ID" = C."PROF_ID" and C."YEAR" between 2013 and 2018
	group by F."NAME", C."COURSE_ID", C."PROF_ID", C."YEAR", F."ID"
	having count(CR."STUDENT_ID")/cast(C."MAX_ENROLLEES" as float) > 0.8
) as BT
group by BT."ID", BT."NAME"
order by "COURSE_NUM" desc, BT."NAME" asc

