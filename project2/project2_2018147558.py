from turtle import update
from xmlrpc.client import boolean
import psycopg
from psycopg import sql
import os
from typing import Union

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

# problem 1
def entire_search(CONNECTION: str, table_name: str) -> list:
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(query['p1'] + table_name)
            data = cur.fetchall()
    return data


# problem 2
def search_by_studentID(CONNECTION: str, student_id: str) -> Union[list, None]:
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(query['p2'], (student_id,))
            data = cur.fetchall()
            if data == []: print("Not Exist student with STUDENT ID : " + student_id)
            else : return data
    pass


# problem 3
def search_by_studentname(CONNECTION: str, student_name: str) -> Union[list, None]:
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(query['p3'], (student_name, student_name))
            data = cur.fetchall()
            if data == []: print("Not Exist student with NAME Like: " + student_name)
            else : return data
    pass


# problem 4
def registration_history(CONNECTION: str, student_id: str) -> Union[list, None]:
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(query['p4'], (student_id, ))
            data = cur.fetchall()
            if data == []: print("Not Exist student with STUDENT ID: " + student_id)
            else : return data
    pass



# problem 5
def registration(CONNECTION: str, course_id: int, student_id: str) -> Union[list, None]:
    flag = [True, True]
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(query['searchS'], (student_id, ))
            data = cur.fetchall()
            if data == []: flag[0] = False

            cur.execute(query['searchC'], (course_id, ))
            data = cur.fetchall()
            if data == [] : flag[1] = False

            if(not flag[0]) : print("Not Exist student with STUDENT ID : " + student_id)
            if(not flag[1]) : print("Not Exist course with COURSE ID : " + course_id)
            if(not flag[0] or not flag[1]) : return

            cur.execute(query['searchA'], (student_id, course_id))
            data = cur.fetchall()
            if data != [] : 
                print(data[0][0] + "is already registrated in " + data[0][1])
                return
            cur.execute(query['p5'], (course_id, student_id))
            cur.execute("""select * from myschema.course_registration""")
            data = cur.fetchall()
    return data


# problem 6
def withdrawal_registration(CONNECTION: str, course_id: int, student_id: str) -> Union[list, None]:
    flag = [True, True]

    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(query['searchS'], (student_id, ))
            data = cur.fetchall()
            if data == []: flag[0] = False
    
            cur.execute(query['searchC'], (course_id, ))
            data = cur.fetchall()
            if data == [] : flag[1] = False

            if(not flag[0]) : print("Not Exist student with STUDENT ID : " + student_id)
            if(not flag[1]) : print("Not Exist course with COURSE ID : " + course_id)
            if(not flag[0] or not flag[1]) : return

            cur.execute(query['searchA'], (student_id, course_id))
            data = cur.fetchall()
            if data == [] :
                cur.execute(query['searchS'], (student_id, ))
                sName = cur.fetchone()[0]
                cur.execute(query['searchC'], (course_id, ))
                cName = cur.fetchone()[0]
                print(sName + " is not registrated in " + cName)
                return
            cur.execute(query['p6'], (course_id, student_id))
            cur.execute("""select * from myschema.course_registration""")
            data = cur.fetchall()

    return data

# problem 7
def modify_lectureroom(CONNECTION: str, course_id: int, buildno: str, roomno: str) -> Union[list, None]:
    flag = [True, True]

    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cur:    
            cur.execute(query['searchC'], (course_id, ))
            data = cur.fetchall()
            if data == [] : flag[0] = False

            cur.execute(query['searchB'], (buildno, roomno))
            data = cur.fetchall()
            if data == [] : flag[1] = False

            if(not flag[0]) : print("Not Exist course with COURSE ID : " + course_id)
            if(not flag[1]) : print("Not Exist lecture room with BUILD NO: " + buildno + " / ROOM NO: " + roomno)
            if(not flag[0] or not flag[1]) : return

            cur.execute(query['p7'], (buildno, roomno, course_id))
            cur.execute("""select * from myschema.course""")
            data = cur.fetchall()
    return data

# sql file execute ( Not Edit )
def execute_sql(CONNECTION, path):
    folder_path = '/'.join(path.split('/')[:-1])
    file = path.split('/')[-1]
    if file in os.listdir(folder_path):
        with psycopg.connect(CONNECTION) as conn:
            conn.execute(open(path, 'r', encoding='utf-8').read())
            conn.commit()
        print("{} EXECUTRED!".format(file))
    else:
        print("{} File Not Exist in {}".format(file, folder_path))
