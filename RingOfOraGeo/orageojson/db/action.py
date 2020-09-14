
import os, cx_Oracle
from orageojson.log.flogger import loginfo, logexcep, flog


def dbopen(p_connstr):
    try:
        os.environ["NLS_LANG"] = ".AL32UTF8"
        global conn
        conn = cx_Oracle.connect(p_connstr, encoding="UTF-8", nencoding="UTF-8")
        global cursor
        cursor = conn.cursor()
        schema = p_connstr.split('/', 1)
    except Exception as e:
        logexcep('$$$ Error db.connet() : {}'.format(e))
        raise

    loginfo('--- EO - DB connection opened. ---')

    return conn, cursor, schema[0]
#.............................

def dbclose():
    try:
        cursor.close
        conn.close
    except Exception as e:
        None

    loginfo('--- EO - DB connection closed. ---')

    return

#-------------------------------------------------
