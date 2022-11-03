select c."YEAR", c."SEMESTER", c."COURSE_ID_PREFIX", c."COURSE_ID_NO", c."DIVISION_NO", c."COURSE_NAME", f."NAME", g."GRADE"
from myschema.students s 
  join myschema.grade g on s."STUDENT_ID" = g."STUDENT_ID"
  join myschema.course c on c."COURSE_ID" = g."COURSE_ID"
  join myschema.faculty f on f."ID" = c."PROF_ID"
where s."STUDENT_ID" = '2017111111' and not (c."YEAR" = 2022 and c."SEMESTER" = 2)