select substr(R."NAME", 1 , 1) || LPAD('*', length(R."NAME")-1, '*') as "NAME", R."STUDENT_ID", college."MAJOR_NAME", college."COLLEGE_NAME"
from
(
	select T."STUDENT_ID", T."NAME", sum(T."CREDIT" * G."GRADE") / sum(T."CREDIT") as total_grade, sum(case G."GRADE" when 0 then 0 else T."CREDIT" end) as CS
  from 
    (
      select S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX", C."YEAR", C."SEMESTER", C."CREDIT", max(C."COURSE_ID") as "COURSE_ID"
      from students as S, course as C
      where (S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX",  concat(C."YEAR", C."SEMESTER")) in
        (
          select S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX", max(concat(c."YEAR", c."SEMESTER")) as "YS"
          from students as S, course as C, grade as G
          where S."GRADE" = 4 and C."COURSE_ID" = G."COURSE_ID" and G."STUDENT_ID" = S."STUDENT_ID" and C."YEAR" between 2015 and 2018
          group by S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX"
        )
      group by S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX", C."YEAR", C."SEMESTER", C."CREDIT"
    ) as T, grade as G
  where G."STUDENT_ID" = T."STUDENT_ID"
    and G."COURSE_ID" = T."COURSE_ID"
  group by T."STUDENT_ID", T."NAME"
) as R, college, students
where students."MAJOR_ID" = college."MAJOR_ID"
	and students."STUDENT_ID" = R."STUDENT_ID"
	and (
	(R.total_grade = (
			select max(maxg.total_grade)
			from 
			(
        select T.total_grade
        from
        (
          select T."STUDENT_ID", T."NAME", sum(T."CREDIT" * G."GRADE") / sum(T."CREDIT") as total_grade, sum(case G."GRADE" when 0 then 0 else T."CREDIT" end) as CS
          from 
            (
              select S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX", C."YEAR", C."SEMESTER", C."CREDIT", max(C."COURSE_ID") as "COURSE_ID"
              from students as S, course as C
              where (S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX",  concat(C."YEAR", C."SEMESTER")) in
                (
                  select S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX", max(concat(c."YEAR", c."SEMESTER")) as "YS"
                  from students as S, course as C, grade as G
                  where S."GRADE" = 4 and C."COURSE_ID" = G."COURSE_ID" and G."STUDENT_ID" = S."STUDENT_ID" and C."YEAR" between 2015 and 2018
                  group by S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX"
                )
              group by S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX", C."YEAR", C."SEMESTER", C."CREDIT"
            ) as T, grade as G
          where G."STUDENT_ID" = T."STUDENT_ID"
            and G."COURSE_ID" = T."COURSE_ID"
          group by T."STUDENT_ID", T."NAME"
        ) as T
        where T.CS >= 40
      ) as maxg
		)
	) or 
	(R.total_grade = (
			select min(ming.total_grade)
			from 
			(
        select T.total_grade
        from
        (
          select T."STUDENT_ID", T."NAME", sum(T."CREDIT" * G."GRADE") / sum(T."CREDIT") as total_grade, sum(case G."GRADE" when 0 then 0 else T."CREDIT" end) as CS
          from 
            (
              select S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX", C."YEAR", C."SEMESTER", C."CREDIT", max(C."COURSE_ID") as "COURSE_ID"
              from students as S, course as C
              where (S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX",  concat(C."YEAR", C."SEMESTER")) in
                (
                  select S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX", max(concat(c."YEAR", c."SEMESTER")) as "YS"
                  from students as S, course as C, grade as G
                  where S."GRADE" = 4 and C."COURSE_ID" = G."COURSE_ID" and G."STUDENT_ID" = S."STUDENT_ID" and C."YEAR" between 2015 and 2018
                  group by S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX"
                )
              group by S."STUDENT_ID", S."NAME", C."COURSE_ID_NO", C."COURSE_ID_PREFIX", C."YEAR", C."SEMESTER", C."CREDIT"
            ) as T, grade as G
          where G."STUDENT_ID" = T."STUDENT_ID"
            and G."COURSE_ID" = T."COURSE_ID"
          group by T."STUDENT_ID", T."NAME"
        ) as T
        where T.CS >= 40
      ) as ming
		)
	)
)
order by R.total_grade desc