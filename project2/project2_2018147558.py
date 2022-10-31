from turtle import update
from xmlrpc.client import boolean
import psycopg
from psycopg import sql
import os
from typing import Union
from sql import query


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
