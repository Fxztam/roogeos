#-------------------------------------------------
#  Loading GeoJSON file to CLOB
#  Friedhold Matz - 2020-aug
#-------------------------------------------------
from orageojson.log.flogger import loginfo, logexcep

def load2table(p_cursor, p_geojson):
    #print('--- BO - load.laod2table. ---')

    try:
        p_cursor.execute('''drop table ld_geojson''')
    except Exception as e:
        None

    try:
        p_cursor.execute('''create table ld_geojson (ldjson clob, constraint chk_ld_geojson check (ldjson IS JSON))''')
    except Exception as e:
        logexcep('$$$ Error load.load2table(create ldgeojson) : {}'.format(e))
        raise

    try:
        with open(p_geojson, 'r', encoding='UTF-8') as f:
            geojson = f.read()

        p_cursor.execute('''insert into ld_geojson (ldjson)
                            values ( :clobdata )''', clobdata=geojson)

        p_cursor.execute("commit")

    except Exception as e:
        logexcep('$$$ Error load.load2table(insert into ldgeojson) : {}'.format(e))
        raise

    loginfo('--- EO - load2table. ---')

    return
# ------------------------------------------
