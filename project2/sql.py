query = {
  'p1': "select * from myschema.",
  'p2': """
    select s."NAME", s."STUDENT_ID", s."ADMISSION_YEAR", c."MAJOR_NAME", c."COLLEGE_NAME", case when s."GRADE" = 0 then true else false end as "GRADUATE"
    from myschema.students s join myschema.college c on s."MAJOR_ID" = c."MAJOR_ID"
    where s."STUDENT_ID" = %s
  """,
  'p3' : """
    select s."NAME", s."STUDENT_ID", s."ADMISSION_YEAR", c."MAJOR_NAME", c."COLLEGE_NAME", case when s."GRADE" = 0 then true else false end as "GRADUATE"
    from myschema.students s join myschema.college c on s."MAJOR_ID" = c."MAJOR_ID"
    where s."NAME" like %s or s."NAME" = %s
  """,
  'p4' : """
    select c."YEAR", c."SEMESTER", c."COURSE_ID_PREFIX", c."COURSE_ID_NO", c."DIVISION_NO", c."COURSE_NAME", f."NAME", g."GRADE"
    from myschema.students s 
      join myschema.grade g on s."STUDENT_ID" = g."STUDENT_ID"
      join myschema.course c on c."COURSE_ID" = g."COURSE_ID"
      join myschema.faculty f on f."ID" = c."PROF_ID"
    where s."STUDENT_ID" = %s
  """,
  'p5' : """insert into myschema.course_registration("COURSE_ID", "STUDENT_ID") VALUES (%s, %s)""",
  'p6' : """delete from myschema.course_registration where "COURSE_ID" = %s and "STUDENT_ID" = %s""",
  'p7' : """update myschema.course set "BUILDNO" = %s, "ROOMNO" = %s where "COURSE_ID" = %s""",
  'searchB' : """select * from myschema.lectureroom l where l."BUILDNO" = %s and "ROOMNO" = %s""",
  'searchS' : """select s."NAME" from myschema.students s where s."STUDENT_ID" = %s""",
  'searchC' : """select c."COURSE_NAME" from myschema.course c where c."COURSE_ID" = %s""",
  'searchA' : """
    select s."NAME", c."COURSE_NAME"
    from myschema.students s 
      join myschema.course_registration cr on s."STUDENT_ID" = cr."STUDENT_ID"
      join myschema.course c on cr."COURSE_ID" = c."COURSE_ID"
    where s."STUDENT_ID" = %s and c."COURSE_ID" = %s
  """
}