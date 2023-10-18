import psycopg2 as pg

from pars import mask_pars


q='"'


def connect(host:str, port:int, db_name:str, user:str, password:str):
    """
    Create connection to database
    If error occured return string of "Exception"
    WARNING database conection needs to be closed before stop of program
    """
    try:
        base = pg.connect(host=host,user=user,password=password,database=db_name,port=port)
        base.autocommit = True
        print("[INFO] Connected to database")
        return base
    except Exception as _ex:
        print("[INFO] Exception raised:", _ex)
        return "Exception"


def cursor(db, command:str, args:tuple=tuple()):
    """
    Execute given SQL command
    """
    if db != "Exception":
        with db.cursor() as cursor:
            cursor.execute(command, args)
            return cursor.fetchall()
    else:
        return "You have no db to execute command"



def get_faculty_list(db):
    SQL="SELECT schema_name FROM information_schema.schemata \
    WHERE NOT schema_name='public' \
    AND NOT schema_name='pg_catalog' \
    AND NOT schema_name='information_schema' \
    AND NOT schema_name='pg_toast';"
    list = cursor(db,SQL)
    for i in range(len(list)):
        list[i] = list[i][0]
    return list


def get_answer_mask(db):
    SQL = "SELECT public.questions.id,public.questions.type, public.questions.answer_format FROM public.questions;"
    try:
        return mask_pars(cursor(db, SQL))
    except Exception as _ex:
        print("[INFO]", _ex)
        return "No public schema"


def get_teachers_list_by_faculty(db, faculty:str):
    SQL=f"SELECT %s.teachers.id, %s.teachers.full_name FROM %s.teachers"
    args=[pg.extensions.AsIs(faculty)]*3
    return cursor(db, SQL,args)


def get_results(db, faculty:str, teacher_id:list):
    SQL=f"SELECT 'lecture' AS typefield, %s.votes.results -> 'lecture',%s.votes.user_id AS {q}result{q} FROM %s.teachers \
            INNER JOIN %s.votes ON %s.votes.teacher_id=%s.teachers.id \
            AND %s.teachers.id=%s \
            AND %s.votes.results::jsonb ? 'lecture' \
            UNION ALL \
            SELECT 'practice' AS typefield, %s.votes.results -> 'practice',%s.votes.user_id FROM %s.teachers \
            INNER JOIN %s.votes ON %s.votes.teacher_id=%s.teachers.id \
            AND %s.teachers.id=%s \
            AND %s.votes.results::jsonb ? 'practice' \
            UNION ALL \
            SELECT 'practice' AS typefield, %s.votes.results -> 'practice',%s.votes.user_id FROM %s.teachers \
            INNER JOIN %s.votes ON %s.votes.teacher_id=%s.teachers.id \
            AND %s.teachers.id=%s \
            AND %s.votes.results::jsonb ? '';" 
    args = [pg.extensions.AsIs(faculty)]*7
    args += [pg.extensions.AsIs(teacher_id)]
    args += [pg.extensions.AsIs(faculty)]*8
    args += [pg.extensions.AsIs(teacher_id)]
    args += [pg.extensions.AsIs(faculty)]*8
    args += [pg.extensions.AsIs(teacher_id)]
    args += [pg.extensions.AsIs(faculty)]
    return cursor(db, SQL,args)