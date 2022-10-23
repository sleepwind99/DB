SELECT FIN."DAY_OF_WEEK", concat(to_char(TT."START_TIME", 'HH24:MI'), ' ~ ' , to_char(TT."END_TIME", 'HH24:MI'))
FROM(
    SELECT day_of_week."DAY_OF_WEEK", timetable."NO"
    FROM day_of_week, timetable
    WHERE day_of_week."DAY_OF_WEEK" != 'SAT' and day_of_week."DAY_OF_WEEK" != 'SUN'
    EXCEPT
    SELECT STU."DAY_OF_WEEK", STU."NO"
    FROM(
        SELECT X."DAY_OF_WEEK", X."NO"
        FROM(
            SELECT ONE."DAY_OF_WEEK", ONE."NO"
            FROM(
                SELECT B."DAY_OF_WEEK", B."NO", CR."STUDENT_ID", CR."COURSE_ID"
                FROM(
                    SELECT CT."DAY_OF_WEEK", CT."NO", course."YEAR", course."SEMESTER", course."COURSE_ID"
                    FROM course, course_to_time as CT 
                    WHERE course."YEAR" = 2018 and course."SEMESTER" = 2 and course."COURSE_ID" = CT."COURSE_ID"
                    )as B, course_registration as CR
                WHERE B."COURSE_ID" = CR."COURSE_ID" and CR."STUDENT_ID" = '2018111111'
                )as ONE
            UNION   
            SELECT TWO."DAY_OF_WEEK", TWO."NO"
            FROM
                (
                SELECT B."DAY_OF_WEEK", B."NO", CR."STUDENT_ID", CR."COURSE_ID"
                FROM(
                    SELECT CT."DAY_OF_WEEK", CT."NO", course."YEAR", course."SEMESTER", course."COURSE_ID"
                    FROM course, course_to_time as CT 
                    WHERE course."YEAR" = 2018 and course."SEMESTER" = 2 and course."COURSE_ID" = CT."COURSE_ID"
                    )as B, course_registration as CR
                WHERE B."COURSE_ID" = CR."COURSE_ID" and CR."STUDENT_ID" = '2017222222'
                )as TWO
            )as X
        ORDER BY X."DAY_OF_WEEK" ASC, X."NO" ASC
        )as STU
    )as FIN, timetable as TT
WHERE FIN."NO" = TT."NO"