select T.total_grade, s."STUDENT_ID",  s."GRADE", cg."MAJOR_NAME", cg."COLLEGE_NAME"
from
(
	select s."STUDENT_ID", s."NAME", sum(c."CREDIT" * g."GRADE") / sum(c."CREDIT") as total_grade, s."MAJOR_ID", s."GRADE"
	from course as c, students as s, grade as g
	where c."YEAR" = 2018 and c."SEMESTER" = 2 and c."COURSE_ID" = g."COURSE_ID" and g."STUDENT_ID" = s."STUDENT_ID"
	group by s."STUDENT_ID", s."NAME", s."MAJOR_ID", s."GRADE"
) as T, students as s, college as cg
where T."STUDENT_ID" = s."STUDENT_ID" 
	and s."MAJOR_ID" = cg."MAJOR_ID" 
	and s."GRADE" between 1 and 4
	and T.total_grade in
	(
		select max(total_grade)
		from 
		(
			select s."STUDENT_ID", s."NAME", sum(c."CREDIT" * g."GRADE") / sum(c."CREDIT") as total_grade, s."MAJOR_ID", s."GRADE"
			from course as c, students as s, grade as g
			where c."YEAR" = 2018 and c."SEMESTER" = 2 and c."COURSE_ID" = g."COURSE_ID" and g."STUDENT_ID" = s."STUDENT_ID"
			group by s."STUDENT_ID", s."NAME", s."MAJOR_ID", s."GRADE"
		) as t, students as s
		where T."STUDENT_ID" = s."STUDENT_ID"
		group by s."MAJOR_ID", s."GRADE"
	)
order by cg."MAJOR_NAME", s."GRADE", x."STUDENT_ID"