import psycopg2 as pg
from pars import mask_pars
q='"'

def connect(host:str,port:int,db_name:str,user:str,password:str):
    """
    Create connection to database
    If error occured return string of "Exception"
    WARNING database conection needs to be closed before stop of program
    """
    try:
        base=pg.connect(host=host,user=user,password=password,database=db_name,port=port)
        base.autocommit=True
        print("[INFO] Connected to database")
        return base
    except Exception as _ex:
        print("[INFO] Exception raised:",_ex)
        return "Exception"
def cursor(db,command:str):
    """
    Execute given SQL command
    """
    if db!="Exception":
        with db.cursor() as cursor:
            cursor.execute(command)
            return cursor.fetchall()
    else:
        return "You have no db to execute command"


def get_faculty_list(db):
    SQL="SELECT schema_name FROM information_schema.schemata \
    WHERE NOT schema_name='public' \
    AND NOT schema_name='pg_catalog' \
    AND NOT schema_name='information_schema' \
    AND NOT schema_name='pg_toast';"
    list=cursor(db,SQL)
    for i in range(len(list)):
        list[i]=list[i][0]
    return list
def get_answer_mask(db):
    SQL="SELECT public.questions.id,public.questions.type, public.questions.answer_format FROM public.questions;"
    try:
        return mask_pars(cursor(db,SQL))
    except Exception as _ex:
        print("[INFO]",_ex)
        return "No public schema"
def get_teachers_list_by_faculty(db,faculty):
    SQL=f"SELECT {faculty}.teachers.id, {faculty}.teachers.full_name FROM {faculty}.teachers"
    return cursor(db,SQL)
def get_results(db,faculty,teacher_id):
    SQL=f"SELECT 'lecture' AS typefield, {faculty}.votes.results -> 'lecture',{faculty}.votes.user_id AS {q}result{q} FROM {faculty}.teachers \
            INNER JOIN {faculty}.votes ON {faculty}.votes.teacher_id={faculty}.teachers.id \
            AND {faculty}.teachers.id={teacher_id} \
            AND {faculty}.votes.results::jsonb ? 'lecture' \
            UNION ALL \
            SELECT 'practice' AS typefield, {faculty}.votes.results -> 'practice',{faculty}.votes.user_id FROM {faculty}.teachers \
            INNER JOIN {faculty}.votes ON {faculty}.votes.teacher_id={faculty}.teachers.id \
            AND {faculty}.teachers.id={teacher_id} \
            AND {faculty}.votes.results::jsonb ? 'practice' \
            UNION ALL \
            SELECT 'practice' AS typefield, {faculty}.votes.results -> 'practice',{faculty}.votes.user_id FROM {faculty}.teachers \
            INNER JOIN {faculty}.votes ON {faculty}.votes.teacher_id={faculty}.teachers.id \
            AND {faculty}.teachers.id={teacher_id} \
            AND {faculty}.votes.results::jsonb ? '';" 
    return cursor(db,SQL)

