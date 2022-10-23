select T."COURSE_NAME" 
From(
    SELECT SOL."COURSE_NAME", sum(SOL."count")
    FROM(
        SELECT RE."COURSE_NAME", RE."STUDENT_ID", COUNT(RE."COURSE_NAME")
        FROM(
            SELECT CR."STUDENT_ID", CR."COURSE_ID" , concat(C."COURSE_ID_PREFIX", C."COURSE_ID_NO"), C."COURSE_NAME"
            FROM course_registration as CR, course as C
            where CR."COURSE_ID" = C."COURSE_ID"
            ORDER BY CR."STUDENT_ID" ASC
            )as RE
        GROUP BY RE."COURSE_NAME", RE."STUDENT_ID"
        HAVING COUNT(RE."COURSE_NAME") > 1
        )as SOL
    GROUP BY SOL."COURSE_NAME"
    ORDER BY sum(SOL."count") DESC
    )as T
LIMIT 3