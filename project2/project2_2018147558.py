import psycopg
from psycopg import sql
import os
from typing import Union


# problem 1
def entire_search(CONNECTION: str, table_name: str) -> list:
    query = """select * from myschema.""" + table_name
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
    return data


# problem 2
def search_by_studentID(CONNECTION: str, student_id: str) -> Union[list, None]:
    query = """
        select s."NAME", s."STUDENT_ID", s."ADMISSION_YEAR", c."MAJOR_NAME", c."COLLEGE_NAME", case when s."GRADE" = 0 then true else false end as "GRADUATE"
        from myschema.students s join myschema.college c on s."MAJOR_ID" = c."MAJOR_ID"
        where s."STUDENT_ID" = %s"""
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (student_id,))
            data = cur.fetchall()
    return data


# problem 3
def search_by_studentname(CONNECTION: str, student_name: str) -> Union[list, None]:
    query = """
        select s."NAME", s."STUDENT_ID", s."ADMISSION_YEAR", c."MAJOR_NAME", c."COLLEGE_NAME", case when s."GRADE" = 0 then true else false end as "GRADUATE"
        from myschema.students s join myschema.college c on s."MAJOR_ID" = c."MAJOR_ID"
        where s."NAME" like %s or s."NAME" = %s"""
    with psycopg.connect(CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (student_name, student_name))
            data = cur.fetchall()
    return data
    pass


# problem 4
def registration_history(CONNECTION: str, student_id: str) -> Union[list, None]:

    pass



# problem 5
def registration(CONNECTION: str, course_id: int, student_id: str) -> Union[list, None]:

    pass


# problem 6
def withdrawal_registration(CONNECTION: str, course_id: int, student_id: str) -> Union[list, None]:

    pass


# problem 7
def modify_lectureroom(CONNECTION: str, course_id: int, buildno: str, roomno: str) -> Union[list, None]:
    
    pass

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
