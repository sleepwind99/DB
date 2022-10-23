select course."YEAR", college."MAJOR_NAME", count(course."COURSE_ID") as "COUNT_OF_COURSE"
from course, college
where course."COURSE_ID_PREFIX" != 'XYZ' and course."COURSE_ID_PREFIX" = college."MAJOR_ID"
group by course."YEAR", college."MAJOR_NAME"
order by course."YEAR" asc, count(course."COURSE_ID") desc